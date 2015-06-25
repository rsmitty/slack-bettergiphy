from flask import Flask, request
import json
import urllib2

app = Flask(__name__)  
giphyurl = "http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&limit=1&rating=g&q="  

@app.route("/", methods=['POST'])
def root():
  if request.form['token'] == "INSERT-SLACK-TOKEN-HERE":
    searchtext = request.form['text'].replace(" ","+")
    return_string = query_giphy(searchtext)
  else:
    return_string = "Something is broken!"

  req = urllib2.Request('https://hooks.slack.com/services/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')
  req.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(req, return_string)
  return ""

def query_giphy(searchtext):
  fullurl = giphyurl+searchtext
  print fullurl
  response = urllib2.urlopen(fullurl).read()
  returnresponse = parse_results(response)
  return returnresponse

def parse_results(jsonresponse):
  user = request.form['user_id']
  channel = request.form['channel_id']
  searchstring = '/giphy++ ' + request.form['text']
  jsondict = json.loads(jsonresponse)
  gifurl = jsondict['data'][0]['images']['original']['url']
  gifjson =  json.dumps({ 'username': user, 'channel': channel, 'text': searchstring+"\n"+gifurl })
  return gifjson

if __name__ == "__main__":
  app.run(host='0.0.0.0')
