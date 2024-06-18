import pymsteams

class Chat_Message:
    def __init__(self, webhook, sas_token):
        self.webhook = webhook
        self.sas_token = sas_token
        
    def send_message_to_chat(self, body):
        teams_message = pymsteams.connectorcard(self.webhook)
        teams_message.payload = {
            "type": "message",
            "attachments": [
                {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": body,
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0",
                }
            }]
        }
        teams_message.send()