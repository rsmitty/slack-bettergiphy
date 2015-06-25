from flask import Flask, request
import json
import urllib2
import time

app = Flask(__name__)  
giphyurl = "http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&limit=5&rating=g&q="  

slacktoken = "INSERT-SLACK-TOKEN-HERE"
slackhookurl = "INSERT-SLACK-WEBHOOK-URL-HERE"

@app.route("/", methods=['POST'])
def root():
  if request.form['token'] == slacktoken:
    searchtext = request.form['text'].replace(" ","+")
    return_string = query_giphy(searchtext)
  else:
    return_string = "Something is broken!"
  req = urllib2.Request(slackhookurl)
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
  user = request.form['user_name']
  channel = request.form['channel_id']
  searchstring = '/giphy++ ' + request.form['text']
  jsondict = json.loads(jsonresponse)

  gifiter = 0
  while gifiter < 5:
    if int(jsondict['data'][gifiter]['images']['original']['size']) <= 2097152:
      break

    gifiter += 1

  ##If all 5 were larger than 2MB, we'll just return the first (most relevant)
  ##one and not worry about Slack expansion of the gif.
  if gifiter == 5:
    gifiter = 0
  else:  
    gifurl = jsondict['data'][gifiter]['images']['original']['url']
    gifjson =  json.dumps({ 'username': user, 'channel': channel, 'text': searchstring+"\n"+gifurl })

  return gifjson

if __name__ == "__main__":
  app.run(host='0.0.0.0')
