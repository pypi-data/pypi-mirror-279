import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator, Dict, List, Optional

import pandas as pd

from kelvin.message import AssetDataMessage, Message


def round_timestamp(dt: datetime, delta: timedelta) -> datetime:
    """
    Round a datetime object to the nearest interval specified by delta.

    Parameters:
        dt (datetime): The datetime object to round.
        delta (timedelta): The rounding interval.

    Returns:
        datetime: The rounded datetime object.
    """
    # Convert the delta to total seconds for rounding
    delta_seconds = delta.total_seconds()

    # Round the timestamp's seconds down to the nearest interval
    rounded_seconds = (dt.timestamp() // delta_seconds) * delta_seconds

    # Convert the rounded seconds back to a datetime object
    # Preserving the timezone information if present
    if dt.tzinfo is not None:
        return datetime.fromtimestamp(rounded_seconds, tz=dt.tzinfo)
    else:
        return datetime.fromtimestamp(rounded_seconds)


class RollingWindow:
    """
    A class to manage rolling windows of data for multiple assets.
    """

    def __init__(
        self,
        datastreams: List[str],
        max_data_points: Optional[int] = None,
        max_window_duration: Optional[float] = None,
        timestamp_rounding_interval: Optional[timedelta] = None,
        stream_filter: Optional[AsyncGenerator[Message, None]] = None,
    ):
        """
        Constructs all the necessary attributes for the RollingWindow object.

        Args:
            datastreams (List[str]): A list of datastream names to be used as columns in each Asset DataFrame.
            max_data_points (Optional[int]): The maximum number of entries to keep in each Asset DataFrame.
            max_window_duration (Optional[float]): The maximum duration (in seconds) of the window for each
            Asset DataFrame.
            timestamp_rounding_interval (Optional[timedelta]): Specifies the interval to which timestamps should be
            rounded. This helps ensure data alignment when timestamps may arrive out of sync.
            stream_filter (Optional[AsyncGenerator[Message, None]]): If provided, a async task is created to consume
            messages from the stream_filter and append them to the rolling window.
        """
        self.asset_dfs: Dict[str, pd.DataFrame] = {}
        self.datastreams = datastreams
        self.max_data_points = max_data_points
        self.max_window_duration = max_window_duration
        self.timestamp_rounding_interval = timestamp_rounding_interval
        self.stream_filter = stream_filter

        if self.stream_filter is not None:
            self._consumer_task = asyncio.create_task(self._consume_stream())

    async def _consume_stream(self) -> None:
        async for message in self.stream_filter:  # type: ignore
            self.append(message)

    def append(self, message: Message) -> None:
        """
        Appends a new message to the rolling window DataFrame for the corresponding asset.

        Args:
            message (Message): The message containing data to be added to the rolling window.
        """
        if not isinstance(message, AssetDataMessage):
            return

        # Extract required information from the message
        asset = message.resource.asset
        datastream = message.resource.data_stream
        value = message.payload
        timestamp = message.timestamp

        # Round the timestamp if a timestamp_rounding_interval interval was specified
        if self.timestamp_rounding_interval is not None:
            timestamp = round_timestamp(timestamp, self.timestamp_rounding_interval)

        # Check if asset DataFrame exists, if not, create it with timestamp as index
        df = self.get_asset_df(asset)

        # If the timestamp already exists, update the value, otherwise append a new row
        df.loc[timestamp, datastream] = value

        # Ensure the DataFrame is sorted by timestamp
        df.sort_index(inplace=True)

        # Enforce window size constraint
        if self.max_data_points is not None and self.max_data_points > 0 and len(df) > self.max_data_points:
            # Remove the oldest entry to maintain the size constraint
            df.drop(df.index[0], inplace=True)

        # Enforce time window constraint
        if self.max_window_duration is not None and self.max_window_duration > 0:
            # Calculate the cutoff time
            cutoff_time = df.index[-1] - timedelta(seconds=self.max_window_duration)
            # Keep rows that are within the time window
            df = df[df.index >= cutoff_time]

        self.asset_dfs[asset] = df

    def get_asset_df(self, asset: str) -> pd.DataFrame:
        """
        Retrieve the rolling window DataFrame for a given asset.

        Args:
            asset (str): The asset identifier for which the DataFrame is required.

        Returns:
            pd.DataFrame: The DataFrame associated with the given asset.
        """

        df = self.asset_dfs.get(asset)

        if df is None:
            df = pd.DataFrame(columns=self.datastreams)
            df.index.name = "timestamp"

        return df

    def get_assets_dfs(self) -> Dict[str, pd.DataFrame]:
        """
        Retrieve all stored rolling window DataFrames.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary containing all the DataFrames.
        """
        return self.asset_dfs
