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
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

from watson_developer_cloud import LanguageTranslationV2 as LanguageTranslation
from watson_developer_cloud import WatsonException

# Initialise the application and the secret key needed for CSRF protected form submission.
# You should change the secret key to something that is secret and complex.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'please subtitute this string with something hard to guess'

# The form containing the text to be processed that the application web page will be submitted/
class LangForm(Form):
    txtdata = TextAreaField('Text to process', validators=[Required()])
    submit = SubmitField('Process')

# As this is the only route defined in this application, so far, it is the only page that 
# the application will respond to.
@app.route('/wl/lang', methods=['GET', 'POST'])
def wlhome():
    # This is how you do logging, in this case information messages.
    app.logger.info('wlhome page requested')
    allinfo = {}
    lang = "TBD"
    txt = None
    form = LangForm()
    # If the form passes this check, then its a POST and the fields are valid. ie. if the 
    # request is a GET then this check fails.	
    if form.validate_on_submit():
        lang = "TBC"
        txt = form.txtdata.data
        form.txtdata.data = ''

        try:
            language_translation = LanguageTranslation(username='<your username key for the Watson language translation service>',
                                                   password='<your password key for the service>')
            langsdetected = language_translation.identify(txt)
            primarylang = langsdetected["languages"][0]['language']
            confidence = langsdetected["languages"][0]['confidence']

            lang = "I am %s confident that the language is %s" % (confidence, primarylang)            
            session['langtext'] = lang

            allinfo['lang'] = lang
            allinfo['form'] = form
            return redirect(url_for('wlhome'))
        except WatsonException as err:
          allinfo['error'] = err

    allinfo['lang'] = session.get('langtext')
    allinfo['form'] = form
    return render_template('watson/wlindex.html', info=allinfo)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
