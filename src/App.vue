<script>
  import {
    mapState
  } from 'vuex'
  import GamesList from "./components/GamesList.vue";
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
      /*
      listGames: function () {
        this.state = "listGames";
        this.currentGame = null;
      },
      openGame: function (game) {
        this.state = "showGame";
        this.currentGame = game;
      },
      setGames: function (res) {
        this.games = {
          ...this.games,
          ...res.games
        };
        this.users = {
          ...this.user,
          ...res.users
        };
      },
      addEntry: function (game_id, msg) {
        this.send({
          "type": "addEntry",
          "user_id": this.currentUser.id,
          "game_id": game_id,
          "body": msg
        })
      },
      setEntry: function (res) {
        const g = this.games[res.Entry.game_id];
        g.entries.push(res.Entry);
        g.next_player_user_id = res.next_player_user_id;
        const scrollBottom = () => {
          if (this.state != "showGame" || this.currentGame.id != g.id)
            return;
          const es = document.getElementsByClassName('Entry');
          if (es.length <= 0)
            return;
          const lastEntry = es[es.length - 1];
          lastEntry.scrollIntoView();
        };
        scrollBottom();
      },
      send: function (data) {
        this.connection.send(JSON.stringify(data));
      },
      parse: function (res) {
        this.currentError = ""
        if (res.type == "error") {
          this.currentError = res.body;
          return;
        }
        if (res.type == "loadedGames")
          return this.setGames(res);
        if (res.type == "addEntry")
          return this.setEntry(res);
      },*/
    },
    components: {
      GamesList,
      GameView
    },
    created: function () {
      /*
            // Establish connection via WebSocket
            this.connection = new WebSocket("ws://localhost:8001");
            // parse answer
            this.connection.addEventListener('message', (event) => {
              //console.log('Message from server: ', event.data);
              const res = JSON.parse(event.data);
              if (res.type)
                this.parse(res);
            });
            // notify in browser
            this.connection.addEventListener('open', () => {
              this.has_server = true;
            });*/
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
