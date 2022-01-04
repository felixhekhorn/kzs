<template>
  <div><button @click="loadGames()">Spiele laden</button></div>
  <AddGame />
  <div v-if="hasGames" >
    <q-list separator >
      <q-item v-for="game in games" :key="game.id" clickable >
        <GameHeadView :game="game" mode="list" />
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
  import GameHeadView from "../GameHeadView.vue";
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
      GameHeadView,
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
