#!/usr/bin/env python
# coding=utf-8
'''
Author: JiangJi
Email: johnjim0816@gmail.com
Date: 2023-12-22 23:02:13
LastEditor: JiangJi
LastEditTime: 2024-06-14 09:26:17
Discription: 
'''
import torch
import torch.nn as nn
import math, random
import numpy as np
from joyrl.algos.base.policy import BasePolicy
from joyrl.algos.base.network import QNetwork
class Policy(BasePolicy):
    def __init__(self,cfg) -> None:
        super(Policy, self).__init__(cfg)
        self.gamma = cfg.gamma  
        # e-greedy parameters
        self.epsilon_start = cfg.epsilon_start
        self.epsilon_end = cfg.epsilon_end
        self.epsilon_decay = cfg.epsilon_decay
        self.target_update = cfg.target_update
        self.sample_count = 0
        self.update_step = 0

    def create_model(self):
        self.model = QNetwork(self.cfg,self.state_size_list).to(self.device)
        self.target_model = QNetwork(self.cfg,self.state_size_list).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict()) # or use this to copy parameters
    
    def load_model_meta(self, model_meta):
        super().load_model_meta(model_meta)
        if model_meta.get('sample_count') is not None:
            self.sample_count = model_meta['sample_count']

    def sample_action(self, state, **kwargs):
        ''' sample action
        '''
        self.sample_count += 1
        # epsilon must decay(linear,exponential and etc.) for balancing exploration and exploitation
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * \
            math.exp(-1. * self.sample_count / self.epsilon_decay) 
        self.update_model_meta({'sample_count': self.sample_count})
        if random.random() > self.epsilon:
            action = self.predict_action(state)
        else:
            action = [self.action_space.sample()]
        return action
    
    @torch.no_grad()
    def predict_action(self,state, **kwargs):
        ''' predict action
        '''
        state = [torch.tensor(np.array(state), device=self.device, dtype=torch.float32).unsqueeze(dim=0)]
        model_outputs = self.model(state)
        actor_outputs = model_outputs['actor_outputs']
        actions = self.model.action_layers.get_actions(mode = 'predict', actor_outputs = actor_outputs)
        return actions
    
    def learn(self, **kwargs):
        ''' learn policy
        '''
        super().learn(**kwargs)
        actor_outputs = self.model(self.states)['actor_outputs']
        target_actor_outputs = self.target_model(self.next_states)['actor_outputs']
        tot_loss = 0
        self.summary_loss = []
        for i in range(len(self.action_size_list)):
            actual_q_value = actor_outputs[i]['q_value'].gather(1, self.actions[i].long())
            next_q_values = target_actor_outputs[i]['q_value']
            next_target_q_values_action = next_q_values.gather(1, torch.max(next_q_values, 1)[1].unsqueeze(1))
            expected_q_value = self.rewards + self.gamma * next_target_q_values_action * (1 - self.dones)
            loss_i = nn.MSELoss()(actual_q_value, expected_q_value)
            tot_loss += loss_i
            self.summary_loss.append(loss_i.item())
        self.optimizer.zero_grad() 
        tot_loss.backward()
        # clip to avoid gradient explosion
        for param in self.model.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
        # update target net every C steps
        if self.update_step % self.target_update == 0: 
            self.target_model.load_state_dict(self.model.state_dict())
        self.update_step += 1
        self.update_summary() # update summary
        
        