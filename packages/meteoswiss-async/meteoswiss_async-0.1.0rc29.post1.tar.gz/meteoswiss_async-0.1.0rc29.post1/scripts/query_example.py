import asyncio

from rich import console
from meteoswiss_async import MeteoSwissClient


async def main():
    term = console.Console()
    client = await MeteoSwissClient.with_session()

    async with client:
        resp = await client.get_station_information(station_code="KLO")
        term.print(resp)

        resp = await client.get_weather(postal_code="8152")
        term.print(resp)

        resp = await client.get_current_weather(station_code="KLO")
        term.print(resp)

        resp = await client.get_webcam_previews()
        term.print(resp.stations[:2])
        # resp = await client.get_station_information(station_code="KLO")
        # print(resp)

        # resp = await client.get_full_overview(
        #     postal_code=["8152", "8001"], station_code=["KLO"]
        # )
        # print(resp)

        # stations = await client.get_stations()
        # print(stations)


if __name__ == "__main__":
    asyncio.run(main())
