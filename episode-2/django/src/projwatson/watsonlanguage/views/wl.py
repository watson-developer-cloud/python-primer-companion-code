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

from django.shortcuts import render
from django import forms

from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslationService
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
  outputTxt = "TBD"
  targetlang = 'en'
  form = None
  if request.POST:
    form = Form_language(request.POST)
    if form.is_valid():
      data = form.cleaned_data['txtdata']
      logger.info("Text to be process is %s" % data)
      lang = "TBD"

      try:
        lang = identifyLanguage(data)
        primarylang = lang["language"]
        confidence = lang["confidence"]

        outputTxt = "I am %s confident that the language is %s" % (confidence, primarylang)
        if targetlang != primarylang:
          supportedModels = checkForTranslation(primarylang, targetlang)
          if supportedModels:
            englishTxt = performTranslation(data, primarylang, targetlang)
            outputTxt += ", which in english is %s" % englishTxt
          else:
            outputTxt += ", which unfortunately we can't translate into English"

      except WatsonException as err:
      	allinfo['error'] = err

      allinfo['lang'] = outputTxt
    else:
      allinfo['error'] = "The form is invalid"
  else:
    form = Form_language

  allinfo['form'] = form
  return render(request, 'watson/wlindex.html', allinfo)

def getTranslationService():
  return LanguageTranslationService(username='<Your watson language translation service username key>',
                                    password='<sevice password key>')

def identifyLanguage(data):
  txt = data.encode("utf-8", "replace")
  language_translation = getTranslationService()
  langsdetected = language_translation.identify(txt)

  logger.info(json.dumps(langsdetected, indent=2))
  logger.info(langsdetected["languages"][0]['language'])
  logger.info(langsdetected["languages"][0]['confidence'])

  primarylang = langsdetected["languages"][0]['language']
  confidence = langsdetected["languages"][0]['confidence']

  retData = { "language" : primarylang,
              "confidence" : confidence }
  return retData


def checkForTranslation(fromlang, tolang):
  supportedModels = []
  lt = getTranslationService()
  models = lt.list_models()
  if models and ("models" in models):
    modelList = models["models"]
    for model in modelList:
      if fromlang == model['source'] and tolang == model['target']:
        supportedModels.append(model['model_id'])
  return supportedModels

def performTranslation(txt, primarylang, targetlang):
  lt = getTranslationService()
  translation = lt.translate(txt, source=primarylang, target=targetlang)
    theTranslation = None
    if translation and ("translations" in translation):
      theTranslation = translation['translations'][0]['translation']
    return theTranslation
