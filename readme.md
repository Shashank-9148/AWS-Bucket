# Weather Data to AWS S3

A Python script that fetches current weather data from the [OpenWeatherMap API](https://openweathermap.org/current) and uploads it to an Amazon S3 bucket in JSON format.

## Features

- Fetches live weather data for a specified city.
- Saves the data as a JSON file with a timestamp.
- Uploads the file to an encrypted, private S3 bucket.
- Creates the bucket if it doesn’t exist.
- Automatically handles AWS credentials and bucket policies.
- Structured S3 key format:  
