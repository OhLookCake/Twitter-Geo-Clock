
from __future__ import print_function
import oauth2 as oauth
import urllib2 as urllib

access_token_key = "46710702-SqzfnXZxufnl21ZhrZskX68hkA22cmXn3MmNQPbJ0"
access_token_secret = "344U9Nnntj1izFpOzKnmhsBN5vpFrRw0OUfWiuvjU"

consumer_key = "0k51XWHSPXdQ7RCbsPCffg"
consumer_secret = "pr0mEgILcHBQpenripWr3nfsSb88cZffBPaJvNgF0k"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''

def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

import json

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  
  hasgeo=0
  nogeo=0
  timestamp=""
  for line in response:
    #extract timestamp, geo data from line
	
    jtweet=json.loads(line)
    if 'created_at' in jtweet:
        timestamp=jtweet['created_at']
    if 'coordinates' in jtweet and jtweet['coordinates']!=None:
        long=jtweet['coordinates']['coordinates'][0]
        lat=jtweet['coordinates']['coordinates'][1]
        print(timestamp,long,lat,sep=',')
        #If timestamp does not exist, and coordinates do, the timestamp will be one-behind. That's cool, though.
        hasgeo+=1
    else:
        nogeo+=1
        
	

if __name__ == '__main__':
  fetchsamples()