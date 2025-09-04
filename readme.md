# Weather Data to AWS S3

A Python script that fetches current weather data from the [OpenWeatherMap API](https://openweathermap.org/current) and uploads it to an Amazon S3 bucket in JSON format.

## Features

- Fetches live weather data for a specified city.
- Saves the data as a JSON file with a timestamp.
- Uploads the file to an encrypted, private S3 bucket.
- Creates the bucket if it doesn’t exist.
- Automatically handles AWS credentials and bucket policies.
- Structured S3 key format:
- The weather data JSON files are stored in the S3 bucket using a well-organized folder structure based on date and location for easy management and retrieval. The format is:

raw/YYYY/MM/DD/<city>/<city>_<YYYYMMDDTHHMMSSZ>.json


Where:

raw/ — a root folder to separate raw data files.

YYYY/MM/DD/ — year, month, and day of the data capture (e.g., 2025/09/04).

<city>/ — the city name for which weather data is fetched (e.g., Mumbai).

<city>_<YYYYMMDDTHHMMSSZ>.json — file name containing the city name and a UTC timestamp in ISO 8601 format (20250904T083000Z), ensuring unique and chronological file naming. 

