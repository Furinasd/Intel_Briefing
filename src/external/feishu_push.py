# src/external/feishu_push.py
import requests
import json

def push_to_feishu(webhook_url, report_markdown):
    headers = {"Content-Type": "application/json"}
    payload = {
        "msg_type": "interactive", # 使用卡片消息更漂亮
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "👑 COO 每日财富简报"},
                "template": "blue"
            },
            "elements": [
                {"tag": "markdown", "content": report_markdown}
            ]
        }
    }
    requests.post(webhook_url, headers=headers, data=json.dumps(payload))