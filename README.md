# Audio Transcription using AWS Lambda and OpenAI Whisper

This repository contains a Python Lambda function for transcribing audio files stored in an S3 bucket using the Whisper ASR (Automatic Speech Recognition) system.

## Requirements

- [Amazon Web Services (AWS)](https://aws.amazon.com/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [Docker](https://www.docker.com/)
- [Boto3](https://aws.amazon.com/sdk-for-python/)
- [Whisper ASR](https://github.com/openai/whisper)

## Functionality

The Lambda function defined in `app.py` does the following:

1. Listens for S3 bucket events.
2. When a new audio file is uploaded to the S3 bucket, it triggers the Lambda function.
3. The function downloads the audio file from S3.
4. It uses FFMpeg to decode the audio file and resample it to a specified sample rate.
5. The audio data is transcribed using the Whisper ASR model.
6. The transcription result is returned as a JSON response.

## Installation and Deployment

1. Build the Docker image with the provided Dockerfile.
2. Deploy the Docker image as an AWS Lambda function. You can use AWS Elastic Container Registry (ECR) for this purpose.
3. Set up an S3 bucket event trigger to invoke the Lambda function when a new audio file is uploaded.
4. Ensure that the Lambda function has the necessary IAM permissions to read from the S3 bucket and write to CloudWatch Logs.

## Usage 
1. Upload an audio file to the configured S3 bucket.
2. Wait for the Lambda function to be triggered automatically by the S3 bucket event.
3. Retrieve the transcription result from the Lambda function's JSON response.

![6](https://github.com/azizbouaouina/HostingWhisperOnAWS/assets/104959387/abe1f800-bcc1-463c-a30e-10267c29dde7)
