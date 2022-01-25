<template>
  <q-toolbar>
    <q-btn v-if="hasBack" flat round dense icon="arrow_back" @click="onBack">
      <q-tooltip>
        {{ $t("back") }}
      </q-tooltip>
    </q-btn>
    <q-toolbar-title>Knickzettelspiel</q-toolbar-title>
    <LocaleSelector />
    <template v-if="hasLogout">
      <q-chip color="white" icon="account_circle">
        {{ currentUser.name }}
      </q-chip>
      <q-btn flat round dense icon="logout" @click="onLogout">
        <q-tooltip>
          {{ $t("logout") }}
        </q-tooltip>
      </q-btn>
    </template>
  </q-toolbar>
</template>

<script>
import { mapState } from "vuex";

import LocaleSelector from "./LocaleSelector.vue";

export default {
  computed: {
    ...mapState(["currentUser", "state"]),
    hasBack() {
      return this.state == "showGame";
    },
    hasLogout() {
      return this.state != "login";
    },
  },
  methods: {
    onBack() {
      if (this.state == "showGame") return this.$store.commit("listGames");
    },
    onLogout() {
      if (this.state != "login") {
        this.$store.dispatch("logout");
        return this.$store.commit("logout");
      }
    },
  },
  components: { LocaleSelector },
};
</script>

<style scoped></style>
