<template>
  <div class="hello">
    <div class="sample">
      <h2>Download slip</h2>
      <el-row>
        <el-col :span="8">
          <label class="item-label">開始日</label>
        </el-col>
        <el-col :span="12">
          <el-date-picker v-model="tgtDateFrom" type="date" placeholder="Pick a day" />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
          <label class="item-label">終了日</label>
        </el-col>
        <el-col :span="12">
          <el-date-picker v-model="tgtDateTo" type="date" placeholder="Pick a day" />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-button type="warning" plain @click="download">Download</el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import AWS from 'aws-sdk'
import { useAuthenticator } from '@aws-amplify/ui-vue';
import { CognitoUserSession } from 'amazon-cognito-identity-js';
import { ElMessage } from 'element-plus'

import awsConfig from '@/aws-exports';
import ApiCalls from '@/common/api';
import { accountUtils } from '@/common/accountUtils';

const S3_USERBACKETNAME = 'myapp-userdata'
const PROVIDER_KEY = 'cognito-idp.' + awsConfig.Auth.region + '.amazonaws.com/' + awsConfig.Auth.userPoolId

export default defineComponent({
  name: 'ToolsView',
  setup() {
    const api = new ApiCalls();
    const auth = ref(useAuthenticator());
    const tgtDateFrom = ref<Date>(new Date());
    const tgtDateTo = ref<Date>(new Date());

    const download = () => {
      auth.value.user.getSession(async (error: Error, session: CognitoUserSession) => {
        if (error != null || !session || !session.isValid()) {
          ElMessage({
            showClose: true,
            message: 'セッション取得に失敗しました',
            type: 'error',
          });
          throw error;
        }

        const idToken = session.getIdToken().getJwtToken();
        // Initialize the Amazon Cognito credentials provider
        AWS.config.region = awsConfig.Auth.region;
        const credentials = new AWS.CognitoIdentityCredentials({
          IdentityPoolId: awsConfig.Auth.identityPoolId,
          Logins: {
            [PROVIDER_KEY]: idToken
          }
        });
        AWS.config.credentials = credentials;
        const identityId = credentials.identityId;
        const tgtToDateStr = accountUtils.getYYYYMMDDStr(tgtDateTo.value);
        const tgtFromDateStr = accountUtils.getYYYYMMDDStr(tgtDateFrom.value);
  
        try {
          const zipFileName = await api.getSlipZipFileName(tgtToDateStr, tgtFromDateStr, identityId);
          const s3 = new AWS.S3({
            params: { Bucket: S3_USERBACKETNAME }
          });
          const getUrlparams = {
            // バケット名
            Bucket: S3_USERBACKETNAME,
            // S3に格納済みのファイル名
            Key: 'cognito/myhome-account/' + identityId + '/' + zipFileName,
            // 期限(秒数)
            Expires: 900
          };
          // URL発行
          s3.getSignedUrl('getObject', getUrlparams, execDownloadCallback);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (error: any) {
          ElMessage({
            showClose: true,
            message: `ダウンロード情報取得に失敗しました\n${error}`,
            type: 'error',
          });
        }
      });
    };
    const execDownloadCallback = (err: Error, url: string) => {
      location.href = url;
    };

    return {
      tgtDateFrom,
      tgtDateTo,
      download
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.item-label {
  text-align: end;
  vertical-align: text-top;
}
.el-row {
  margin: 10px;
}
</style>
