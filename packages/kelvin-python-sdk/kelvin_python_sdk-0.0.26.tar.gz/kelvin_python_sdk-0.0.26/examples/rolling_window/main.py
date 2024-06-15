import asyncio
from datetime import timedelta
from kelvin.application import KelvinApp, filters
from kelvin.ai import RollingWindow


async def check_window(window: RollingWindow):
    print("Checking window task")
    while True:
        print(window.get_assets_dfs())
        await asyncio.sleep(10)


async def main() -> None:
    app = KelvinApp()
    await app.connect()
    print("App connected successfully")

    # Subscribe to the asset data streams
    stream = app.stream_filter(filters.is_asset_data_message)

    # Create a rolling window
    rolling_window = RollingWindow(
        datastreams=[i.name for i in app.inputs],  # App inputs
        max_window_duration=300,  # max of 5 minutes of data
        max_data_points=10,  # max of 10 data points
        timestamp_rounding_interval=timedelta(seconds=1),  # round to the nearest 30 seconds
        stream_filter=stream,
    )

    await asyncio.gather(
        check_window(rolling_window),
    )


if __name__ == "__main__":
    asyncio.run(main())
