# Data Pipeline Workflow

This is an example of a data pipeline workflow. The pipeline is triggered by a new GPX file on an S3 bucket.
The pipeline code will parse the GPX file and insert it into a database.

The event flow is:

- S3 sends a new item notification to an SNS topic
- SNS sends a notification to the AutoKitteh HTTP trigger
- The workflow extracts the bucket and file name from the S3 event
- The workflow reads the file from S3
- The workflow parses the GPX file and inserts the data into a SQLite database

## Setting Up

### Starting `ak`

Start `ak`, you can use development mode

```
ak up --mode dev
```

You'll need to expose `ak` web API to the outside world in order to get events from S3.
In this example, we'll use [ngrok](https://ngrok.com/)

```
ngrok http 9980
```

You'll see a screen with a line like:

```
Forwarding                    https://e7c499cae8d9.ngrok.app -> http://localhost:9980
```

This means your `ak` is exposed to the web at `https://e7c499cae8d9.ngrok.app`, remember this URL, you'll need it later.

### Deploy The Workflow

Before you deploy the workflow, edit the `AWS_REGION` value in the `vars` section of the manifest (`autokitteh.yaml`) to match your bucket region.

```
ak deploy --manifest autokitteh.yaml --file pipeline.py
```

### AWS Keys

Make sure you have AWS keys with read access to the S3 bucket.
See [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for more information on how to create AWS keys.

### Configuring S3 Bucket for Notifications

- Create an S3 bucket, or using an existing one
- [Create SNS topic](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html)
- [Give the bucket permission to publish to the SNS topic][ap]
- Create a subscription to the SNS topic
    - Select `HTTPS` protocol
    - In the `Endpoint`, write the domain from ngrok and the HTTP trigger path.
      For example `https://e7c499cae8d9.ngrok.app/http/pipeline/new_object`
- Send a confirmation to the subscription. 
   This will trigger the workflow and you should be able to see the subscription URL in the `ak` logs.

```
ak session log --prints-only
...
[stdout] SNS Subscribe URL: https://...
```

Visit the URL to confirm the subscription.

### Configure The S3 Bucket to Send Notifications

See [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html).

### Create The Database

Pick a location for the database, say `$PWD/hikes.db`, and create the database.

```
sqlite3 $PWD/hikes.db < schema.sql
```

### Set Up Project Vars and Secrets

Add database location and AWS keys to `ak` secrets.

```
ak var set --env pipeline/default DB_DSN $PWD/hikes.db
ak var set --secret --env pipeline/default AWS_ACCESS_KEY_ID <your aws access key ID>
ak var set --secret --env pipeline/default AWS_SECRET_KEY <your aws secret key>
```

Make sure that your AWS credentials give you access to read the bucket.

[ap]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html#step1-create-sns-topic-for-notification

## Upload Files

Now upload a new GPX file to the bucket (you can use `hike.gpx` from here).
After the file is loaded, look at the session log:

```
ak session log --prints-only
```

```json
[2024-06-27 14:15:44.990824306 +0000 UTC] [stdout] event: {'Type': 'Notification', 'MessageId': 'e199ce57-86f5-59ba-a38a-90a0f0e190aa', 'TopicArn': 'arn:aws:sns:eu-north-1:975050051518:hikes', 'Subject': 'Amazon S3 Notification', 'Message': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"eu-north-1","eventTime":"2024-06-27T14:14:44.418Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROA6GBMDB67DH6QBEE75:miki"},"requestParameters":{"sourceIPAddress":"147.235.211.162"},"responseElements":{"x-amz-request-id":"2593RVSRRERSMWG4","x-amz-id-2":"h+wcGUnQUN/uIMMybLf+mQj9k0xeAuUWN6GZw9P2fTNXWtpYY4v76wnvtQ5EZI+epG32f0OFGeB64mQScVkYMTVLatKGvn06nC71SQPTP2s="},"s3":{"s3SchemaVersion":"1.0","configurationId":"new","bucket":{"name":"ak-miki-hikes","ownerIdentity":{"principalId":"A3RBVIBHMVQI0T"},"arn":"arn:aws:s3:::ak-miki-hikes"},"object":{"key":"hike11.gpx","size":31683,"eTag":"07618ea3c6e04cb24c80007a10d91438","sequencer":"00667D73D45F53EA22"}}}]}', 'Timestamp': '2024-06-27T14:14:44.924Z', 'SignatureVersion': '1', 'Signature': 'fpXoBYMe3pvs74mtXy7vKCi9DDmh7kPeecoGuqgsEuyBHLK40yzWaZDb/v71WfsDH/UOLOAWE/LyqkAmOj3xNQVlH9NYh+rRYjAw6YcrzjRvmd2GvRqG6ZCQIxUgrUmXGSibFIGnJeTTEuLdKiP+FDU26ZjvGcAt9ogC6no9MT2+mkPd+9z1Czs+JDEGBV7IgWwDKKQ51Rkt48+CzjYl9EBeQesn4EjTpdIckss3p0324hc6IZneQhLcqopaPNVMLPX83hlAFmCEMSoUxuMp+dyGMaXVG4PsmpP2I3M5lbdnHBk5bueneJRft8xAsLMkFt+tfdwpHbIakm2I14vEZQ==', 'SigningCertURL': 'https://sns.eu-north-1.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem', 'UnsubscribeURL': 'https://sns.eu-north-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-north-1:975050051518:hikes:18b9ba01-43f1-4a6f-a5a1-95c76a68f760'}
[2024-06-27 14:15:45.002167665 +0000 UTC] [stdout] getting ak-miki-hikes/hike11.gpx
[2024-06-27 14:15:46.075361184 +0000 UTC] [stdout] inserted 358 records
```

## Local Development

### Via `ak`

There's a `Makefile` for common operation

You can run the pipeline locally and test it.
- Initialize the database
    - `make init-db`
- Run `ak --mode dev` and set the AWS keys and database DSN (see above)
    - `make vars`
- Deploy the workflow
    - `make deploy`
- Trigger the workflow
    - Make sure there's a GPX file in your bucket. I'll assume the bucket name is `miki-hikes` and the file is `hike-1.gpx`
    - Edit `example-sns-event.json` and set the bucket name and the file name in the embedded `Message` JSON.
    - `make trigger`
- View the `ak` logs in its console and the workflow logs
    - `make logs`


### Debugging

You can set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_KEY`, and `DB_DSN` in the environment (or in your IDE)
Then you can import `pipeline` and call `pipeline.on_new_s3_object` with the event JSON.

For example:

```python
from os import environ
import json

import pipeline

# Make sure to initialize hikes.db

environ.update({
    'AWS_ACCESS_KEY_ID': '...',
    'AWS_SECRET_KEY': '...',
    'DB_DSN': 'hikes.db',
})

with open('example-sns-event.json') as fp:
    event = json.load(fp)
pipline.on_new_s3_object(event)
```
