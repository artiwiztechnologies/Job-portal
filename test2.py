import requests
import json

body = {
  "to": [
    {
      "name": "Felix",
      "email": "felixjordan312@gmail.com"
    }
  ],
  "from": {
    "name": "Textile Jobs",
    "email": "noreply@mail.jobstextile.com"
  },

  "domain": "mail.jobstextile.com",
  "mail_type_id": 3,

  "template_id": "Email-Confirmation",
  "variables": {
    "VAR1": "https://jobstextile.com" 
  },
  "authkey": "368863A1EOG1DR61766562P1"
}

url = "https://api.msg91.com/api/v5/email/send"

response = requests.post(url, data = json.dumps(body), headers = {"Content-type": "application/json", 'Accept': 'application/json'}).json()

print(response)