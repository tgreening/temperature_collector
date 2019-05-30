# importing the requests library
import requests, json
 
# defining the api-endpoint 
API_ENDPOINT = "https://hooks.slack.com/services/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"
 
 
# data to be sent to api
message = "HOuse temperature is 54.8F"
data = json.dumps({'text':message,'username':'Temperature Collector'})
headers = {'Content-Type': 'application/json'}
 
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data, headers = headers)
 
# extracting response text 
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)
