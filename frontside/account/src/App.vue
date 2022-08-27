<template>
  <p class="loginpanel">
    <authenticator :hide-sign-up="hideSignup"/>
  </p>
  <div v-if="auth.route === 'authenticated'">
    <el-menu
      :default-active="activeIndex"
      :ellipsis="false"
      class="el-menu-navi"
      mode="horizontal"
      @select="onPageSelect">
      <el-menu-item label="Input" name="input" index="1">Input</el-menu-item>
      <el-menu-item label="List" name="input" index="2">List</el-menu-item>
      <div class="flex-grow" />
      <el-menu-item label="SignOut" name="signout" index="3">SignOut</el-menu-item>
    </el-menu>
    <router-view/>
  </div>
</template>

<script lang="ts">
import { defineComponent /* , computed, onMounted */ , ref } from 'vue';
import { useRouter } from "vue-router";
import { Authenticator, useAuthenticator, translations } from "@aws-amplify/ui-vue";
import { Amplify, I18n } from 'aws-amplify';
import "@aws-amplify/ui-vue/styles.css";
I18n.putVocabularies(translations);
I18n.setLanguage('ja');

import awsconfig from '@/aws-exports';
Amplify.configure(awsconfig);

export default defineComponent({
  name: 'App',
  setup() {
    const router = useRouter();
    const auth = ref(useAuthenticator());
    const activeIndex = ref<string>("1");
    const hideSignup = ref<boolean>(true);
    const menuEllipsis = ref<boolean>(false);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const onPageSelect = (key: string, keyPath: string[]) => {
      switch(key) {
        case "1":
          router.push({ name: "SlipInput" });
          break;
        case "2":
          router.push({ name: "SlipList" });
          break;
        case "3":
          router.push({ name: "SlipInput" });
          auth.value.signOut();
          break;
      }
    };
    router.push({ name: "SlipInput" });
    return {
      auth,
      activeIndex,
      hideSignup,
      menuEllipsis,
      //
      onPageSelect
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

.loginpanel>div {
  height: 94vh;
}

.flex-grow {
  flex-grow: 1;
}

</style>
