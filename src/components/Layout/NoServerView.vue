<template>
  <q-banner v-if="remainingTime > 0" rounded class="bg-warning q-mb-sm">
    {{ $t("connecting", { time: remainingTime }) }}
  </q-banner>
  <q-banner inline-actions rounded class="bg-red text-white">
    {{ $t("no-server") }}
    <template v-slot:action>
      <q-btn :label="$t('reload')" icon="loop" @click="reload" />
    </template>
  </q-banner>
</template>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      remainingTime: 10,
      intervalId: null,
    };
  },
  computed: {
    ...mapState(["has_server"]),
  },
  methods: {
    reload() {
      location.reload();
    },
  },
  mounted() {
    this.intervalId = setInterval(() => {
      if (this.remainingTime > 0) {
        this.remainingTime--;
        if (this.has_server) clearInterval(this.intervalId);
      }
    }, 1000);
  },
};
</script>

<style scoped></style>
