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

def get_vcap_settings(var_service):
  """ Pulls VCAP settings from Bluemix environmental values"""
  app_vcap_config = os.environ.get('VCAP_SERVICES')
  if app_vcap_config:
    app_decoded_config = json.loads(app_vcap_config) 
    for key, value in app_decoded_config.items():
      if key.startswith(var_service): 
        the_creds = app_decoded_config[key][0]['credentials'] 
        return the_creds
  return None