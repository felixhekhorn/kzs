<template>
  <div v-if="has_server">
    Spieler: <input type="number" v-model="user_id" />
    <div v-if="currentError">{{currentError}}</div>
    <div v-if="state == 'listGames'">
      <ListView />
    </div>
    <div v-else-if="state == 'showGame'">
      <GameView />
    </div>
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
    data: function () {
      return {
        /*
                connection: null,
                has_server: false,
                currentError: "",
                currentUser: {
                  "id": 1
                },
                games: {},
                users: {},
                state: "listGames",
                currentGame: null,*/
      }
    },
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
    components: {
      ListView,
      GameView
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
