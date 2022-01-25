<template>
  <q-banner inline-actions rounded class="bg-red text-white">
    {{ $t("no-server") }}
    <template v-slot:action>
      <q-btn :label="$t('reload')" icon="loop" @click="reload" />
    </template>
  </q-banner>
</template>

<script>
export default {
  methods: {
    reload() {
      location.reload();
    },
  },
};
</script>

<style scoped></style>
