<script>
  import GamesList from "./components/GamesList.vue";
  import GameView from "./components/GameView.vue"

  // https://github.com/AykutSarac/chatify

  export default {
    data: function () {
      return {
        connection: null,
        has_server: false,
        currentError: "",
        currentUser: {
          "id": 1
        },
        myGames: [],
        myParticipations: [],
        state: "listGames",
        currentGame: null,
      }
    },
    methods: {
      loadGames: function () {
        this.send({
          "type": "loadGames",
          "user_id": this.currentUser.id
        });
      },
      listGames: function () {
        this.state = "listGames";
        this.currentGame = null;
      },
      openGame: function (game) {
        this.state = "showGame";
        this.currentGame = game;
      },
      addEntry: function (game_id, msg) {
        this.send({
          "type": "addEntry",
          "user_id": this.currentUser.id,
          "game_id": game_id,
          "body": msg
        })
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
        if (res.type == "loadedGames") {
          this.myGames = res.myGames;
          this.myParticipations = res.myParticipations;
          return;
        }
      },
    },
    components: {
      GamesList,
      GameView
    },
    created: function () {
      // Establish connection via WebSocket
      this.connection = new WebSocket("ws://localhost:8001");
      // parse answer
      this.connection.addEventListener('message', (event) => {
        console.log('Message from server: ', event.data);
        const res = JSON.parse(event.data);
        if (res.type)
          this.parse(res);
      });
      // notify in browser
      this.connection.addEventListener('open', () => {
        this.has_server = true;
      });
    }
  }
</script>

<template>
  <div v-if="has_server">
    Spieler: <input type="number" v-model="currentUser.id" />
    <div v-if="currentError">{{currentError}}</div>
    <div v-if="state == 'listGames'">
      <button @click="loadGames()">Spiele laden</button>
      <h1>Als Spielleiter</h1>
      <GamesList @open-game="openGame" :games="myGames" />
      <h1>Als Teilnehmer</h1>
      <GamesList @open-game="openGame" :games="myParticipations" />
    </div>
    <div v-else-if="state == 'showGame'">
      <button @click="listGames()">Zurück</button>
      <GameView @add-entry="addEntry" :game="currentGame" />
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
