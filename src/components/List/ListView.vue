<template>
  <div><button @click="loadGames()">Spiele laden</button></div>
  <AddGame />
  <div v-if="hasGames" class="GamesList">
    <div v-for="game in games" :key="game.id">
      <div class="players">
        <GameView :game="game" />
      </div>
    </div>
  </div>
  <div v-else class="">
    Keine Spiele gefunden.
  </div>
</template>

<script>
  import {
    mapState
  } from 'vuex';
  import GameView from "./GameView.vue";
  import AddGame from "./AddGame.vue";
  import isObjectEmpty from "../../lib/isObjectEmpty.js"

  export default {
    props: {},
    mixins: [isObjectEmpty],
    computed: {
      ...mapState([
        "games"
      ]),
      hasGames() {
        return !this.isObjectEmpty(this.games);
      }
    },
    components: {
      GameView,
      AddGame,
    },
    methods: {
      loadGames() {
        this.$store.dispatch("loadGames");
      },
    },
  }
</script>

<style scoped>
  .GamesList {
    text-align: left;
  }
</style>
