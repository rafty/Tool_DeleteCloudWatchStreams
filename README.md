# Tool: Delete old CloudWatch Logs Streams

- Delete old CloudWatch Logs streams older than 3 days.
- Delete log group with stored size 0.

## How to use:
AWS Lambda functionのManagement Consoleでテストを実行する。

## Deploying

```
$ UPLOADBUCKETNAME=xxxxxx-lambda-functions

$ aws cloudformation package \
    --template-file template.yml \
    --s3-bucket $UPLOADBUCKETNAME \
    --output-template-file packaged.yml

$ aws cloudformation deploy \
    --stack-name Tool-DeleteCloudWatchLogsStream \
    --region ap-northeast-1 \
    --template-file packaged.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --output text
```
