# -*- coding: utf-8 -*-
import os
import datetime
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logs = boto3.client('logs')


def delete_stream(log_stream_name, log_group_name):
    logger.info('delete_stream: {}'.format(log_stream_name))
    logs.delete_log_stream(logGroupName=log_group_name,
                           logStreamName=log_stream_name)
    return log_stream_name


def extract_streams_to_delete(log_streams):
    # datetime to unixtime and to milliseconds
    three_days_ago = int((datetime.datetime.utcnow() -
                          datetime.timedelta(days=3)).timestamp()*1000)
    now = int(datetime.datetime.utcnow().timestamp()*1000)

    streams_to_delete = [
        stream.get('logStreamName')
        for stream in log_streams.get('logStreams')
        if stream.get('lastEventTimestamp', now) <= three_days_ago]

    logger.info('streams_to_delete: {}'.format(streams_to_delete))
    return streams_to_delete


def describe_log_streams(log_group_name, next_token):
    if next_token:
        log_streams = logs.describe_log_streams(
            logGroupName=log_group_name,
            nextToken=next_token
        )
    else:
        log_streams = logs.describe_log_streams(
            logGroupName=log_group_name,
        )
    return log_streams


def lambda_handler(event, context):
    logger.info('lambda_handler(event): {}'.format(event))

    log_groups = logs.describe_log_groups()

    for log_group in log_groups.get('logGroups'):
        log_group_name = log_group.get('logGroupName')

        if log_group['storedBytes'] == 0:
            logs.delete_log_group(logGroupName=log_group_name)
            logger.info('delete log group: {}'.format(log_group_name))
            continue

        next_token = None
        while True:
            log_streams = describe_log_streams(log_group_name, next_token)
            next_token = log_streams.get('nextToken', None)

            streams_to_delete = extract_streams_to_delete(log_streams)

            list(map(lambda x: delete_stream(x, log_group_name),
                     streams_to_delete))

            if not next_token or len(log_streams.get('logStreams')):
                break
