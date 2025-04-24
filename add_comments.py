import os   
from dotenv import load_dotenv   
import requests
import json
from typing import Dict, List, Optional, Any, Union


class JIRAAddComments:
    def __init__(self, base_url:str, email:str, api_token:str):
        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers={
  "Accept": "application/json",
  "Content-Type": "application/json"
        }
        
    def add_comment_to_issue(self, issueId):
        """https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/#api-rest-api-3-issue-issueidorkey-comment-post"""
        print("Add add comment to ticket SP-3 : ")
        user_input = str(input())
        url = f"{self.base_url}/rest/api/3/issue/{issueId}/comment"
        print(f"Base url being sent {url}")
        
        addComment =json.dumps(  {
  "body": {
    "content": [
      {
        "content": [
          {
            "text": user_input,
            "type": "text"
          }
        ],
        "type": "paragraph"
      }
    ],
    "type": "doc",
    "version": 1
  },

} )


        
        
        response = requests.post(
            url,
            headers=self.headers,
            auth=self.auth,
            data=addComment
                   
        )
        response.raise_for_status()
        print(f"::: check for return message ${response.text}")
        

        
        










if __name__ == "__main__":
    jira = JIRAAddComments(
        base_url=os.getenv("JIRA_BASE_URL"),
        email=os.getenv("JIRA_EMAIL"),
        api_token=os.getenv("VINIT_API_TOKEN"),
    )
    jira.add_comment_to_issue(issueId="SP-3")