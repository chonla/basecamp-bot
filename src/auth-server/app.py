import sys
from time import sleep
from flask import Flask, request
import requests
import yaml
from ..bc3bot import config

conf = config.Config('./bot.yaml')

app = Flask(__name__)

@app.route("/")
def login():
    url = f"https://launchpad.37signals.com/authorization/new?type=web_server&client_id={conf.get('bot.client_id')}&redirect_uri={conf.get('bot.redirect_uri')}"
    return f"""
    <html>
    <head>
    <title>{conf.get('bot.name')} authorization</title>
    <style type="text/css">
    body {{ font-size: 14pt; }}
    </style>
    </head>
    <body><a href="{url}">Click here to authorize</a> on behalf of bot <strong>{conf.get('bot.name')}</strong>.</body>
    </html>
    """

@app.route("/auth", methods=['GET'])
def do_auth():
    args = request.args
    verification_code = args.get('code')
    url = f"https://launchpad.37signals.com/authorization/token?type=web_server&client_id={conf.get('bot.client_id')}&redirect_uri={conf.get('bot.redirect_uri')}&client_secret={conf.get('bot.client_secret')}&code={verification_code}"
    headers = {
        "User-Agent": f"{conf.get('bot.name')} ({conf.get('bot.version')})"
    }

    resp = requests.post(url=url, headers=headers)
    resp_json = resp.json()

    access_token = resp_json.get('access_token')
    refresh_token = resp_json.get('refresh_token')

    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    with open(".botrc", "w") as f:
        yaml.safe_dump(tokens, f)

    return f"""
    <html>
    <head>
    <title>{conf.get('bot.name')} authorization</title>
    <style type="text/css">
    body {{ font-size: 14pt; }}
    .inline-code {{ padding: 4px; border: 1px solid; }}
    </style>
    </head>
    <body>You have been authorized on behalf of bot <strong>{conf.get('bot.name')}</strong>. You may close this window and run <span class="inline-code">bot run</span> to start the bot.</body>
    </html>
    """
