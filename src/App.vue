<script>
  export default {
    name: 'App',
    data: function () {
      return {
        connection: null,
        user_id: 1,
        has_server: false,
        myGames: [],
        myParticipations: [],
      }
    },
    methods: {
      loadGames: function () {
        this.send({
          "type": "loadGames",
          "user_id": this.user_id
        });
      },
      send: function (data) {
        this.connection.send(JSON.stringify(data));
      },
      parse: function (res) {
        if (res.type == "loadedGames") {
          this.myGames = res.myGames;
          this.myParticipations = res.myParticipations;
        }
      },
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
    Spieler: <input type="number" v-model="user_id" />
    <button @click="loadGames()">Spiele laden</button>
    <div>Als Spielleiter</div>
    <ul v-for="game in myGames" :key="game.id">
      <li>{{game.title}}</li>
    </ul>
    <div>Als Teilnehmer</div>
    <ul v-for="game in myParticipations" :key="game.id">
      <li>{{game.title}}</li>
    </ul>
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
