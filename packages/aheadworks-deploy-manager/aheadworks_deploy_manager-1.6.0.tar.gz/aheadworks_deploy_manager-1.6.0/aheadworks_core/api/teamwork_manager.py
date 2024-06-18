import os
import requests

class TeamworkManager:
    base = ''
    api_base = ''
    token = ''

    def __init__(self, cloud, token):
        self.base = f"https://{cloud}.teamwork.com/"
        self.token = token

    def get_issue_url(self, id):
        return f"{self.base}app/tasks/{id}"

    def find_tasks_by_tags(self, tags):
        str_tags = ",".join(tags)
        url = self.base + f"projects/api/v3/tasks.json?tags={str_tags}&includeCompletedTasks=true"
        response = requests.get(url, auth=(self.token, ''))
        return response.json()['tasks']

    def close_issue(self, task_id):
        url = self.base + f"/tasks/{task_id}.json"
        payload = {
            'todo-item': {
                'completed': True
            }
        }
        response = requests.put(url, auth=(self.token, ''), json=payload)

    def reassign(self, task_id, assign_to):
        url = self.base + f"projects/api/v3/tasks/{task_id}.json"
        payload = {
                "task": {
                    "assignees" :{
                    "userIds" : [assign_to]
                    }
                }
            }
        response = requests.patch(url, auth=(self.token, ''), json=payload)

    def add_comment(self, task_id, text):
        url = self.base + f"tasks/{task_id}/comments.json"
        payload = {
            "comment": {
                "body": text,
                "notify": True
            }
        }
        response = requests.post(url, auth=(self.token, ''), json=payload)

    def add_attachments_to_task(self, task_id, file_names):
        for file_path in file_names:
            # Get a presigned url
            file_name = os.path.basename(file_path)
            file_size = os.stat(file_path)
            url = self.base + f"/projects/api/v1/pendingfiles/presignedurl.json?fileName={file_name}&fileSize={file_size}"
            response = requests.get(url, auth=(self.token, ''))

            ref = response.json()['ref']
            upload_url = response.json()['url']

            # Upload a file to presigned url
            with open(file_path, 'rb') as file:
                files = {'file': (file_path, file)}
                headers = {
                    "X-Amz-Acl": "public-read"
                }
                response = requests.put(
                    upload_url,
                    headers = headers,
                    files=files
                )
        
            # attach the uploaded file to the task
            url = self.base + f"/projects/api/v3/tasks/{task_id}.json"
            payload = {
                "attachments": 
                {
                    "pendingFiles": 
                        [{
                            "reference" :ref 
                        }]
                }
            }
            response = requests.patch(url, auth=(self.token, ''), json=payload)
