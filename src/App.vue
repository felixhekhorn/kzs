<template>
  <div v-if="has_server">
    <HeaderView />
    <ErrorView />
    <component :is="currentComponent" />
  </div>
  <div v-else>
    WebSocket-Server nicht verfügbar!
  </div>
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
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: black;
  }
</style>
