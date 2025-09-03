import boto3
import requests
import os
import json
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import sys

# Load env vars
load_dotenv()

# Config from .env
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Mumbai")
BUCKET_NAME = os.getenv("BUCKET_NAME", "mumbai-weather-data-001")  # must be globally unique
REGION = os.getenv("AWS_REGION", "ap-south-1")

if not API_KEY:
    print(" Missing OPENWEATHER_API_KEY in .env file")
    sys.exit(1)

# AWS client
s3 = boto3.client("s3", region_name=REGION)

def ensure_bucket(bucket_name):
    """Check if S3 bucket exists, create if not (with encryption & restricted access)."""
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f" Bucket {bucket_name} exists, reusing it.")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("404", "NoSuchBucket"):
            print(f" Bucket {bucket_name} not found. Creating...")

            # us-east-1 is special — CreateBucketConfiguration is not allowed
            if REGION == "us-east-1":
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": REGION}
                )

            # Block public access
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                },
            )

            # Enable encryption
            s3.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "AES256"
                            }
                        }
                    ]
                },
            )

            print(f" Bucket {bucket_name} created in {REGION} with encryption and blocked public access.")
        else:
            print(f" Error checking bucket: {e}")
            sys.exit(1)

def fetch_weather():
    """Fetch current weather data from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        print(f" Weather data fetched for {CITY}")
        return resp.json()
    except requests.RequestException as e:
        print(f" Failed to fetch weather data: {e}")
        sys.exit(1)

def upload_to_s3(data):
    """Save weather data locally and upload to S3."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"raw/{datetime.now().strftime('%Y/%m/%d')}/{CITY}/{CITY}_{timestamp}.json"

    filename = f"{CITY}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    try:
        s3.upload_file(filename, BUCKET_NAME, key)
        print(f" Uploaded {filename} → s3://{BUCKET_NAME}/{key}")
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_bucket(BUCKET_NAME)
    weather_data = fetch_weather()
    upload_to_s3(weather_data)
