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

3. Set API endpoint and API key to frontside/homeaccount/src/router/index.js

# branches
- 1-1-base_design <br>
Add design information, cloudformation template files, sample s3 resource and apigateway swagger file.


# フロント開発時

コンテナ起動（ホスト）
```
docker-compose up
```

コンテナにログイン（ホスト）
```
docker exec -it account-vuefront bash
```

Vueセットアップ（コンテナ内）
```bash
yarn global add @vue/cli
vue create account # vue3, yarnを選択
cd account
yarn add axios
yarn add google-palette
yarn add vue-chartjs chart.js
yarn add element-plus

```