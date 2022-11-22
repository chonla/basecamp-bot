"""Bot

The bot.
"""

import re
from time import sleep
from typing import Callable
import requests
import logging
from datetime import datetime


from . import config, session, graceful_interrupt_handler, hook


class Bot:
    def __init__(self, auth: config.Config, conf: config.Config):
        log_level = conf.get("log_level", "DEBUG")
        logging.basicConfig(level=log_level)

        self._auth = auth
        self._conf = conf
        self._log_level = log_level

        # Pre-evaluations
        self._access_token = auth.get("access_token")
        self._name = conf.get("bot.nick")
        self._useragent = f"{conf.get('bot.name')} ({conf.get('bot.version')})"
        self._poll_interval = conf.get("bot.poll_interval", 5)
        self._identity = conf.get("bot.identity")
        self._trigger = conf.get("bot.trigger", "บอท")
        logging.debug(f"bot identity: {self._identity}")

        resp = self.whoami()
        self._impersonated_id = resp["accounts"][0]["id"]

        self._hooks = {
            hook.Hook.ENTER_CAMPFIRE: [],
            hook.Hook.NEW_MESSAGE: [],
            hook.Hook.EXIT_CAMPFIRE: [],
        }
        self._stats = {"triggered": 0, "messages_sent": 0}
        self._in_campfire = False

    def log_level(self):
        return self._log_level

    def whoami(self):
        url = f"https://launchpad.37signals.com/authorization.json"
        resp = self._get_resource(url)
        return resp

    def name(self):
        return self._name

    def trigger(self):
        return self._trigger

    def print_stats(self):
        logging.info("summary")
        logging.info(f"bot triggered: {self._stats['triggered']}")
        logging.info(f"messages sent by bot: {self._stats['messages_sent']}")

    def add_hook(self, event_key: hook.Hook, callback: Callable):
        if event_key not in self._hooks:
            logging.error(f"hook {event_key} does not support")
            return

        self._hooks[event_key].append(callback)

    def enter_campfire(self, target_campfire_alias: str):
        logging.info(f"entering campfire {target_campfire_alias}")

        target_campfire_project_id = self._conf.get(
            f"campfires.{target_campfire_alias}.project_id"
        )
        target_campfire_chat_id = self._conf.get(
            f"campfires.{target_campfire_alias}.campfire_id"
        )
        url = self._campfire_url(target_campfire_project_id, target_campfire_chat_id)

        store = session.Session(target_campfire_alias)
        last_etag = store.get_value("last-etag", "")
        last_message_timestamp = store.get_value("last-timestamp", 0)
        headers = {}

        with graceful_interrupt_handler.GracefulInterruptHandler() as h:
            while True:
                try:
                    if h.interrupted:
                        logging.info("interruption detected. exiting ...")
                        self._dispatch_hook(
                            hook.Hook.EXIT_CAMPFIRE,
                            {"campfire_alias": target_campfire_alias},
                        )
                        self.print_stats()
                        return

                    if last_etag != "":
                        headers["If-None-Match"] = last_etag
                        headers["If-Modified-Since"] = last_etag
                    resp_json, resp_headers = self._get_resource(
                        url, headers=headers, return_with_headers=True
                    )

                    if not self._in_campfire:
                        self._in_campfire = True
                        self._dispatch_hook(
                            hook.Hook.ENTER_CAMPFIRE,
                            {"campfire_alias": target_campfire_alias},
                        )

                    if resp_headers.get("status_code") == 200:
                        logging.debug("new messages detected ...")

                        messages = list(
                            filter(
                                # get only new messages
                                lambda m: m["created_at"] > last_message_timestamp,
                                filter(
                                    # get only messages from the others
                                    lambda m: m["sender"]["id"] != self._identity,
                                    map(
                                        # get only needed detail
                                        lambda m: {
                                            "id": m["id"],
                                            "message": self._clean_html(m["content"]),
                                            "created_at": datetime.strptime(
                                                m["created_at"],
                                                "%Y-%m-%dT%H:%M:%S.%f%z",
                                            ).timestamp()
                                            * 1000,
                                            "sender": {
                                                "id": m["creator"]["id"],
                                                "name": m["creator"]["name"],
                                            },
                                        },
                                        resp_json,
                                    ),
                                ),
                            )
                        )

                        last_etag = resp_headers.get("ETag")
                        store.set_value("last-etag", last_etag)
                        if len(messages) > 0:
                            last_message_timestamp = messages[0]["created_at"]
                            store.set_value("last-timestamp", last_message_timestamp)

                            new_messages_event_params = {
                                "campfire_alias": target_campfire_alias,
                                "messages": messages,
                            }
                            self._dispatch_hook(
                                hook.Hook.NEW_MESSAGE, new_messages_event_params
                            )
                            self._stats["triggered"] = self._stats["triggered"] + len(
                                messages
                            )

                    elif resp_headers.get("status_code") == 404:
                        logging.error(
                            f"unable to enter the campfire {target_campfire_alias}. campfire may not exist or you have not invited bot to campfire yet."
                        )
                        return
                except requests.JSONDecodeError:
                    pass
                finally:
                    sleep(self._poll_interval)

    def send_message_to_campfire(self, message: str, target_campfire_alias: str):
        target_campfire_project_id = self._conf.get(
            f"campfires.{target_campfire_alias}.project_id"
        )
        target_campfire_chat_id = self._conf.get(
            f"campfires.{target_campfire_alias}.campfire_id"
        )
        url = self._campfire_url(target_campfire_project_id, target_campfire_chat_id)
        data = {"content": message}
        resp = self._post_resource(url, data)
        self._stats["messages_sent"] = self._stats["messages_sent"] + 1
        return resp

    def _campfire_url(self, project_id: str, chat_id: str) -> str:
        return f"https://3.basecampapi.com/{self._impersonated_id}/buckets/{project_id}/chats/{chat_id}/lines.json"

    def _get_resource(
        self, url: str, headers: dict = {}, return_with_headers: bool = False
    ):
        return self._request(
            url, method="get", headers=headers, return_with_headers=return_with_headers
        )

    def _post_resource(
        self,
        url,
        body: dict = {},
        headers: dict = {},
        return_with_headers: bool = False,
    ):
        return self._request(
            url,
            method="post",
            body=body,
            headers=headers,
            return_with_headers=return_with_headers,
        )

    def _request(
        self,
        url: str,
        method: str = "post",
        body: dict = {},
        headers: dict = {},
        return_with_headers: bool = False,
    ):
        extended_headers = dict(
            {
                "User-Agent": self._useragent,
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json",
            },
            **headers,
        )

        if method == "post":
            resp = requests.post(url, headers=extended_headers, json=body)
        elif method == "get":
            resp = requests.get(url, headers=extended_headers)
        if return_with_headers:
            return resp.json(), dict(resp.headers, **{"status_code": resp.status_code})
        return resp.json()

    def _clean_html(self, html_text: str) -> str:
        regex = re.compile(r"<[^>]+>")
        return regex.sub("", html_text)

    def _dispatch_hook(self, event_key: hook.Hook, params: any):
        if event_key not in self._hooks:
            logging.error(f"hook {event_key} does not support")
            return

        for hook in self._hooks[event_key]:
            hook(self, params)
