#!/bin/bash

BRANCH=$(git branch --show-current)
S3_BUCKET="mpv2-static-$BRANCH"

echo ':docker: Generating static assets'

docker build -t membership-portal:$BRANCH .
docker run --rm -v $(pwd)/build:/app/out -e STAGE=$BRANCH membership-portal:$BRANCH

echo ":s3: Deploying to s3"

POLICY_STRING='{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::'$S3_BUCKET'/*"
    }
  ]
}'

PUBLIC_ACCESS_BLOCK='{
    "BlockPublicAcls": false,
    "IgnorePublicAcls": false,
    "BlockPublicPolicy": false,
    "RestrictPublicBuckets": false
}'

# Create bucket if it doesn't exist
if ! aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null; then
    aws s3 mb s3://$S3_BUCKET
    aws s3 website s3://$S3_BUCKET/ --index-document index.html --error-document 404.html
    aws s3api put-public-access-block --bucket $S3_BUCKET --public-access-block-configuration "$PUBLIC_ACCESS_BLOCK"
    aws s3api put-bucket-policy --bucket $S3_BUCKET --policy "$POLICY_STRING"
fi

aws s3 sync "build" "s3://$S3_BUCKET"

echo ":party: Success!"
