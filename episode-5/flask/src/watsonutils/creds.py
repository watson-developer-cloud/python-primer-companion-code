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

import os
import json

class CredentialStore(object):
  """
    Load Credentials from local store
  """
  creds = None
  
  def __init__(self):
    super(CredentialStore, self).__init__() 
    if CredentialStore.creds is None:
        module_dir = os.path.dirname(__file__) 
        file_path = os.path.join(module_dir, '../static/', 'credentials.json')	
        print("Looking for file ", file_path)
        try:
          with open(file_path) as f:
            CredentialStore.creds = json.loads(f.read())
        except FileNotFoundError:
          print("Credential File was not found")
	  	
  def getCreds(self, service):
    if CredentialStore.creds:
      return CredentialStore.creds.get(service, None)  
    else:
      return None	
	