import json
import sqlite3
import xml.etree.ElementTree as xml
from contextlib import closing
from io import BytesIO
from os import getenv

import autokitteh
import boto3

INSERT_SQL = """
INSERT INTO points
	(track_id, n, lat, lng, height)
VALUES
	(:track_id, :n, :lat, :lng, :height)
;
"""


# From secret
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = getenv("AWS_SECRET_KEY")
DB_DSN = getenv("DB_DSN")

# From vars in manifest
AWS_REGION = getenv("AWS_REGION")


def on_new_s3_object(event):
    event = json.loads(event.data.body)
    print("event:", event)
    if url := event.get("SubscribeURL"):
        print(f"SNS Subscribe URL: {url}")
        return

    # sns events encodes the `Message` field in JSON
    s3_event = json.loads(event["Message"])
    for record in s3_event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"getting {bucket}/{key}")
        data = get_s3_object(bucket, key)
        records = parse_gpx(key, data)
        count = insert_records(DB_DSN, records)
        print(f"inserted {count} records")


@autokitteh.activity
def get_s3_object(bucket, key):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


@autokitteh.activity
def insert_records(db_dsn, records):
    with closing(sqlite3.connect(db_dsn)) as conn, conn:
        cur = conn.executemany(INSERT_SQL, records)
    return cur.rowcount


trkpt_tag = "{http://www.topografix.com/GPX/1/1}trkpt"


@autokitteh.activity
def parse_gpx(track_id, data):
    io = BytesIO(data)
    root = xml.parse(io).getroot()
    return [
        {
            "track_id": track_id,
            "n": i,
            "lat": float(elem.get("lat")),
            "lng": float(elem.get("lon")),
            "height": float(elem.findtext(".//")),
        }
        for i, elem in enumerate(root.findall(".//" + trkpt_tag))
    ]
