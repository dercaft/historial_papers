import requests
import urllib
from urllib import parse
auth="10419bf0-8084-be2d-7d50-9053a926bbd4"

url="https://api.deepl.com/v1/translate"
# url="https://api.deepl.com/v1/usage"

print(url)
header={
    "Content-Type":"application/x-www-form-urlencoded",
}
content={
    "auth_key":auth,
    "text":"hello world",
    "target_lang":"ZH",
}
response=requests.post(url,headers=header,data=content)
print(response)
print(response.text)