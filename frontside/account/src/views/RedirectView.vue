<template>
  <div>Redirect to {{ redirectPath }}</div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useRouter, useRoute } from "vue-router";

export default defineComponent({
  name: 'RedirctView',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const redirectPath = ref<string | undefined>( (route.query && route.query.redirect) ? `${route.query.redirect}` : undefined);
    onMounted(() => {
      if (redirectPath.value) {
        router.push({ path: redirectPath.value });
      }
    });
    return {
      redirectPath
    }
  }
});
</script>
