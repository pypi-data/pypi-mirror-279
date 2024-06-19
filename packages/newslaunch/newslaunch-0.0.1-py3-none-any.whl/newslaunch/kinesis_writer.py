from __future__ import annotations

import json
import uuid

import boto3


class KinesisWriterError(Exception):
    """Custom exception class for KinesisWriter errors."""


class KinesisWriter:
    """Helper class for writing data to an AWS Kinesis stream.

    Args:
        stream_name (str): The name of the Kinesis stream.
        region_name (str, optional): If not provided, the default region from the boto3 session will be used.
        aws_access_key_id (str, optional): The AWS access key ID for authentication.
        aws_secret_access_key (str, optional): The AWS secret access key for authentication.
        If not provided, the default aws credential resolution chain will be used.

    Raises:
        KinesisWriterError: If stream_name parameter is not provided.
    """

    def __init__(
        self,
        stream_name: str,
        region_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
    ):
        if not stream_name:
            raise KinesisWriterError("Stream_name parameter is required.")

        self.stream_name = stream_name
        self.region_name = region_name or boto3.Session().region_name

        if aws_access_key_id and aws_secret_access_key:
            self.session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
        else:
            self.session = boto3.Session()

        self.client = self.session.client("kinesis", region_name=self.region_name)

    def send_to_stream(
        self,
        data,
        partition_key: str | None = None,
        record_per_entry: bool = False,
    ) -> dict:
        """Send data to Kinesis stream.

        Args:
            data: Data to send to the stream. Can be a single item or a list of items.
            partition_key (str, optional): Partition key to use. Defaults to random UUID.
            record_per_entry (bool, optional): Flag to determine whether to use put_record or put_records.
                Defaults to False (use put_record) whereby the contents of data are sent as a single record.

        Returns:
            (dict): The response from the Kinesis API call.
        """
        # TODO: retries if response['FailedRecordCount'] > 0?
        if record_per_entry:
            return self._send_batch_put_records(data, partition_key)
        else:
            return self._send_single_put_record(data, partition_key)

    def _send_batch_put_records(self, data, partition_key: str | None) -> dict:
        """Send a batch of data to the Kinesis stream using put_records.

        Args:
            data: List of data items to send to the stream as a batch.
                Can be a list of JSON-serializable items, a list of strings, or a list of bytes data.
            partition_key (str, optional): Partition key to use. Defaults to random UUID.

        Returns:
            (dict): The response from the Kinesis put_records API call.

        Raises:
            KinesisWriterError:
                If data is not a list.
                If the number of records or total size exceeds the limits.
        """
        if not isinstance(data, list):
            raise KinesisWriterError(
                "Data must be a list of values when using 'put_records' mode."
            )

        # TODO: split into chunks if > 500
        if len(data) > 500:
            raise KinesisWriterError(
                "The number of records exceeds the 500 record limit for put_records."
            )

        records = []
        for item in data:
            if isinstance(item, bytes):
                record_data = item
            elif isinstance(item, str):
                record_data = item.encode("utf-8")
            else:
                record_data = json.dumps(item).encode("utf-8")

            # If partition key is not provided, generate a random one for each
            # record for equal shard distribution.
            part_key = partition_key if partition_key is not None else str(uuid.uuid4())
            records.append({"Data": record_data, "PartitionKey": part_key})

        if (
            sum(len(rec["Data"]) + len(rec["PartitionKey"]) for rec in records)
            > 5 * 1024 * 1024
        ):
            raise KinesisWriterError(
                "The total size of records exceeds the 5MiB limit for a single put_records."
            )
        return self.client.put_records(StreamName=self.stream_name, Records=records)

    def _send_single_put_record(self, data, partition_key: str | None) -> dict:
        """Send a single data record to the Kinesis stream using put_record.

        Args:
            Data to send to the stream. Can be a JSON-serializable data or bytes data.
            partition_key (str, optional): Partition key to use. Defaults to random UUID.

        Returns:
            (dict): The response from the Kinesis put_record API call.

        Raises:
            KinesisWriterError: If the data size exceeds the limit.
        """
        if partition_key is None:
            partition_key = str(uuid.uuid4())

        if isinstance(data, str):
            data = data.encode("utf-8")
        elif isinstance(data, bytes):
            pass
        else:
            data = json.dumps(data).encode("utf-8")

        if len(data) + len(partition_key.encode("utf-8")) > 1024 * 1024:
            raise KinesisWriterError(
                "The size of the data exceeds the 1MiB limit for a single put_record call."
            )

        return self.client.put_record(
            StreamName=self.stream_name,
            Data=data,
            PartitionKey=partition_key,
        )
