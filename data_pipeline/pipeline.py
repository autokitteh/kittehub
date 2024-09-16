"""Parse GPX files when uploaded to an S3 bucket, and insert the data into a SQLite database."""

from contextlib import closing
from io import BytesIO
import json
import os
import sqlite3
import xml.etree.ElementTree as xml

import autokitteh
from autokitteh.aws import boto3_client


DB_DSN = os.getenv("DB_DSN")  # Secret

INSERT_SQL = """
INSERT INTO points
	(track_id, n, lat, lng, height)
VALUES
	(:track_id, :n, :lat, :lng, :height)
;
"""


def on_new_s3_object(event):
    if not event.data.body.json:
        print("Unexpected (non-JSON) content type:", event)
        return

    event = event.data.body.json
    print("event:", event)
    if url := event.get("SubscribeURL"):
        print("SNS Subscribe URL:", url)
        return

    # SNS events encode the `Message` field in JSON
    s3_event = json.loads(event.get("Message", {}))
    for record in s3_event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"getting {bucket}/{key}")
        data = get_s3_object(bucket, key)
        records = parse_gpx(key, data)
        count = insert_records(DB_DSN, records)
        print(f"inserted {count} records")


@autokitteh.activity
def get_s3_object(bucket, key):
    response = boto3_client("aws_conn", "s3").get_object(Bucket=bucket, Key=key)
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
