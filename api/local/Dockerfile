FROM public.ecr.aws/lambda/python:3.8 AS applications

COPY applications/src ${LAMBDA_TASK_ROOT}
RUN pip install boto3
CMD ["src.api_handler.handle_event"]

FROM public.ecr.aws/lambda/python:3.8 AS membership

COPY membership/src ${LAMBDA_TASK_ROOT}
COPY membership/requirements.txt requirements.txt
RUN pip3 install -t src -r requirements.txt
CMD ["src.api_handler.handle_event"]

# proxy image

# init image
