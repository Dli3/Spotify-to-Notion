import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class Notion():
    '''
    Create, update, and read the specified Notion DB through the Notion API.
    
    Docs:
        - https://developers.notion.com/
    '''
    def __init__(self) -> None:
        # Notion's Integration Token 
        self.token = os.getenv('INTERNAL_INTEGRATION_TOKEN')
        
        # The page/DB ID
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        
        # The Notion-Version is subject to change
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Notion-Version": "2021-05-13",
            "Content-Type": "application/json"
        }

    
    def read_database(self):
        url = f'https://api.notion.com/v1/databases/{self.database_id}/query'

        response = requests.post(url, headers=self.headers)

        response_json = response.json()

        assert response.status_code == 200

        with open('./data/db.json', 'w', encoding='utf8') as f:
            json.dump(response_json,f, ensure_ascii=False)
        print(f"Database {self.database_id}'s content': {response_json}")
        return response_json

    def create_page(self, song_title, author):
        url = 'https://api.notion.com/v1/pages'

        new_page_data = {
                "parent": { "database_id": self.database_id},
                "properties": {
                    "Title": {
                        "title": [
                            {
                                "text": {
                                    "content": song_title
                                }
                            }
                        ]
                    },
                "Author": {
                    "rich_text": [
                        {
                            "text": {
                                "content": author
                            }
                        }
                    ]
                },
            }
        }

        data = json.dumps(new_page_data)

        response = requests.post(url, headers=self.headers, data=data)
        assert response.status_code == 200
        
        response_json = json.loads(response.text)
        print("Created a new page: " + response_json['id'])
        return response_json

    def update_page(self, page_id, song_title, author):
        url = f'https://api.notion.com/v1/pages/{page_id}'

        update_data = {
            "properties": {
                 "Title": {
                        "title": [
                            {
                                "text": {
                                    "content": song_title
                                }
                            }
                        ]
                    },
                "Author": {
                    "rich_text": [
                        {
                            "text": {
                                "content": author
                            }
                        }
                    ]
                },
            }
        }

        data = json.dumps(update_data)
        response = requests.patch(url, headers=self.headers, data=data)
        assert response.status_code == 200

        response_json = json.loads(response.text)
        print('Updated page: ' + response_json['id'])
        return response_json['id']

