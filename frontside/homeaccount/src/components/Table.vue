<template>
  <div class="hello">
    <div class="sample">
      <h2>Basic Button</h2>
      <el-row>
        <el-button type="primary" plain @click="reload">Reload</el-button>
        <el-button type="success" plain @click="logout">Logout</el-button>
        <el-button type="info" plain @click="s3test">S3 test</el-button>
        <el-button type="warning" plain @click="download">Download</el-button>
        <el-button type="danger" plain>Danger</el-button>
      </el-row>
    </div>

    <div class="sample">
      <h2>Text Button</h2>
      <el-row>
        <el-date-picker v-model="tgtdate_from" type="date" placeholder="Pick a day" />
        <el-date-picker v-model="tgtdate_to" type="date" placeholder="Pick a day" />
        <el-input v-model="balance" />
      </el-row>
    </div>
  </div>
</template>

<script>
import AWS from 'aws-sdk'
import awsconfig from '../cognito/config'
// import cognito from '@/cognito'

const S3_USERBACKETNAME = 'myapp-userdata'
const PROVIDER_KEY = 'cognito-idp.' + awsconfig.Region + '.amazonaws.com/' + awsconfig.UserPoolId

export default {
  name: 'Graph',
  data () {
    return {
      balance: 4,
      tgtdate_from: new Date(),
      tgtdate_to: new Date()
    }
  },
  methods: {
    reload: function () {
      console.log(this.tgtdate)
      console.log(this.apienv.baseendpoint)

      this.$cognito.callGetApi(this.$axios, this.apienv.baseendpoint + 'balance?tgt_date=20190831').then(
        response => {
          console.log(response.data)
          /* this.tableData3 = response.data; */
        }
      ).catch(err => {
        this.$message({message: err, type: 'error'})
      })
    },
    s3test: function () {
      const cognitoUser = this.$cognito.userPool.getCurrentUser()
      cognitoUser.getSession((err, session) => {
        if (!err && session.isValid()) {
          const itoken = session.getIdToken().getJwtToken()

          // Initialize the Amazon Cognito credentials provider
          AWS.config.region = awsconfig.Region
          AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: awsconfig.IdentityPoolId,
            Logins: {
              [PROVIDER_KEY]: itoken
            }
          })
          var identityId = AWS.config.credentials.identityId
          var s3key = 'cognito/myhome-account/' + identityId + '/testfile.txt'

          // refresh AWS credentials
          AWS.config.credentials.refresh((err) => {
            if (err) {
              var errmsg = (err.message || JSON.stringify(err))
              this.$message({showClose: true, message: errmsg, type: 'error'})
              console.log(err)
            } else {
              var s3 = new AWS.S3({
                params: { Bucket: S3_USERBACKETNAME }
              })

              const updateParams = {
                Key: s3key,
                Body: 'teststring',
                ContentType: 'application/text'
              }

              s3.upload(updateParams, function (err, data) {
                if (err) {
                  console.log('error : ', err)
                } else {
                  console.log('success : ' + S3_USERBACKETNAME + '/' + s3key)
                }
              })
            }
          })
        }
      })
    },
    download: function () {
      const cognitoUser = this.$cognito.userPool.getCurrentUser()
      var that = this
      cognitoUser.getSession((err, session) => {
        if (!err && session.isValid()) {
          const itoken = session.getIdToken().getJwtToken()
          // Initialize the Amazon Cognito credentials provider
          AWS.config.region = awsconfig.Region
          AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: awsconfig.IdentityPoolId,
            Logins: {
              [PROVIDER_KEY]: itoken
            }
          })
          var identityId = AWS.config.credentials.identityId

          const tgttodatestr = that.$myutils.getYYYYMMDDStr(that.tgtdate_to)
          const tgtfromdatestr = that.$myutils.getYYYYMMDDStr(that.tgtdate_from)

          const prmstr = 'tgt_date_to=' + tgttodatestr + '&tgt_date_from=' + tgtfromdatestr + '&identityid=' + identityId
          this.$cognito.callGetApi(that.$axios, that.apienv.baseendpoint + 'download?' + prmstr).then(
            response => {
              console.log('response : ', response.data)
              var s3 = new AWS.S3({
                params: { Bucket: S3_USERBACKETNAME }
              })
              var getUrlparams = {
                // バケット名
                Bucket: S3_USERBACKETNAME,
                // S3に格納済みのファイル名
                Key: 'cognito/myhome-account/' + identityId + '/' + response.data,
                // 期限(秒数)
                Expires: 900
              }
              // URL発行
              s3.getSignedUrl('getObject', getUrlparams, that.execdownload)
            }
          ).catch(err => {
            that.$message({message: err, type: 'error'})
          })
        }
      })
    },
    execdownload: function (dummy, url) {
      location.href = url
    },
    logout: function () {
      this.$cognito.logout()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
