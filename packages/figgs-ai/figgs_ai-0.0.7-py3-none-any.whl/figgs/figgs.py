import requests
import json
import uuid

from datetime import datetime
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

current_time = datetime.now()
created_time = current_time.isoformat()

class figgs:
    def __init__(self, url="https://www.figgs.ai/", auth=None):
        self.url = url 
        self.auth = auth

    def fetch_page(self):
        response = requests.get(self.url, verify=False)
        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def change_user_name(self,username: str):
        soup = self.fetch_page()
        if soup:
            headers ={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Content-Type": "application/json",
            }    
            cookies = {
                'figs-auth-prod': self.auth
            }
            payload = {
                "name": username,
 
            }
            edit_url = f"https://www.figgs.ai/api/proxy/users/me"
            requests.patch(edit_url, headers=headers, json=payload, cookies=cookies, verify=False)
            print("Your Username Changed To: ", username)
        else:
            print("ded")

    def change_bio(self,bio: str):
            soup = self.fetch_page()
            if soup:
                headers ={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                }    
                cookies = {
                    'figs-auth-prod': self.auth
                }
                payload = {
                    "description": bio
    
                }
                edit_url = f"https://www.figgs.ai/api/proxy/users/me"
                requests.patch(edit_url, headers=headers, json=payload, cookies=cookies, verify=False)
                print("Your Bio Changed To: ", bio)
            else:
                print("ded")

    def change_suggistives(self,hide_suggestive: bool, hide_suggestive_avatar:bool):
            soup = self.fetch_page()
            if soup:
                headers ={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                }    
                cookies = {
                    'figs-auth-prod': self.auth
                }
                payload = {
                    "hide_suggestive": hide_suggestive,
                    "hide_suggestive_avatar": hide_suggestive_avatar
    
                }
                edit_url = f"https://www.figgs.ai/api/proxy/users/me"
                requests.patch(edit_url, headers=headers, json=payload, cookies=cookies, verify=False)
                print("hide Suggestive: ", hide_suggestive, "Hide Suggestive Avatar: ", hide_suggestive_avatar)
            else:
                print("ded")
    def send_message(self, messages: str, room_id: str, bot_id : str):
        soup = self.fetch_page()
        if soup:
           # session_url = "https://www.figgs.ai/api/auth/session"
           # resp= requests.get(session_url, headers=headers,cookies=cookies, verify=False)
           # print(resp.text)

            headers ={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Content-Type": "application/json",
            }
            cookies = {
                'figs-auth-prod': self.auth
            }

            payload = {
                
                "botId": bot_id,
                "roomId": room_id,
                "messages": [
                    {
                        "id": str(uuid.uuid4()),
                        "role": "user",
                        "content": messages,
                        "created": created_time
                    }
                ]
            }


            api_url = "https://api.figgs.ai/chat_completion"
            response = requests.post(api_url, headers=headers,json=payload,cookies=cookies,verify=False)
            return response