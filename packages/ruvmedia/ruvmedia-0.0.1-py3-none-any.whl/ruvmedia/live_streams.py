from __future__ import annotations

import json
import aiohttp

from .const import LIVE_CHANNELS, LOGGER

CHANNEL_BASE_URL = "https://geo.spilari.ruv.is/channel/"


async def get_channels(session: aiohttp.client.ClientSession) -> list[{}]:
    results = []
    for channel in LIVE_CHANNELS:
        url = CHANNEL_BASE_URL + channel["slug"]
        response = await session.request(
            "GET", url, headers={"Accept": "application/json"}
        )
        if response.status == 200:
            data = json.loads(await response.text())
            # If the channel has a switcher for different resolution/bitrates, use that instead of the url
            # if 'switcher' in data:
            #     url = data['switcher']
            # else:
            url = data["url"]
            results.append(
                {**channel, "url": url, "identifier": f'channel.{channel["slug"]}'}
            )
        else:
            LOGGER.error(
                f"Error getting channel {channel['name']}: {response.status} {await response.text()}"
            )

    return results
