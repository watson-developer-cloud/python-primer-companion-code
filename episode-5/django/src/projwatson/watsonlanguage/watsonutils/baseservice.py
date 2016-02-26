# -*- coding: utf-8 -*-
# Copyright 2016 IBM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from .creds import CredentialStore
from .vcap import get_vcap_settings

import logging
logger = logging.getLogger(__name__)

class BaseService(object):
  def __init__(self,  serviceName):
    super(BaseService, self).__init__()  

    self.username = "<username>"
    self.password = "<password>"	

    creds = get_vcap_settings(serviceName)
    if not creds:
      credStore = CredentialStore()      
      creds = credStore.getCreds(serviceName)
    if creds:  
      self.username = str(creds['username'])
      self.password = str(creds['password']) 
    else:
      logger.warn("No credentials found for service %s" % serviceName)

  def getUser(self):
    return self.username

  def getPassword(self):
    return self.password

	
