#!/bin/bash
set -eou pipefail

AWS_REGION=us-west-2
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BRANCH=$(git branch --show-current)
STACK_NAME=membership-api-$BRANCH-stack
BUCKET=mpv2-lambda

# S3 bucket and object key for Lambda deployment packages and swagger definition
MEMBERSHIP_SRC_OBJECT_KEY=membership-api-$BRANCH/membership.zip
APPLICATION_SRC_OBJECT_KEY=membership-api-$BRANCH/application.zip
SWAGGER_OBJECT_KEY=membership-api-$BRANCH/swagger.yml

# Local path to the Lambda deployment packages and swagger definition
MEMBERSHIP_DEPLOYMENT_PACKAGE=membership/build/membership-api.zip
APPLICATION_DEPLOYMENT_PACKAGE=applications/build/application-api.zip
SWAGGER_DEFINITION=swagger.yml

# Upload the Lambda deployment packages to S3
aws s3 cp $MEMBERSHIP_DEPLOYMENT_PACKAGE s3://$BUCKET/$MEMBERSHIP_SRC_OBJECT_KEY --region $AWS_REGION
aws s3 cp $APPLICATION_DEPLOYMENT_PACKAGE s3://$BUCKET/$APPLICATION_SRC_OBJECT_KEY --region $AWS_REGION

# Upload the Lambda swagger definition to S3
aws s3 cp $SWAGGER_DEFINITION s3://$BUCKET/$SWAGGER_OBJECT_KEY --region $AWS_REGION

# retrieve database config from SSM
DB_NAME=$(aws ssm get-parameter --name mpv2-db-name --query "Parameter.Value" --output text)
DB_PORT=$(aws ssm get-parameter --name mpv2-db-port --query "Parameter.Value" --output text)
DB_ENDPOINT=$(aws ssm get-parameter --name mpv2-db-endpoint --query "Parameter.Value" --output text)
DB_USER=$(aws ssm get-parameter --name mpv2-db-user --query "Parameter.Value" --output text)
DB_PASSWORD=$(aws ssm get-parameter --name mpv2-db-password --query "Parameter.Value" --output text)
SNS_TOPIC_ARN=arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:Outcome-$BRANCH

# Deploy the membership api stack
# Update the stack or create it if it doesn't already exist
if aws cloudformation describe-stacks --stack-name $STACK_NAME 2>/dev/null; then
    echo "Updating stack $STACK_NAME"
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://$PWD/sam_template.yml \
        --parameters \
            ParameterKey=MembershipSrcObjectKey,ParameterValue=$MEMBERSHIP_SRC_OBJECT_KEY \
            ParameterKey=ApplicationSrcObjectKey,ParameterValue=$APPLICATION_SRC_OBJECT_KEY \
            ParameterKey=SwaggerObjectKey,ParameterValue=$SWAGGER_OBJECT_KEY \
            ParameterKey=Branch,ParameterValue=$BRANCH \
            ParameterKey=Bucket,ParameterValue=$BUCKET \
            ParameterKey=DbName,ParameterValue=$DB_NAME \
            ParameterKey=DbPort,ParameterValue=$DB_PORT \
            ParameterKey=DbEndpoint,ParameterValue=$DB_ENDPOINT \
            ParameterKey=DbUser,ParameterValue=$DB_USER \
            ParameterKey=DbPassword,ParameterValue=$DB_PASSWORD \
            ParameterKey=SnsTopicArn,ParameterValue=$SNS_TOPIC_ARN \
        --region $AWS_REGION \
        --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME
else
    echo "Creating stack $STACK_NAME"
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://$PWD/sam_template.yml \
        --parameters \
            ParameterKey=MembershipSrcObjectKey,ParameterValue=$MEMBERSHIP_SRC_OBJECT_KEY \
            ParameterKey=ApplicationSrcObjectKey,ParameterValue=$APPLICATION_SRC_OBJECT_KEY \
            ParameterKey=SwaggerObjectKey,ParameterValue=$SWAGGER_OBJECT_KEY \
            ParameterKey=Branch,ParameterValue=$BRANCH \
            ParameterKey=Bucket,ParameterValue=$BUCKET \
            ParameterKey=DbName,ParameterValue=$DB_NAME \
            ParameterKey=DbPort,ParameterValue=$DB_PORT \
            ParameterKey=DbEndpoint,ParameterValue=$DB_ENDPOINT \
            ParameterKey=DbUser,ParameterValue=$DB_USER \
            ParameterKey=DbPassword,ParameterValue=$DB_PASSWORD \
            ParameterKey=SnsTopicArn,ParameterValue=$SNS_TOPIC_ARN \
        --region $AWS_REGION \
        --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
fi

# Use the latest version of source code
aws lambda update-function-code \
    --function-name membership-api-handler-$BRANCH \
    --s3-bucket $BUCKET \
    --s3-key $MEMBERSHIP_SRC_OBJECT_KEY
aws lambda update-function-code \
    --function-name application-api-handler-$BRANCH \
    --s3-bucket $BUCKET \
    --s3-key $APPLICATION_SRC_OBJECT_KEY

echo '++ Complete ++'
