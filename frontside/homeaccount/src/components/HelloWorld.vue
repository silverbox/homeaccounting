<template>
  <div class="hello">
    <div class="sample">
      <h2>Basic Button</h2>
      <el-row>
        <el-button plain>Plain</el-button>
        <el-button type="primary" plain @click="reload">Reload</el-button>
        <el-button type="success" plain>Success</el-button>
        <el-button type="info" plain>Info</el-button>
        <el-button type="warning" plain>Warning</el-button>
        <el-button type="danger" plain>Danger</el-button>
      </el-row>
    </div>

    <div class="sample">
      <h2>Text Button</h2>
      <el-row>
        <el-date-picker v-model="tgtdate" type="date" placeholder="Pick a day" />
        <el-input v-model="balance" />
      </el-row>
    </div>
    <h1>{{ msg }}</h1>
    <h2>Essential Links</h2>
    <ul>
      <li>
        <a
          href="https://vuejs.org"
          target="_blank"
        >
          Core Docs
        </a>
      </li>
      <li>
        <a
          href="https://forum.vuejs.org"
          target="_blank"
        >
          Forum
        </a>
      </li>
      <li>
        <a
          href="https://chat.vuejs.org"
          target="_blank"
        >
          Community Chat
        </a>
      </li>
      <li>
        <a
          href="https://twitter.com/vuejs"
          target="_blank"
        >
          Twitter
        </a>
      </li>
      <br>
      <li>
        <a
          href="http://vuejs-templates.github.io/webpack/"
          target="_blank"
        >
          Docs for This Template
        </a>
      </li>
    </ul>
    <h2>Ecosystem</h2>
    <ul>
      <li>
        <a
          href="http://router.vuejs.org/"
          target="_blank"
        >
          vue-router
        </a>
      </li>
      <li>
        <a
          href="http://vuex.vuejs.org/"
          target="_blank"
        >
          vuex
        </a>
      </li>
      <li>
        <a
          href="http://vue-loader.vuejs.org/"
          target="_blank"
        >
          vue-loader
        </a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/awesome-vue"
          target="_blank"
        >
          awesome-vue
        </a>
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      balance: 0,
      tgtdate: new Date()
    }
  },
  methods: {
    reload: function () {
      console.log(this.tgtdate)
      console.log(this.apienv.baseurl)
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apienv.key,
          'Authorization': 1
        },
        data: {}
      }

      this.$axios.get(this.apienv.baseurl + 'balance?tgt_date=20190831', config).then(
        response => {
          console.log(response.data)
          /* this.tableData3 = response.data; */
        }
      )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
