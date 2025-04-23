import os   
from dotenv import load_dotenv   
import requests
import json
from typing import Dict, List, Optional, Any, Union

class JiraAPI:

    def __init__(self, base_url: str, email: str, api_token: str):

        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def get_available_transitions(self, issue_key: str) -> Dict:
        """
        Documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-transitions-get
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        
        response = requests.get(
            url,
            headers=self.headers,
            auth=self.auth
        )
        
        response.raise_for_status() 
        return response.json()
    
    def perform_transition(self, issue_key: str, transition_id: str, 
                          resolution_id: Optional[str] = None,
                          comment: Optional[str] = None,
                          fields: Optional[Dict[str, Any]] = None) -> bool:
        """ 
        Documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-transitions-post
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        
  
        payload = {
            "transition": {
                "id": transition_id
            }
        }
        
        if resolution_id:
            if not fields:
                fields = {}
            fields["resolution"] = {"id": resolution_id}
            
        if fields:
            payload["fields"] = fields
            
        if comment:
            payload["update"] = {
                "comment": [
                    {
                        "add": {
                            "body": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": comment
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        
        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            auth=self.auth
        )
        
        response.raise_for_status()  
        return True
        
    def get_board_issues(self, board_id: int, jql: Optional[str] = None, 
                         start_at: int = 0, max_results: int = 50) -> Dict:
        """
        Documentation: https://developer.atlassian.com/cloud/jira/software/rest/api-group-board/#api-rest-agile-1-0-board-boardid-issue-get
        """
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/issue"
        
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if jql:
            params["jql"] = jql
            
        response = requests.get(
            url,
            params=params,
            headers=self.headers,
            auth=self.auth
        )
        
        response.raise_for_status()
        return response.json()
    
    def transition_board_issues(self, board_id: int, transition_id: str, 
                               jql: Optional[str] = None) -> Dict[str, Union[int, List[str]]]:

        all_issues = []
        start_at = 0
        max_results = 100
        total = None
        
        while total is None or start_at < total:
            response = self.get_board_issues(
                board_id, 
                jql=jql, 
                start_at=start_at, 
                max_results=max_results
            )
            
            issues = response.get('issues', [])
            all_issues.extend(issues)
            
            if total is None:
                total = response.get('total', 0)
                
            start_at += len(issues)
            
            if len(issues) < max_results:
                break
        
        results = {
            "total": len(all_issues),
            "successful": 0,
            "failed": 0,
            "failed_issues": []
        }
        
        for issue in all_issues:
            issue_key = issue.get('key')
            try:
                self.perform_transition(issue_key, transition_id)
                results["successful"] += 1
            except Exception as e:
                results["failed"] += 1
                results["failed_issues"].append(f"{issue_key}: {str(e)}")
                
        return results
    
    def get_user_account_id(self, email: str) -> str:
        """
        Documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-search-get
        """
        url = f"{self.base_url}/rest/api/3/user/search"
        
        params = {
            "query": email
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
            raise ValueError(f"No user found with email: {email}")
            
        return users[0]["accountId"]


if __name__ == "__main__":
    jira = JiraAPI(
        base_url=os.getenv("JIRA_BASE_URL"),
        email=os.getenv("JIRA_EMAIL"),
        api_token=os.getenv("VINIT_API_TOKEN"),
    )
    # TO get available transition
    issue_key = "SP-2"
    transition_id = "21"
    board_id = "SP"    
    transitions = jira.get_available_transitions(issue_key)
    print(f"::: Available transitions for {issue_key}:")
    for transition in transitions.get('transitions', []):
        print(f"  - {transition['name']} (ID: {transition['id']})")

    success = jira.perform_transition(
        issue_key=issue_key,
        transition_id=transition_id,
        comment="Moving to In Progress via API"
    )
    

    results = jira.transition_board_issues(
        board_id=board_id,
        transition_id=transition_id,
        jql="project = PROJ AND status = 'To Do'"  
    )
    