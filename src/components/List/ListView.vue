<template>
  <div><button @click="loadGames()">Spiele laden</button></div>
  <AddGame />
  <div v-if="hasGames" class="q-pa-md" style="max-width: 550px">
    <q-list padding>
      <q-item v-for="game in games" :key="game.id">
        <GameView :game="game" />
      </q-item>
    </q-list>
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
