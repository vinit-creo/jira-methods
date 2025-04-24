import requests
from dotenv import load_dotenv   
import os   

class JiraAPIAssign:
    def __init__(self, base_url: str, email:str, api_token:str):
        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"            
        }
    
    def fetch_user_id(self):
        
        print("Enter email of user: ")
        user_input = str(input())
        
   

        url = f"{self.base_url}/rest/api/3/user/search"
    
        params = {
            "query": user_input
            }
    
        response = requests.get(
                url,
                params=params,
                headers=self.headers,
                auth=self.auth
                )
    
        response.raise_for_status()
        users = response.json()
    
        if not users:
            raise ValueError(f"No user found with email")
        print(f"Account id : ",{users[0]["accountId"]})
        return users[0]["accountId"]
    
    def assign_issue(self, issue_key: str, account_id: str) -> bool:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/assignee"
        payload = {
            "accountId": account_id
            }
        print(f" payload in assign issue method ${payload}")
    
        response = requests.put(
                    url,
                    json=payload,
                    headers=self.headers,
                    auth=self.auth
                    )
    
        response.raise_for_status()
        return True    



    def get_assigneable_users_for_issue(self) -> None:
        url = f"""{self.base_url}/rest/api/3/user/assignable/search"""
        payload = {
            "issueID":"SP-2" 
            }
        response = requests.request("GET",url,headers=self.headers,params=payload,auth=self.auth)
        print(f"::: response {response.text}")
             
    
    
    
    
    
if __name__ == "__main__":
    jira = JiraAPIAssign(
        base_url=os.getenv("JIRA_BASE_URL"),
        email=os.getenv("JIRA_EMAIL"),
        api_token=os.getenv("VINIT_API_TOKEN"),
    )
    user_id = jira.fetch_user_id()  
    jira.assign_issue(account_id=user_id,issue_key="SP-2")

     
    