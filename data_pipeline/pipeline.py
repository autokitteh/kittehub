"""Parse GPX files when uploaded to an S3 bucket, and insert into a SQLite database."""

from contextlib import closing
from io import BytesIO
import json
import os
from pathlib import Path
import sqlite3
import xml.etree.ElementTree as Xml

import autokitteh
from autokitteh.aws import boto3_client


DB_DSN = os.getenv("DB_DSN", "")  # Secret
CREATE_DB = os.getenv("CREATE_DB", "no").lower() in {"y", "yes", "true"}

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

    if CREATE_DB:
        create_db(DB_DSN)

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
    with closing(sqlite3.connect(db_dsn)) as conn:
        cur = conn.executemany(INSERT_SQL, records)
        conn.commit()
    return cur.rowcount


@autokitteh.activity
def create_db(db_dsn):
    code_dir = Path(__file__).absolute().parent
    schema_file = code_dir / "schema.sql"
    schema_sql = schema_file.read_text()

    with closing(sqlite3.connect(db_dsn)) as conn, conn:
        conn.executescript(schema_sql)


trkpt_tag = "{http://www.topografix.com/GPX/1/1}trkpt"


@autokitteh.activity
def parse_gpx(track_id, data):
    io = BytesIO(data)
    root = Xml.parse(io).getroot()
    records = []

    for i, elem in enumerate(root.findall(".//" + trkpt_tag)):
        records.append(
            {
                "track_id": track_id,
                "n": i,
                "lat": float(elem.get("lat", "0")),
                "lng": float(elem.get("lon", "0")),
                "height": float(elem.findtext(".//") or "0"),
            }
        )

    return records
