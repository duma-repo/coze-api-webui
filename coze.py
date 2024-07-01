import json

import requests

url = 'https://api.coze.com/open_api/v2/chat'
headers = {
    'Authorization': 'Bearer <扣子token>',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': 'api.coze.com',
    'Connection': 'keep-alive'
}

data = {
    "conversation_id": "123",
    "bot_id": "<Bot ID>",
    "user": "<用户id>",
    "query": "我刚刚问的是什么",
    "stream": True
}


def chat(query, history):
    chat_history = []
    for hist_item in history:
        chat_history.append({'role': 'user', 'type': 'query', 'content': hist_item[0], "content_type": "text"})
        chat_history.append({'role': 'assistant', 'type': 'answer', 'content': hist_item[1], "content_type": "text"})


    data['query'] = query
    data['chat_history'] = chat_history

    response = requests.post(url, headers=headers, json=data)

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_data = json.loads(decoded_line.split("data:")[-1])

            if json_data['event'] == 'done':
                break
            else:
                if json_data['message']['type'] == 'answer':
                    yield json_data['message']['content']