import requests, json
from datetime import datetime
from notion_credentials import *

# token = add your token found in Notion
#
# databaseId = add database created in Notion

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

now = datetime.now().astimezone().isoformat()


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request('POST', readUrl, headers=headers)
    data = res.json()
    print(res.status_code)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


def createPage(description, status):
    create_url = 'https://api.notion.com/v1/pages'

    newData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "Description": {
                "title": [
                    {
                        "text": {
                            "content": description
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                            'start': now,
                            'end': None
                        }
            },
            "Status": {
                "rich_text": [
                    {
                        'text': {
                            'content': status
                        }
                    }
                ]
            },
        }
    }

    data = json.dumps(newData)
    res = requests.request('POST', create_url, headers=headers, data=data)
    print(res.status_code)
    return res



def get_page_id(n):

    with open('db.json') as json_file:
        page_id_dict = json.load(json_file)

    print(page_id_dict.get('results')[n].get('id'))
    return page_id_dict.get('results')[n].get('id')


def updatePage(n, status):
    page_id = get_page_id(n)

    create_url = f'https://api.notion.com/v1/pages/{page_id}'

    newData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "Status": {
                "rich_text": [
                    {
                        'text': {
                            'content': status
                        }
                    }
                ]
            },
        }
    }

    data = json.dumps(newData)

    res = requests.request('PATCH', create_url, headers=headers, data=data)

    print(res.status_code)


def retrieve_objects(page_id):
    url = f'https://api.notion.com/v1/blocks/{page_id}'

    res = requests.request('GET', url, headers=headers)
    data = res.json()
    return data.get('child_page').get('title')