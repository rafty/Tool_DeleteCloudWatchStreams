# -*- coding: utf-8 -*-
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logs = boto3.client('logs')

STREAM_NAME_PREFIX = '2020/02/'


def delete_stream(stream, log_stream_name):
    logger.info('stream: {}'.format(stream))
    if stream.get('logStreamName').startswith(STREAM_NAME_PREFIX):
        logger.info('delete streamName: {}'.format(stream.get('logStreamName')))
        delete_response = logs.delete_log_stream(
            logGroupName=log_stream_name,
            logStreamName=stream['logStreamName']
        )
        logger.info('delete response: {}'.format(delete_response))
    else:
        logger.info('???: {}: {}'.format(stream.get('logStreamName'), stream.get('logStreamName').startswith(STREAM_NAME_PREFIX)))

    return stream

# これを実装する
# https://github.com/mihai011/Darkstorm/blob/0fe419d8c196cdc244a5b28ce50e1e6019355322/delete_log_groups.py


def lambda_handler(event, context):
    logger.info('lambda_handler(event): {}'.format(event))

    next_token = None
    log_groups = logs.describe_log_groups()

    for log_group in log_groups.get('logGroups'):
        log_group_name = log_group.get('logGroupName')
        logger.info('delete log group: {}'.format(log_group_name))

        while True:
            if next_token:
                log_streams = logs.describe_log_streams(
                    logGroupName=log_group_name,
                    nextToken=next_token
                )
            else:
                log_streams = logs.describe_log_streams(
                    logGroupName=log_group_name,
                )

            map(lambda x: delete_stream(x, log_group_name),
                log_streams.get('logStreams'))

            if not next_token or len(log_streams.get('logStreams')):
                break
