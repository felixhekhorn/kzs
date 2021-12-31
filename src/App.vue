<script>
  import {
    mapState
  } from 'vuex'
  import GamesList from "./components/List/GamesList.vue";
  import GameView from "./components/GameView.vue"

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
        get () {
          return this.$store.state.currentUser.id
        },
        set (value) {
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
      GamesList,
      GameView
    },
    created: function () {
      this.$store.dispatch("open");
    }
  }
</script>

<template>
  <div v-if="has_server">
    Spieler: <input type="number" v-model="user_id" />
    <div v-if="currentError">{{currentError}}</div>
    <div v-if="state == 'listGames'">
      <button @click="loadGames()">Spiele laden</button>
      <GamesList />
    </div>
    <div v-else-if="state == 'showGame'">
      <button @click="listGames()">Zurück</button>
      <GameView />
    </div>
  </div>
  <div v-else>
    WebSocket-Server nicht verfügbar!
  </div>
</template>

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
