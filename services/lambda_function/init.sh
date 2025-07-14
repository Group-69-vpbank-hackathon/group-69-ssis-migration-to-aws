aws iam create-role \
  --role-name lambda_processor \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name lambda_processor \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name lambda_processor \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess


# aws lambda publish-layer-version \
#   --layer-name my-python312-layer \
#   --description "Python 3.12 Layer with psycopg2-binary" \
#   --zip-file fileb://my_layer.zip \
#   --compatible-runtimes python3.12 \
#   --region us-east-1

# # core-stream-process
# aws lambda create-function \
#   --function-name qxnam_test_lambda \
#   --runtime python3.12 \
#   --role arn:aws:iam::408110214432:role/lambda_processor \
#   --handler handler.lambda_handler \
#   --zip-file fileb://psycopg2-layer.zip \
#   --timeout 30 \
#   --environment file://db_app.json \
#   --region us-east-1


