import requests

class MS_Teams():
    def __init__(self, client_id, client_secret, tenant_id, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.username = username
        self.password = password
        
    def get_headers(self, bearer_token):
        """This is the headers for the Microsoft Graph API calls"""
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "ConsistencyLevel": "eventual",
        }


    def get_token_for_user_application(self):
        """
        Get Token on behalf of a user using username/password
        """

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        payload = (
            f"grant_type=password&client_id={self.client_id}&username={self.username}&password={self.password}"
            "&scope=User.Read"
        )
        headers = {}

        resp = requests.request("POST", url, headers=headers, data=payload)
        if resp.status_code != 200:
            return None
        return resp.json()["access_token"]


    def get_token_for_client_application(self):
        """
        Get Token on behalf of a client application using client_secret/client_id
        """

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        payload = (
            f"grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}"
            "&scope=https%3A//graph.microsoft.com/.default"
        )
        headers = {}

        resp = requests.request("POST", url, headers=headers, data=payload)
        if resp.status_code != 200:
            return None
        return resp.json()["access_token"]


    def get_signedin_user_data(self, bearer_token):
        """
        Get SignedIn user data
        """

        resp = requests.get(f"https://graph.microsoft.com/v1.0/me",
                            headers=self.get_headers(bearer_token))

        json_resp = resp.json()
        return json_resp


    def get_ms_teams_users(self, bearer_token, filters=""):
        """
        Get/Search MS Teams users
        """

        if filters:
            filters = f"$filter={filters}"

        url = f"https://graph.microsoft.com/beta/users?{filters}"
        resp = requests.get(url, headers=self.get_headers(bearer_token))
        if resp.status_code != 200:
            print(resp.json())
            return None

        json_resp = resp.json()
        try:
            return json_resp["value"]
        except KeyError as err:
            return []


    def send_message_to_ms_teams_user(self, bearer_token, sender_ms_team_id, user_ms_teams_id, payload):
        """
        Send Message to MS Teams user is done in 2 steps:
            1: Create chat
            2: Use chat-id created in 1st step and send message to the user.
        """
        # 1st step: Create chat
        creat_chat_url = "https://graph.microsoft.com/v1.0/chats"
        data = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_ms_teams_id}')",
                },
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{sender_ms_team_id}')",
                },
            ],
        }

        resp = requests.post(
            creat_chat_url, headers=self.get_headers(bearer_token), json=data)
        json_resp = resp.json()
        if resp.status_code not in [200, 201]:
            return False

        # 2nd step: Use created chat-id and send message to it.
        chat_id = json_resp["id"]
        send_message_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
 
        
        resp = requests.post(send_message_url, headers=self.get_headers(
            bearer_token), json=payload)
        json_resp = resp.json()
        if resp.status_code not in [200, 201]:
            return False

        return True


    def get_ms_teams_users_using_emails(self, bearer_token, emails=[]):
        filters = [f"mail eq '{email}'" for email in emails]
        filters = " OR ".join(filters)
        users = self.get_ms_teams_users(bearer_token, filters=filters)

        return users
    
    def main(self, payload, emails):

        # Get Client application token
        client_app_token = MS_Teams.get_token_for_client_application(self)

        # Get User application token
        user_app_token = MS_Teams.get_token_for_user_application(
            self)

        # Get SignedIn user data
        signedin_user_data = MS_Teams.get_signedin_user_data(self, user_app_token)
        sender_ms_teams_id = signedin_user_data["id"]

        # Search user(s) with email
        ms_teams_users = MS_Teams.get_ms_teams_users_using_emails(self,
            client_app_token, emails=[emails])

        # Get first user id of above search
        ms_teams_user_id = ms_teams_users[0]["id"]

        # Send message
        is_message_sent = MS_Teams.send_message_to_ms_teams_user(
            self, user_app_token, sender_ms_teams_id, ms_teams_user_id, payload)

        if is_message_sent:
            print("Message sent")
        else:
            print("Message sending Failed")