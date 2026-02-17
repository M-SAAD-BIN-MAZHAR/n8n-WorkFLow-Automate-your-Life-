import requests
user_message="Get the data from the google sheet and add all the expenses" 
request_message={"message":user_message}
url=""
response=requests.post(url,json=request_message)
print(response.status_code)
print(response.json()[0]['output'])
