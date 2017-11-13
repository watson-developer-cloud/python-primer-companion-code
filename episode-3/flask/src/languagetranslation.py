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

import json

from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslationService
from watson_developer_cloud import WatsonException


class LanguageTranslationUtils(object):
  def __init__(self, app):
    super(LanguageTranslationUtils, self).__init__()
    self.app = app
    self.service = LanguageTranslationService(username='<your username key for the Watson language translation service>',
                                      password='<your password key for the service>')

  def getTranslationService(self):
    return self.service

  def identifyLanguage(self, data):
    txt = data.encode("utf-8", "replace")
    language_translation = self.getTranslationService()
    langsdetected = language_translation.identify(txt)

    self.app.logger.info(json.dumps(langsdetected, indent=2))
    self.app.logger.info(langsdetected["languages"][0]['language'])
    self.app.logger.info(langsdetected["languages"][0]['confidence'])

    primarylang = langsdetected["languages"][0]['language']
    confidence = langsdetected["languages"][0]['confidence']

    retData = { "language" : primarylang,
                "confidence" : confidence }
    return retData


  def checkForTranslation(self, fromlang, tolang):
    supportedModels = []
    lt = self.getTranslationService()
    models = lt.get_models()
    if models and ("models" in models):
      modelList = models["models"]
      for model in modelList:
        if fromlang == model['source'] and tolang == model['target']:
          supportedModels.append(model['model_id'])
    return supportedModels

  def performTranslation(self, txt, primarylang, targetlang):
    lt = self.getTranslationService()
    translation = lt.translate(txt, source=primarylang, target=targetlang)
    return translation
