<template>
  <q-toolbar>
    <q-btn v-if="hasBack" flat round dense icon="arrow_back" @click="onBack" />
    <q-btn v-if="!hasBack" flat round dense icon="" class="invisible" />
    <q-toolbar-title>Knickzettelspiel</q-toolbar-title>
    <LocaleSelector />
    <template v-if="hasLogout">
      <q-chip color="white">
        <q-icon flat round dense name="account_circle" />&nbsp;{{
          currentUser.name
        }}
      </q-chip>
      <q-btn flat round dense icon="logout" @click="onLogout" />
    </template>
    <q-btn v-if="!hasLogout" flat round dense icon="" class="invisible" />
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
