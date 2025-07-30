---
title: ETL Pipeline From S3 to SQLite
description: Processes GPX files from S3 and inserts them into a SQLite database, creating a data pipeline from cloud to structured data
integrations: ["aws", "sqlite3"]
categories: ["DevOps"]
tags: ["data_pipeline", "webhook_handling", "activity", "data_processing", "essential"]
---

# ETL Pipeline From S3 to SQLite

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=data_pipeline)

This project downloads and parses GPX files from an S3 bucket and inserts the resulting structured records into a SQLite database. It leverages AWS notifications to trigger an HTTP endpoint when new GPX files are available.

## How It Works

1. Monitor S3 bucket for new GPX files
2. Receive SNS notification at AutoKitteh HTTP endpoint
3. Extract file details from notification
4. Download GPX file from S3 bucket
5. Parse file contents into structured data
6. Insert parsed records into SQLite database

## Cloud Usage

1. Initialize your AWS connection
2. Configure your SNS topic and S3 bucket notifications to trigger on new GPX file uploads.
3. Deploy the project

## Trigger Workflow

> [!IMPORTANT]
> Ensure all connections (AWS) are initialized; otherwise, the workflow will raise a `ConnectionInitError`.

To trigger the workflow, upload a new GPX file to the S3 bucket (you can use `hike.gpx` from here).
After the file is loaded, look at the session log:

```json
[2024-06-27 14:15:44.990824306 +0000 UTC] [stdout] event: {'Type': 'Notification', 'MessageId': 'e199ce57-86f5-59ba-a38a-90a0f0e190aa', 'TopicArn': 'arn:aws:sns:eu-north-1:975050051518:hikes', 'Subject': 'Amazon S3 Notification', 'Message': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"eu-north-1","eventTime":"2024-06-27T14:14:44.418Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROA6GBMDB67DH6QBEE75:miki"},"requestParameters":{"sourceIPAddress":"147.235.211.162"},"responseElements":{"x-amz-request-id":"2593RVSRRERSMWG4","x-amz-id-2":"h+wcGUnQUN/uIMMybLf+mQj9k0xeAuUWN6GZw9P2fTNXWtpYY4v76wnvtQ5EZI+epG32f0OFGeB64mQScVkYMTVLatKGvn06nC71SQPTP2s="},"s3":{"s3SchemaVersion":"1.0","configurationId":"new","bucket":{"name":"ak-miki-hikes","ownerIdentity":{"principalId":"A3RBVIBHMVQI0T"},"arn":"arn:aws:s3:::ak-miki-hikes"},"object":{"key":"hike11.gpx","size":31683,"eTag":"07618ea3c6e04cb24c80007a10d91438","sequencer":"00667D73D45F53EA22"}}}]}', 'Timestamp': '2024-06-27T14:14:44.924Z', 'SignatureVersion': '1', 'Signature': 'fpXoBYMe3pvs74mtXy7vKCi9DDmh7kPeecoGuqgsEuyBHLK40yzWaZDb/v71WfsDH/UOLOAWE/LyqkAmOj3xNQVlH9NYh+rRYjAw6YcrzjRvmd2GvRqG6ZCQIxUgrUmXGSibFIGnJeTTEuLdKiP+FDU26ZjvGcAt9ogC6no9MT2+mkPd+9z1Czs+JDEGBV7IgWwDKKQ51Rkt48+CzjYl9EBeQesn4EjTpdIckss3p0324hc6IZneQhLcqopaPNVMLPX83hlAFmCEMSoUxuMp+dyGMaXVG4PsmpP2I3M5lbdnHBk5bueneJRft8xAsLMkFt+tfdwpHbIakm2I14vEZQ==', 'SigningCertURL': 'https://sns.eu-north-1.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem', 'UnsubscribeURL': 'https://sns.eu-north-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-north-1:975050051518:hikes:18b9ba01-43f1-4a6f-a5a1-95c76a68f760'}
[2024-06-27 14:15:45.002167665 +0000 UTC] [stdout] getting ak-miki-hikes/hike11.gpx
[2024-06-27 14:15:46.075361184 +0000 UTC] [stdout] inserted 358 records
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- The current parsing mechanism is tailored for GPX files and might need adjustments for other formats
- Error handling is basic and may require enhancement for production environments

## AWS Setup

Make sure you have AWS keys with read access to the S3 bucket.

See [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for more information on how to create AWS keys.

### Configuring S3 Bucket for Notifications

> [!WARNING]
> This project assumes that the AutoKitteh server is already configured with
> [HTTP tunneling](https://docs.autokitteh.com/config/http_tunneling/).

- Create an S3 bucket, or using an existing one
- [Create SNS topic](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html)
- [Give the bucket permission to publish to the SNS topic](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html#step1-create-sns-topic-for-notification)
- Create a subscription to the SNS topic
  - Select `HTTPS` protocol
  - In the `Endpoint`, write the domain from ngrok and the HTTP trigger path.
    For example `https://e7c499cae8d9.ngrok.app/<webhook-slug>`
- Send a confirmation to the subscription.
  This will trigger the workflow and you should be able to see the subscription URL in the `ak` logs.

Visit the URL to confirm the subscription.

### Configure the S3 Bucket to Send Notifications

See [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html).

### Create the Database

(Self-hosted) Pick a location for the database, say `$PWD/hikes.db`, and create the database.

```
sqlite3 $PWD/hikes.db < schema.sql
```

> [!NOTE]
> When running on autokitteh.com, you can set the workflow variable `CREATE_DB` to `yes` to automatically
> create the database. Note that since the database is created inside the workflow's Docker container,
> it will be deleted when the workflow session ends.
