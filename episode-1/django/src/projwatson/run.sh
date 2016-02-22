#!/bin/bash

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

# This file must be saved as a UNIX File

if [ -z "$VCAP_APP_PORT" ];
then SERVER_PORT=80;
else SERVER_PORT="$VCAP_APP_PORT";
fi
echo port is $SERVER_PORT
echo Performing database initialisations and migrations
python manage.py makemigrations
python manage.py migrate
python manage.py shell < initdbadmin.py
echo [$0] Starting Django Server...
python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload
