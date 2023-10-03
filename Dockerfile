FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

RUN pip install boto3 --target "${LAMBDA_TASK_ROOT}"

RUN yum install -y git "${LAMBDA_TASK_ROOT}"

RUN pip install git+https://github.com/openai/whisper.git --target "${LAMBDA_TASK_ROOT}"

COPY ffmpeg-6.0-amd64-static /usr/local/bin/ffmpeg

RUN chmod 777 -R /usr/local/bin/ffmpeg

RUN pip install ffmpeg-python --target "${LAMBDA_TASK_ROOT}"

RUN pip install numpy --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler 
CMD [ "app.lambda_handler" ] 