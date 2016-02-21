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
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms

from watson_developer_cloud import LanguageTranslationV2 as LanguageTranslation
from watson_developer_cloud import WatsonException

import json

import logging
logger = logging.getLogger(__name__)

class Form_language(forms.Form):
  txtdata = forms.CharField(required=True,
                             label="Text to Process",
                             widget=forms.Textarea)

def index(request):
  allinfo = {}
  form = None
  if request.POST:
    form = Form_language(request.POST)
    if form.is_valid():
      data = form.cleaned_data['txtdata']
      logger.info("Text to be process is %s" % data)
      lang = "TBD"

      try:
        language_translation = LanguageTranslation(username='<You watson language translation service username key>',
        	                                       password='<sevice password key>')
        langsdetected = language_translation.identify(data)
        primarylang = langsdetected["languages"][0]['language']
        confidence = langsdetected["languages"][0]['confidence']

        lang = "I am %s confident that the language is %s" % (confidence, primarylang)
      except WatsonException as err:
      	allinfo['error'] = err

      allinfo['lang'] = lang
    else:
      allinfo['error'] = "The form is invalid" 
  else:
    form = Form_language
    
  allinfo['form'] = form
  return render(request, 'watson/wlindex.html', allinfo)
