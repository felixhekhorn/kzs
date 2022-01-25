<template>
  <q-layout view="lHh Lpr fFf">
    <q-header elevated class="glossy text-center">
      <HeaderView />
    </q-header>

    <q-page-container>
      <div class="q-pa-md row justify-center">
        <div v-if="has_server" class="page">
          <ErrorView />
          <component :is="currentComponent" />
        </div>
        <div v-else>
          <NoServerView />
        </div>
      </div>
    </q-page-container>

    <q-footer class="glossy text-center q-pa-sm items-center">
      &copy; F. Hekhorn 2021-2022
      <a target="_blank" href="https://github.com/felixhekhorn/kzs"
        ><img
          src="img/GitHub-Mark-32px.png"
          alt="GitHub"
          style="max-height: 17px; vertical-align: text-bottom"
      /></a>
      v{{ version }}
    </q-footer>
  </q-layout>
</template>

<script>
import { mapState } from "vuex";

import NoServerView from "./components/Layout/NoServerView.vue";
import HeaderView from "./components/Layout/HeaderView.vue";
import ErrorView from "./components/ErrorView.vue";
import LoginView from "./components/LoginView.vue";
import ListView from "./components/List/ListView.vue";
import GameView from "./components/Game/GameView.vue";

// https://github.com/AykutSarac/chatify

export default {
  computed: {
    ...mapState(["has_server", "state"]),
    currentComponent() {
      if (this.state == "showGame") return GameView;
      if (this.state == "listGames") return ListView;
      return LoginView;
    },
    version() {
      return process.env.VUE_APP_VERSION;
    },
  },
  beforeCreate() {
    this.$store.commit("readFromSession");
  },
  created() {
    this.$store.dispatch("open");
  },
  components: {
    ErrorView,
    HeaderView,
    NoServerView,
  },
};
</script>

<style scoped lang="scss">
@import "styles/quasar.variables.scss";

.page {
  width: 100%;
  max-width: $layout-max-width;
}
</style>
