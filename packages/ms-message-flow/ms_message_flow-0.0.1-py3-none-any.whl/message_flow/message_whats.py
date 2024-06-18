import requests
import json

class WhatsAppMessage:
  def __init__(self, from_number, to_number, template_name, template_data, language, authorization):
    self.from_number = from_number
    self.to_number = to_number
    self.template_name = template_name
    self.template_data = template_data
    self.language = language
    self.url = "https://nzrvly.api.infobip.com/whatsapp/1/message/template"
    self.headers = {
      'Authorization': authorization,
      'Content-Type': 'application/json'
    }
    
  def send(self):
    payload = json.dumps({
      "messages": [
        {
          "from": self.from_number,
          "to": self.to_number,
          "messageId": "{{$guid}}",
          "content": {
            "templateName": self.template_name,
            "templateData": self.template_data,
            "language": self.language
          }
        }
      ]
    })
    response = requests.request("POST", self.url, headers=self.headers, data=payload)
    return response