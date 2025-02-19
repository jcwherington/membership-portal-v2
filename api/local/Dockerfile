FROM public.ecr.aws/lambda/python:3.13 AS applications
COPY applications/src ${LAMBDA_TASK_ROOT}
CMD ["app.handler"]

FROM public.ecr.aws/lambda/python:3.13 AS membership
COPY membership/src ${LAMBDA_TASK_ROOT}
COPY membership/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD ["app.handler"]
