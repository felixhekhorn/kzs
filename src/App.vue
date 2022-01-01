<template>
  <div v-if="has_server">
    Spieler: <input type="number" v-model="user_id" />
    <div v-if="currentError">{{currentError}}</div>
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
  import ListView from "./components/List/ListView.vue";
  import GameView from "./components/Game/GameView.vue"

  // https://github.com/AykutSarac/chatify

  export default {
    computed: {
      ...mapState([
        "has_server", "currentError", "state"
      ]),
      user_id: {
        get() {
          return this.$store.state.currentUser.id
        },
        set(value) {
          this.$store.commit('setUserId', value)
        }
      },
      currentComponent() {
        if (this.state == "showGame")
          return GameView;
        return ListView;
      }
    },
    methods: {
      loadGames() {
        this.$store.dispatch("loadGames");
      },
      listGames() {
        this.$store.commit("listGames");
      },
    },
    created: function () {
      this.$store.dispatch("open");
    }
  }
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
