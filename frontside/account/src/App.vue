<template>
  <authenticator>
    <template v-slot="{ signOut }">
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator>
  <div id="app">
    <div v-if="auth.route === 'authenticated'">
      <el-menu
        :default-active="activeIndex"
        class="el-menu-navi"
        mode="horizontal">
        <router-link to="/input" index="1">Input</router-link>
      </el-menu>
      <nav>
      </nav>
      <router-view/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent /* , computed, onMounted */ , ref } from 'vue';
import { Authenticator, useAuthenticator } from "@aws-amplify/ui-vue";
import { Amplify } from 'aws-amplify';
import "@aws-amplify/ui-vue/styles.css";

import awsconfig from '@/aws-exports';
Amplify.configure(awsconfig);

export default defineComponent({
  name: 'LoginView',
  setup() {
    const auth = ref(useAuthenticator());
    const activeIndex = ref<string>("1");
    return {
      auth,
      activeIndex
    }
  },
  components: {
    Authenticator
  },
});
</script>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
