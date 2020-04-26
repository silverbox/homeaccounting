<template>
  <div>
    <el-form @submit.prevent="login" label-width="100px" class="login">
      <h2>ログイン</h2>
      <el-form-item label="ユーザー名">
        <el-input v-model="username" />
      </el-form-item>
      <el-form-item label="パスワード">
        <el-input v-model="password" show-password />
      </el-form-item>
      <el-button type="warning" :plain="true" @click="login">ログイン</el-button>
    </el-form>
    <el-dialog
      title="新しいパスワードの入力"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-input v-model="newpassword" show-password />
      <span slot="footer" class="dialog-footer">
        <el-button @click="onCancelNewPassword">Cancel</el-button>
        <el-button type="primary" @click="onDecideNewPassword">OK</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
let newpasswordresolve
let newpasswordreject
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      newpassword: '',
      dialogVisible: false
    }
  },
  methods: {
    login () {
      this.$cognito.login(this.username, this.password, this.onNewPasswordRequired)
        .then(result => {
          this.$router.replace('/input')
        })
        .catch(err => {
          var errmsg = (err.message || JSON.stringify(err))
          this.$message({showClose: true, message: errmsg, type: 'error'})
          this.error = err
        })
    },
    onNewPasswordRequired () {
      this.dialogVisible = true
      return new Promise((resolve, reject) => {
        newpasswordresolve = resolve
        newpasswordreject = reject
      })
    },
    onCancelNewPassword () {
      this.dialogVisible = false
      newpasswordreject('cancel')
    },
    onDecideNewPassword () {
      this.dialogVisible = false
      newpasswordresolve(this.newpassword)
    },
    handleClose (done) {
      this.$confirm('Are you sure to close this dialog?')
        .then(_ => {
          done()
          newpasswordreject('cancel')
        })
        .catch(_ => {})
    }
  }
}
</script>

<style scoped>
.login{
  padding : 20px;
}
</style>
