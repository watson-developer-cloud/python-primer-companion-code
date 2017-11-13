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

import os
import json

from flask import Flask, jsonify, render_template, redirect, session, url_for
from flask import request
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

from watson_developer_cloud import WatsonException

from watsonutils.languagetranslation import LanguageTranslationUtils
from watsonutils.naturallanguageclassification import NaturalLanguageClassifierUtils
from watsonutils.naturallanguageunderstanding import NaturalLanguageUnderstandingUtils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'please subtittute this string with something hard to guess'

class LangForm(Form):
    txtdata = TextAreaField('Text to process', validators=[Required()])
    submit = SubmitField('Process')

@app.route('/wl/lang', methods=['GET', 'POST'])
def wlhome():
    app.logger.info('wlhome page requested')
    allinfo = {}
    outputTxt = "TBD"
    targetlang = 'en'
    lang = "TBD"
    txt = None
    form = LangForm()
    if form.validate_on_submit():
        lang = "TBC"
        txt = form.txtdata.data
        form.txtdata.data = ''

        try:
            ltu = LanguageTranslationUtils(app)
            nlcu = NaturalLanguageClassifierUtils(app)
            nlu = NaturalLanguageUnderstandingUtils(app)                      
            lang = ltu.identifyLanguage(txt)
            primarylang = lang["language"]
            confidence = lang["confidence"]

            englishTxt = None
            outputTxt = "I am %s confident that the language is %s" % (confidence, primarylang)
            if targetlang != primarylang:
                supportedModels = ltu.checkForTranslation(primarylang, targetlang)
                if supportedModels:
                    englishTxt = ltu.performTranslation(txt, primarylang, targetlang)
                    outputTxt += ", which in english is %s" % englishTxt
                    classification = nlcu.classifyTheText(englishTxt)
                else:
                    outputTxt += ", which unfortunately we can't translate into English"
            else:
                englishTxt = txt

            if englishTxt:
                classification = nlcu.classifyTheText(txt)
                if classification:
                    outputTxt += "(and %s confident that it is %s classification)" \
                                              % (classification['confidence'],
                                                 classification['className'])

                nluResults = nlu.identifyKeyworkdsAndEntities(englishTxt)
                app.logger.info(nluResults)

                if nluResults:
                    if 'prime_entity' in nluResults:
                        outputTxt += ' Primary entity is %s ' % nluResults['prime_entity']
                    if 'prime_keyword' in nluResults:
                        outputTxt += ' Primary keyword is %s' % nluResults['prime_keyword']

            session['langtext'] = outputTxt

            allinfo['lang'] = lang
            allinfo['form'] = form
            return redirect(url_for('wlhome'))
        except WatsonException as err:
          allinfo['error'] = err

    allinfo['lang'] = session.get('langtext')
    allinfo['form'] = form
    return render_template('watson/wlindex.html', info=allinfo)


@app.route('/api/process/', methods=['POST'])
def apiprocess():
    app.logger.info('REST API for process has been invoked')
    targetlang = 'en'
    classification = {"className":"unknown"}
    nluResults = {"prime_entity":"unknown",
                      "prime_keyword": "unknown"  }
    results = {}
    theData = {"error":"If you see this message then something has gone badly wrong"}

    app.logger.info(request.form['txtdata'])
    if not 'txtdata' in request.form:
        theData = {"error":"Text to be processed must not be blank"}
    else:
        del theData["error"]
        try:
            data = request.form['txtdata']
            ltu = LanguageTranslationUtils(app)
            nlcu = NaturalLanguageClassifierUtils(app)
            nlu = NaturalLanguageUnderstandingUtils(app)

            englishTxt = None
            primarylang = theData['language'] = ltu.identifyLanguage(data)["language"]
            if targetlang != primarylang:
                supportedModels = ltu.checkForTranslation(primarylang, targetlang)
                if supportedModels:
                    englishTxt = ltu.performTranslation(data, primarylang, targetlang)
                    classification = nlcu.classifyTheText(englishTxt)
            else:
                englishTxt = data
            if englishTxt:
                classification = nlcu.classifyTheText(data)
                nluResults = nlu.identifyKeyworkdsAndEntities(englishTxt)
                app.logger.info(nluResults)

            theData['classification'] = classification.get('className', None)
            theData['primary_entity'] = nluResults.get('prime_entity', None)
            theData['primary_keyword'] = nluResults.get('prime_keyword', None)

        except WatsonException as err:
            theData['error'] = err;

    results["results"] = theData
    return jsonify(results), 201


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)
