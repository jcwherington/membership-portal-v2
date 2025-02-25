#!/bin/bash
set -eou pipefail

AWS_REGION=us-west-2
BRANCH=$(git branch --show-current)
STACK_NAME=notification-service-$BRANCH-stack
LAMBDA_BUCKET=mpv2-lambda
TEMPLATE_BUCKET=mpv2-email-templates

# S3 object key for Lambda deployment package and email template
NOTIFICATION_SRC_OBJECT_KEY=notification-service-$BRANCH/notification.zip
TEMPLATE_SRC_OBJECT_KEY=outcome_email_$BRANCH.html

# Local paths to the Lambda deployment package and email template
NOTIFICATION_DEPLOYMENT_PACKAGE=build/notification.zip
NOTIFICATION_EMAIL_TEMPLATE=templates/outcome_email.html

# Upload the Lambda deployment packages to S3
aws s3 cp $NOTIFICATION_DEPLOYMENT_PACKAGE s3://$LAMBDA_BUCKET/$NOTIFICATION_SRC_OBJECT_KEY --region $AWS_REGION
aws s3 cp $NOTIFICATION_EMAIL_TEMPLATE s3://$TEMPLATE_BUCKET/$TEMPLATE_SRC_OBJECT_KEY --region $AWS_REGION

SENDER=$(aws ssm get-parameter --name mpv2-sender --query "Parameter.Value" --output text)

# Deploy the notification service stack
# Update the stack or create it if it doesn't already exist
if aws cloudformation describe-stacks --stack-name $STACK_NAME 2>/dev/null; then
    echo "Updating stack $STACK_NAME"
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://$PWD/sam_template.yml \
        --parameters \
            ParameterKey=NotificationSrcObjectKey,ParameterValue=$NOTIFICATION_SRC_OBJECT_KEY \
            ParameterKey=LambdaBucket,ParameterValue=$LAMBDA_BUCKET \
            ParameterKey=TemplateBucket,ParameterValue=$TEMPLATE_BUCKET \
            ParameterKey=Sender,ParameterValue=$SENDER \
            ParameterKey=Branch,ParameterValue=$BRANCH \
        --region $AWS_REGION \
        --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME
else
    echo "Creating stack $STACK_NAME"
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://$PWD/sam_template.yml \
        --parameters \
            ParameterKey=NotificationSrcObjectKey,ParameterValue=$NOTIFICATION_SRC_OBJECT_KEY \
            ParameterKey=LambdaBucket,ParameterValue=$LAMBDA_BUCKET \
            ParameterKey=TemplateBucket,ParameterValue=$TEMPLATE_BUCKET \
            ParameterKey=Sender,ParameterValue=$SENDER \
            ParameterKey=Branch,ParameterValue=$BRANCH \
        --region $AWS_REGION \
        --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
fi

# Use the latest version of source code
aws lambda update-function-code \
    --function-name notification-handler-$BRANCH \
    --s3-bucket $LAMBDA_BUCKET \
    --s3-key $NOTIFICATION_SRC_OBJECT_KEY

echo '++ Complete ++'