<template>
  <q-banner v-if="currentError" rounded class="bg-red text-white q-mb-sm">{{
    currentError
  }}</q-banner>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState(["currentError"]),
  },
};
</script>

<style scoped></style>
