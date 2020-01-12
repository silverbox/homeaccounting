<template>
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
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login () {
      this.$cognito.login(this.username, this.password)
        .then(result => {
          this.$router.replace('/input')
        })
        .catch(err => {
          var errmsg = (err.message || JSON.stringify(err))
          this.$message({showClose: true, message: errmsg, type: 'error'})
          this.error = err
        })
    }
  }
}
</script>

<style scoped>
.login{
  padding : 20px;
}
</style>
