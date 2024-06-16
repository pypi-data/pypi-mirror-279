import os
import asyncio
import logging
from fedora_messaging import config as fmc
from anitya_schema.project_messages import ProjectVersionUpdatedV2
from telegram import Bot
from telegram.constants import ParseMode


class ProjectConfig:
    _data: dict

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return str(self._data)

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def allow_nonstable(self) -> bool:
        return self._data.get("allow_nonstable", False)

    @property
    def versions(self) -> list[str]:
        return self._data.get("versions", None)

    def is_in_versions(self, ver: str) -> bool:
        for filter in self.versions:
            if ver.startswith(filter):
                return True
        return False


class TelegramForwardConsumer:

    _log: logging.Logger
    _bot: Bot
    _chat_ids: list[str]
    _projects: list[ProjectConfig] = None

    def __init__(self) -> None:
        self._log = logging.getLogger(self.__class__.__name__)
        config = fmc.conf["consumer_config"]

        api_key = os.getenv("ANITYA_TG_BOT_KEY")
        if api_key:
            self._log.info("Got Bot API key from environment")
        else:
            api_key = config["api_key"]
            self._log.info("Got Bot API key from config")
        self._bot = Bot(api_key)

        chat_ids = os.getenv("ANITYA_TG_CHAT_IDS")
        if chat_ids:
            self._chat_ids = chat_ids.split(",")
            self._log.info("Got chat IDs from environment: %s", self._chat_ids)
        else:
            self._chat_ids = config["chat_ids"]
            self._log.info("Got chat IDs from config: %s", self._chat_ids)

        projects = config.get("projects")
        if projects:
            self._log.info("Got watched projects: %s", projects)
            self._projects = [ProjectConfig(p) for p in projects]

    async def __call__(self, event: ProjectVersionUpdatedV2):
        return await self.consume(event)

    async def consume(self, event: ProjectVersionUpdatedV2):
        if not self._projects:
            message = self._get_message(event.upstream_versions, event.project_name, event.project_homepage)
            self._log.info(message)
            return await self.send_message_to_chats(self._chat_ids, message)

        project = self._find_project(event.project_id)
        if not project:
            self._log.debug("An event is filtered by project ID: %s", event)
            return

        versions = (event.upstream_versions if project.allow_nonstable
                    else set(event.upstream_versions).intersection(event.stable_versions))
        if not versions:
            self._log.debug("An event is filtered by versions stability: %s", event)
            return

        versions = (versions if not project.versions
                    else [ver for ver in versions if project.is_in_versions(ver)])
        if not versions:
            self._log.debug("An event is filtered by versions: %s", event)
            return

        message = self._get_message(versions, event.project_name, event.project_homepage)
        self._log.info(message)
        return await self.send_message_to_chats(self._chat_ids, message)

    async def send_message_to_chats(self, chats: list[str], msg: str):
        sending_tasks = [asyncio.create_task(self.send_message_to_chat(chat, msg))
                         for chat in chats]
        return await asyncio.wait(sending_tasks)

    async def send_message_to_chat(self, chat: str, msg):
        self._log.debug("Sending message to a chat %s", chat)
        return await self._bot.send_message(chat, msg, ParseMode.MARKDOWN, disable_web_page_preview=True)

    def _find_project(self, id: int) -> ProjectConfig:
        for proj in self._projects:
            if id == proj.id:
                return proj

    def _get_message(self, versions: list[str], project_name: str, project_homepage: str) -> str:
        return f"[{project_name}]({project_homepage}): the new versions {versions} were found"
