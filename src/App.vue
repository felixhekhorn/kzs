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
      <FooterView />
    </q-footer>
  </q-layout>
</template>

<script>
import { mapState } from "vuex";

import NoServerView from "./components/Layout/NoServerView.vue";
import HeaderView from "./components/Layout/HeaderView.vue";
import FooterView from "./components/Layout/FooterView.vue";
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
  },
  beforeCreate() {
    this.$store.commit("readFromSession");
    const currentLocal = sessionStorage.getItem("currentLocal");
    if (currentLocal) this.$i18n.locale = currentLocal;
  },
  created() {
    this.$store.dispatch("open");
  },
  components: {
    ErrorView,
    HeaderView,
    NoServerView,
    FooterView,
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
