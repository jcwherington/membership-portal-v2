#!/bin/bash

AWS_REGION=ap-southeast-2
BRANCH=$(git branch --show-current)
STACK_NAME=membership-api-$BRANCH-stack

# S3 bucket and object key for Lambda deployment packages and swagger definition
MEMBERSHIP_SRC_OBJECT_KEY=membership-api-$BRANCH/membership.zip
APPLICATION_SRC_OBJECT_KEY=membership-api-$BRANCH/application.zip
SWAGGER_OBJECT_KEY=membership-api-$BRANCH/swagger.yml

# Local path to the Lambda deployment packages and swagger definition
MEMBERSHIP_DEPLOYMENT_PACKAGE=membership-api.zip
APPLICATION_DEPLOYMENT_PACKAGE=application-api.zip
SWAGGER_DEFINITION=swagger.yml

# Assume deployer role
aws sts assume-role --role-arn arn:aws:iam::724173394727:role/hyp-deployer-role --role-session-name membership-api-deployment

# Upload the Lambda deployment packages to S3
aws s3 cp $MEMBERSHIP_DEPLOYMENT_PACKAGE s3://hyp-lambda/$MEMBERSHIP_SRC_OBJECT_KEY --region $AWS_REGION
aws s3 cp $APPLICATION_DEPLOYMENT_PACKAGE s3://hyp-lambda/$APPLICATION_SRC_OBJECT_KEY --region $AWS_REGION

# Upload the Lambda swagger definition to S3
aws s3 cp $SWAGGER_DEFINITION s3://hyp-lambda/$SWAGGER_OBJECT_KEY --region $AWS_REGION

# Deploy the membership api stack
# Update the stack or create it if it doesn't already exist
if aws cloudformation describe-stacks --stack-name $STACK_NAME; then
    echo "Updating stack $STACK_NAME"
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://$PWD/sam_template.yml \
        --parameters ParameterKey=MembershipSrcObjectKey,ParameterValue=$MEMBERSHIP_SRC_OBJECT_KEY ParameterKey=ApplicationSrcObjectKey,ParameterValue=$APPLICATION_SRC_OBJECT_KEY ParameterKey=SwaggerObjectKey,ParameterValue=$SWAGGER_OBJECT_KEY ParameterKey=Branch,ParameterValue=$BRANCH \
        --region $AWS_REGION \
        --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME
else
    echo "Creating stack $STACK_NAME"
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://$PWD/sam_template.yml \
        --parameters ParameterKey=MembershipSrcObjectKey,ParameterValue=$MEMBERSHIP_SRC_OBJECT_KEY ParameterKey=ApplicationSrcObjectKey,ParameterValue=$APPLICATION_SRC_OBJECT_KEY ParameterKey=SwaggerObjectKey,ParameterValue=$SWAGGER_OBJECT_KEY ParameterKey=Branch,ParameterValue=$BRANCH \
        --region $AWS_REGION \
        --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
fi

# Use the latest version of source code
aws lambda update-function-code \
    --function-name membership-api-handler-$BRANCH \
    --s3-bucket hyp-lambda \
    --s3-key $MEMBERSHIP_SRC_OBJECT_KEY
aws lambda update-function-code \
    --function-name application-api-handler-$BRANCH \
    --s3-bucket hyp-lambda \
    --s3-key $APPLICATION_SRC_OBJECT_KEY

echo '++ Complete ++'
