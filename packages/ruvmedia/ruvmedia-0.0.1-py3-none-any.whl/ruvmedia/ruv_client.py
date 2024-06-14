from __future__ import annotations

from dataclasses import dataclass

import aiohttp

from .live_streams import get_channels
from .gql_client import RuvGQLClient
from .models import Media
from .const import LOGGER


@dataclass
class RUVClient:
    user_agent: str

    request_timeout: float = 8.0
    session: aiohttp.client.ClientSession | None = None
    gq_client: RuvGQLClient | None = None

    def __post_init__(self):
        if self.gq_client is None:
            # self.gq_client = RuvGQLClient(self.session, self.user_agent)
            self.gq_client = RuvGQLClient()

    async def async_get_data(self):
        pass

    async def async_get_live_channels(self) -> list[Media]:
        channels = await get_channels(self.session)
        # return [Media(**channel) for channel in channels]
        return [
            Media(
                name=channel["name"],
                url=channel["url"],
                identifier=channel["identifier"],
            )
            for channel in channels
        ]

    async def async_get_categories(self, category: str | None) -> list[Media]:
        LOGGER.debug("Category: %s", category)
        if category:
            # categories = await self.gq_client.get_category(category)
            items = await self.gq_client.get_category(category)
            return [
                Media(
                    name=item["title"],
                    url=item["slug"],
                    identifier=f"program.{item['programID']}",
                )
                for item in items["categories"][0]["programs"]
            ]
        else:
            categories = await self.gq_client.get_categories()
            # return [Media(**channel) for channel in channels]
            return [
                Media(
                    name=category["title"],
                    url=category["slug"],
                    identifier=f"category.{category['slug']}",
                )
                for category in categories["categories"]
            ]

    async def async_get_programs(self, program_id: str) -> list[Media]:
        LOGGER.debug("Program: %s", program_id)
        # categories = await self.gq_client.get_category(category)
        episodes = await self.gq_client.get_program(program_id)
        return [
            Media(
                name=item["title"],
                url=item["id"],
                identifier=f"program.{program_id}.{item['id']}",
            )
            for item in episodes["episodes"]
        ]

    async def media(self, identifier: str) -> Media:
        LOGGER.debug("Media: %s", identifier)
        prefix, _, id = identifier.partition(".")
        if prefix == "channel":
            channels = await get_channels(self.session)
            for channel in channels:
                if channel["identifier"] == identifier:
                    return Media(
                        name=channel["name"],
                        url=channel["url"],
                        identifier=channel["slug"],
                    )
        if prefix == "program":
            program_id, _, episode_id = id.partition(".")
            episodes = await self.gq_client.get_episode(program_id, episode_id)
            for episode in episodes["episodes"]:
                if episode["id"] == episode_id:
                    return Media(
                        name=episode["title"],
                        url=episode["file"],
                        identifier=episode["id"],
                    )

        return None
