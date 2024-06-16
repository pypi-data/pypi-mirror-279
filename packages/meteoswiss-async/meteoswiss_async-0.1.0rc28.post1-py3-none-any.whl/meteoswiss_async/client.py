"""API Client code"""

from __future__ import annotations

import csv
import io
from typing import Self

import aiohttp
import asyncstdlib

from . import model

__all__ = [
    "MeteoSwissClient",
]

_METEOSWISS_API_URL = "https://app-prod-ws.meteoswiss-app.ch/v1/"
_STATIONS_INFORMATION_URL = "https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/ch.meteoschweiz.messnetz-automatisch_en.csv"
_PREVIEW_IMAGES = "https://s3-eu-central-1.amazonaws.com/app-prod-static-fra.meteoswiss-app.ch/v1/webcam_overview.json"


# TODO: pollen sensor


class MeteoSwissClient:
    """Async client for your API.

    TODO: describe what the client does.
    """

    def __init__(self, *, session: aiohttp.ClientSession):
        self._session = session

    @classmethod
    async def with_session(cls, **kwargs) -> Self:
        session = aiohttp.ClientSession()
        return cls(session=session, **kwargs)

    async def __aenter__(self) -> "MeteoSwissClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def close(self) -> None:
        return await self._session.close()

    async def get_weather(self, *, postal_code: str) -> model.Weather:
        async with self._session.get(
            _METEOSWISS_API_URL + "plzDetail",
            params={"plz": f"{postal_code}00"},
        ) as response:
            return model.Weather.from_dict(await response.json())

    @asyncstdlib.cache
    async def get_stations(self) -> list[model.Station]:
        async with self._session.get(_STATIONS_INFORMATION_URL) as response:
            content = await response.read()
        stream = io.StringIO(content.decode(encoding="latin_1"))

        reader = csv.DictReader(stream, delimiter=";")
        stations: list[model.Station] = []
        for row in reader:
            # Skip footer rows.
            if row["Link"] is None:
                continue
            # Handle better missing data.
            for k in row:
                if row[k] == "":
                    row[k] = None
            # Split this field into a list.
            row["Measurements"] = row["Measurements"].split(", ")
            stations.append(model.Station.from_dict(row))
        return stations

    async def get_station_information(
        self, *, station_code: str
    ) -> model.StationInformation:
        async with self._session.get(
            _METEOSWISS_API_URL + "stationOverview",
            params={"station": station_code},
        ) as response:
            json_response = await response.json()
        return model.StationInformation.from_dict(
            json_response.get(station_code)
        )

    async def get_current_weather(
        self, *, station_code: str
    ) -> model.StationInformation:
        async with self._session.get(
            _METEOSWISS_API_URL + "currentweather",
            params={"ws": station_code},
        ) as response:
            return model.StationInformation.from_dict(await response.json())

    async def get_full_overview(
        self, *, postal_code: list[str], station_code: list[str]
    ) -> model.FullOverview:
        async with self._session.get(
            _METEOSWISS_API_URL + "vorortdetail",
            params={
                "plz": [f"{pc}00" for pc in postal_code],
                "ws": station_code,
            },
        ) as response:
            return model.FullOverview.from_dict(await response.json())

    async def get_webcam_previews(self) -> model.WebcamPreviews:
        async with self._session.get(_PREVIEW_IMAGES) as response:
            return model.WebcamPreviews.from_dict(await response.json())
