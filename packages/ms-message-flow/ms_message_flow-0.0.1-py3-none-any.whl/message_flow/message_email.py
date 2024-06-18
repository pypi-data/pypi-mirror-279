from msal import PublicClientApplication
import requests
import logging


class Email_Message():
    def __init__(self, client_id, tenant_id, username, password):
        # Atributos da classe
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.authority_url = 'https://login.microsoftonline.com/' + tenant_id
        self.scope = ['https://graph.microsoft.com/.default']
        self.username = username
        self.password = password
        self.access_token = None
        # Obtendo o token de acesso
        self.__obter_token()

    # Método para obter o token de acesso
    def __obter_token(self):
        app = PublicClientApplication(
            self.client_id, authority=self.authority_url)
        result = app.acquire_token_by_username_password(
            username=self.username, password=self.password, scopes=self.scope)
        if 'access_token' in result:
            self.access_token = result['access_token']
            return True
        else:
            logging.error(result.get("error"))
            logging(result.get("error_description"))
            return

    def send_message_email(self, payload):
        url = "https://graph.microsoft.com/v1.0/me/sendMail"

        headers = {
            "Content-type": "application/json",
            "Authorization": self.access_token
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 202:
            logging.warning("Email sent successfully!")
        else:
            logging.warning(
                f"Error sending email. Status code: {response.status_code}")
