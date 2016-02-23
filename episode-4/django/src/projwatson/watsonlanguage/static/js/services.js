/*
   Copyright 2016 IBM Corp. All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/   
$(document).ready(function() {
  javascriptCheck();
});


function javascriptCheck() {
  // if javascript is enabled on the browser then can
  // remove the warning message
  $('#no-script').remove();
}

function onProcessClick(urlForAPI){
  console.log('Will be Processing REST API ', urlForAPI);
  $('#id_language').text('');
  $('#id_classification').text('');
  $('#id_errormessagefromserver').text(
         'Service has been invoked, waiting for response');
  
  var ajaxData = "txtdata=" + $('#id_txtdata').val();

  $.ajax({
     type: 'POST',
     url: urlForAPI,
     data: ajaxData,
     success: processOK,
     error: processNotOK
  });
}  

function processNotOK() {
  // There was a problem in the request
  console.log('REST API call failed');
  $('#id_errormessagefromserver').text('Service has failed');
}

function processOK(response) {
  console.log('REST API call was good');

  // Check for Error
  var results = response['results'];
  if (results) {
    var errMessage = results['error'];
    if (errMessage) {
      $('#id_errormessagefromserver').text(errMessage);
    } else {
      $('#id_errormessagefromserver').text('');
    }

    console.log(results)

    var language = results['language'];
    if (language) {
      $('#id_language').text(language);
    }

    var classification = results['classification'];
    if (classification) {
      $('#id_classification').text(classification); 
    }
  }
}  


