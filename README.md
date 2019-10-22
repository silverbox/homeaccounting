# homeaccounting
 my private accounting

# Outline
Accounting service based on AWS service.
- AWS DynamoDB as persitant layer
- AWS lambda as server side logic
- AWS APIGateway as API accepter
- AWS S3 as webpage front side layer
- AWS CloudFront as entrance

# How to setup
1. Import cloudformation template
  - aws/cloudformation/templates/cfn-dynamodb-template
  - aws/cloudformation/templates/cfn-mainbody-template
  - aws/cloudformation/templates/cfn-cloudfront-template<br>
    need one parameter [API Key of API Gateway].
  - set CloudFront config. behaviors (API Gateway)> Edit > change "Cache Based on Selected Request Headers" to "None(Improves caching)"

2. Deploy lambda function

# branches
- 1-1-base_design <br>
Add design information, cloudformation template files, sample s3 resource and apigateway swagger file.