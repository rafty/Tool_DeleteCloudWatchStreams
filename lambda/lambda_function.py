# -*- coding: utf-8 -*-
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logs = boto3.client('logs')
LOGS_GROUP_NAME = '/aws/lambda/serverlessrepo-Datadog-Log-For-' \
                  'loglambdaddfunction-1379AY0BANFA7'
STREAM_NAME_PREFIX = '2020/03/'


# environment variable
# LOGS_GROUP_NAME = os.environ['LOGS_GROUP_NAME']
# STREAM_NAME_PREFIX = os.environ['STREAM_NAME_PREFIX']


def delete_stream(stream):
    logger.info('stream: {}'.format(stream))
    if stream.get('logStreamName').startswith(STREAM_NAME_PREFIX):
        logger.info('delete streamName: {}'.format(stream.get('logStreamName')))
        delete_response = logs.delete_log_stream(
            logGroupName=LOGS_GROUP_NAME,
            logStreamName=stream['logStreamName']
        )
        logger.info('delete response: {}'.format(delete_response))
    else:
        logger.info('???: {}: {}'.format(stream.get('logStreamName'), stream.get('logStreamName').startswith(STREAM_NAME_PREFIX)))


def lambda_handler(event, context):
    logger.info('event: {}'.format(event))

    response = dict()
    response['nextToken'] = ''

    while True:

        # if response['nextToken'] == '':
        if response.get('nextToken', '') == '':

            response = logs.describe_log_streams(
                logGroupName=LOGS_GROUP_NAME
            )
            logger.info(response)

            results = list(map(lambda x: delete_stream(x), response['logStreams']))
            logger.info('map result:{}'.format(results))

        else:

            response = logs.describe_log_streams(
                logGroupName=LOGS_GROUP_NAME,
                nextToken=response['nextToken']
            )
            logger.info(response)

            results = list(
                map(lambda x: delete_stream(x), response['logStreams']))
            logger.info('map result:{}'.format(results))

        # if response['nextToken'] == '':
        if response.get('nextToken', '') == '':
            break
