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
      <el-menu-item label="List" name="list" index="2">List</el-menu-item>
      <el-menu-item label="Graph" name="graph" index="3">Graph</el-menu-item>
      <el-menu-item label="Tools" name="tools" index="4">Tools</el-menu-item>
      <div class="flex-grow" />
      <el-menu-item label="SignOut" name="signout" index="5">SignOut</el-menu-item>
    </el-menu>
    <router-view/>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { useRouter } from "vue-router";
import { Authenticator, useAuthenticator, translations } from "@aws-amplify/ui-vue";
import { I18n } from 'aws-amplify';
import "@aws-amplify/ui-vue/styles.css";
I18n.putVocabularies(translations);
I18n.setLanguage('ja');

// import awsconfig from '@/aws-exports';
// Amplify.configure(awsconfig);

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
          router.push({ name: "GraphView" });
          break;
        case "4":
          router.push({ name: "ToolsView" });
          break;
        case "5":
          auth.value.signOut();
          break;
      }
    };
    watch(router.currentRoute, (newRoute, oldRoute) => {
      const path = newRoute.path
      switch(path) {
        case "/input":
          activeIndex.value = "1";
          break;
        case "/list":
          activeIndex.value = "2";
          break;
        case "/graph":
          activeIndex.value = "3";
          break;
        case "/tools":
          activeIndex.value = "4";
          break;
        // default:
        //   activeIndex.value = "1";
        //   router.push({ name: "SlipInput" });
      }
    });
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
