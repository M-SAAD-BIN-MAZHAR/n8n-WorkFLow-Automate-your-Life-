import requests
user_message="Get the data from the google sheet and add all the expenses" 
request_message={"message":user_message}
url="http://localhost:5678/webhook-test/557d3f68-3720-499e-8419-1a45c142dbef"
response=requests.post(url,json=request_message)
print(response.status_code)
print(response.json()[0]['output'])