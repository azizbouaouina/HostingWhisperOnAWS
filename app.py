import boto3 
import whisper
import ffmpeg
import numpy as np
import json

def load_audio(file: (str, bytes), sr: int = 16000):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: (str, bytes)
        The audio file to open or bytes of audio file

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    
    if isinstance(file, bytes):
        inp = file
        file = 'pipe:'
    else:
        inp = None
    
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd=r"/usr/local/bin/ffmpeg/ffmpeg", capture_stdout=True, capture_stderr=True, input=inp)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

# Create an S3 client object
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Extract the name of the S3 bucket and the file name from the event object
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    # Get the audio file data from S3 using the S3 client object
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    
    # Read the contents of the audio file
    file_data = s3_response['Body'].read()
    
    # Load the audio file data into an array to be used for transcription
    data_array=load_audio(file_data)

    #transcribe the audio file using Whisper
    model = whisper.load_model("large-v2",download_root ="/tmp/whisper")
    result = model.transcribe(data_array)
    print(result["text"])

    # Return the transcription result as a JSON object
    return {
        'statusCode': 200,
        'body': json.dumps(result["text"])
    }