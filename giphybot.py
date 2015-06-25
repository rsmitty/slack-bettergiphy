from flask import Flask, request
import json
import urllib2

app = Flask(__name__)  

##Base URL for Giphy. Embeds rating, limit, and the beta API key.
giphyurl = "http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&limit=5&rating=g&q="  

##Slack variables to edit. Token from slash command and hook url from incoming webhook integration.
slacktoken = "INSERT-SLACK-TOKEN-HERE"
slackhookurl = "INSERT-SLACK-WEBHOOK-URL-HERE"

@app.route("/", methods=['POST'])
def root():

  ##Verify that toke is what we expect, if so, retrieve search string and replace space with plus.
  ##After, we'll query giphy for our search string
  if request.form['token'] == slacktoken:
    searchtext = request.form['text'].replace(" ","+")
    return_string = query_giphy(searchtext)
  else:
    return_string = "Something is broken!"

  ##Return results to Slack incoming webhook.
  req = urllib2.Request(slackhookurl)
  req.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(req, return_string)
  return ""

##Crafts a full rest query and retrieves the response from giphy. 
##Passes result to parse_results.
def query_giphy(searchtext):
  fullurl = giphyurl+searchtext
  response = urllib2.urlopen(fullurl).read()
  returnresponse = parse_results(response)
  return returnresponse

##Parse JSON results, up to 5 gifs. Looks for the first one that's < 2MB to return.
##If none are small enough, it just returns the first, most relevant result
##That gif will not expand in Slack
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

  if gifiter == 5:
    gifiter = 0
  else:  
    gifurl = jsondict['data'][gifiter]['images']['original']['url']
    gifjson =  json.dumps({ 'username': user, 'channel': channel, 'text': searchstring+"\n"+gifurl })

  return gifjson

if __name__ == "__main__":
  app.run(host='0.0.0.0')
