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
vue create account # Manually select featuresを選択。詳細は後述
cd account
yarn add axios
yarn add google-palette
yarn add vue-chartjs chart.js
yarn add element-plus
```

プロジェクト選択詳細
```console
? Please pick a preset: Manually select features
Babel
TypeScript
Router
Vuex
CSS Pre-processors
Linter / Formatter
Unit Testing

? Check the features needed for your project: Babel, TS, Router, Vuex, CSS Pre-processors, Linter, Unit
? Choose a version of Vue.js that you want to start the project with 3.x
? Use class-style component syntax? No
? Use Babel alongside TypeScript (required for modern mode, auto-detected polyfills, transpiling JSX)? Yes
? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): Less
? Pick a linter / formatter config: Basic
? Pick additional lint features: Lint on save
? Pick a unit testing solution: Jest
? Where do you prefer placing config for Babel, ESLint, etc.? In dedicated config files
```

ChromeをCORS無効で起動する時
```console
# 以下どちらか
"C:\Program Files\Google\Chrome\Application\chrome.exe" --disable-web-security --user-data-dir="C:\temp" --disable-site-isolation-trials
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --disable-web-security --user-data-dir="C:\temp" --disable-site-isolation-trials
```