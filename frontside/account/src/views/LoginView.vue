<template>
  <authenticator>
    <template v-slot="{ user, signOut }">
      <h1>Hello {{ user.username }}!</h1>
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator>
</template>
<script lang="ts">
import { defineComponent /* , computed, ref, onMounted */ } from 'vue';
import { Authenticator } from "@aws-amplify/ui-vue";
import { Amplify } from 'aws-amplify';
import "@aws-amplify/ui-vue/styles.css";

import awsconfig from '@/aws-exports';
Amplify.configure(awsconfig);

export default defineComponent({
  name: 'LoginView',
  // setup() {
  // }
  components: {
    Authenticator
  },
});
</script>
