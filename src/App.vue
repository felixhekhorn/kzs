<template>
  <q-layout view="lHh Lpr fFf">
    <q-header elevated class="glossy text-center">
      <q-toolbar>
        <HeaderView />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <div class="q-pa-md row justify-center"  >
        <div v-if="has_server" style="width: 100%; max-width: 550px" >
          <ErrorView />
          <component :is="currentComponent" />
        </div>
        <div v-else>
          WebSocket-Server nicht verfügbar!
        </div>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
  import {
    mapState
  } from 'vuex'

  import HeaderView from "./components/HeaderView.vue"
  import ErrorView from "./components/ErrorView.vue"
  import LoginView from "./components/LoginView.vue"
  import ListView from "./components/List/ListView.vue"
  import GameView from "./components/Game/GameView.vue"

  // https://github.com/AykutSarac/chatify

  export default {
    computed: {
      ...mapState([
        "has_server", "state", "currentUser"
      ]),
      currentComponent() {
        if (this.state == "showGame")
          return GameView;
        if (this.state == "listGames")
          return ListView;
        return LoginView;
      }
    },
    beforeCreate() {
      this.$store.commit('readFromSession');
    },
    created() {
      this.$store.dispatch("open");
    },
    components: {
      ErrorView,
      HeaderView
    }
  }
</script>

<style>
</style>
