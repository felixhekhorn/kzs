<script>
  export default {
    name: 'App',
    data: function () {
      return {
        connection: null,
        has_server: false,
        games: [],
      }
    },
    methods: {
      loadGames: function () {
        this.send({
          "type": "loadGames"
        });
      },
      send: function (data) {
        this.connection.send(JSON.stringify(data));
      },
      parse: function (res) {
        if (res.type == "loadedGames") {
          this.games = res.games;
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
    <button @click="loadGames()">Spiele laden</button>
    <ul v-for="game in games" :key="game.id">
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
