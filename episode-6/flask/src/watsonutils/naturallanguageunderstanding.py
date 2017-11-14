# -*- coding: utf-8 -*-
# Copyright 2017 IBM Corp. All Rights Reserved.
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

from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NaturalLanguageUnderstanding
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

from watson_developer_cloud import WatsonException

from .baseservice import BaseService

class NaturalLanguageUnderstandingUtils(BaseService):
  def __init__(self, app):
    self.app = app
    super(NaturalLanguageUnderstandingUtils, self).__init__("natural_language_understanding")

    self.service = NaturalLanguageUnderstanding(username=self.getUser(),
                                              password=self.getPassword(),
                                              version="2017-02-27")

  def getNLUService(self):
    return self.service

  def identifyKeyworkdsAndEntities(self, data):
    self.app.logger.info('Preparing to invoke Natural Language Understanding service')
    txt = data.encode("utf-8", "replace")
    nlu = self.getNLUService()

    results = nlu.analyze(text=data, return_analyzed_text=True,
                       features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()))

    self.app.logger.info(json.dumps(results, indent=2))

    primeEntity = None
    primeKeyword = None

    if 'entities' in results:
      entities = results['entities']
      if 0 < len(entities):
        primeEntity = entities[0].get('text', None)

    if 'keywords' in results:
      keywords = results['keywords']
      if 0 < len(keywords):
        primeKeyword = keywords[0].get('text', None)


    retData = { "prime_entity" : primeEntity,
                "prime_keyword" : primeKeyword }
    return retData
