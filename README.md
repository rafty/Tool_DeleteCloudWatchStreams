# Tool_CloudWatchStreamDelete
CloudWatch Logsのログストリームを削除する

[delete all log streams of a log group using aws cli](https://stackoverflow.com/questions/42134873/delete-all-log-streams-of-a-log-group-using-aws-cli)

```bash
$ aws logs describe-log-streams --log-group-name $LOG_GROUP_NAME --query 'logStreams[*].logStreamName' --output table | awk '{print $2}' | grep -v ^$ | while read x; do aws logs delete-log-stream --log-group-name $LOG_GROUP_NAME --log-stream-name $x; done
```

__Delete streams from a specific month__
```bash

aws logs describe-log-streams --log-group-name $LOG_GROUP --query 'logStreams[?starts_with(logStreamName,`2017/07`)].logStreamName' --output table | awk '{print $2}' | grep -v ^$ | while read x; do aws logs delete-log-stream --log-group-name $LOG_GROUP --log-stream-name $x; done
```

```python
import boto3

client = boto3.client('logs')

response = client.describe_log_streams(
    logGroupName='/aws/batch/job'
)


def delete_stream(stream):
    delete_response = client.delete_log_stream(
        logGroupName='/aws/batch/job',
        logStreamName=stream['logStreamName']
    )

    print(delete_response)


results = map(lambda x: delete_stream(x), response['logStreams'])
```

[AWS Lambdaで不要なCloudWatch Logsのログストリームを削除する](http://blog.serverworks.co.jp/tech/2020/03/13/schedule-delete-log-stream-with-lambda/)

aws logs describe-log-streams --log-group-name "/aws/lambda/serverlessrepo-Datadog-Log-For-loglambdaddfunction-1379AY0BANFA7"


```
$ UPLOADBUCKETNAME=yagita-lambda-functions

$ aws cloudformation package \
    --template-file template.yml \
    --s3-bucket $UPLOADBUCKETNAME \
    --output-template-file packaged.yml
```

```
$ aws cloudformation deploy \
    --stack-name Tool-DeleteCloudWatchLogsStream \
    --region ap-northeast-1 \
    --template-file packaged.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --output text
```
