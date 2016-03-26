# -*- coding: utf-8 -*-
# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

#Logging doesn't work from manage.py shell
#import logginglogger = logging.getLogger(__name__)

class MainProgram(object):
  def __init__(self):
    print('help')  	
    try:
      print('initialising')    	
      User.objects.create_superuser (username='<the admin id that you will want to use>',
                                     password='<the admin password>',
                                     email='an-email-address@yourco.com')
    except IntegrityError as e:
      print ("DB Error Thrown %s" % e)  	
    #logger.warning("DB Error Thrown %s" % e)
