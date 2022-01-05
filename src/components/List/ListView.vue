<template>
  <ListHead />
  <div v-if="hasGames" >
    <q-list separator >
      <template v-for="game in games" :key="game.id" >
        <GameHeadView :game="game" mode="list" />
      </template>
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
  import ListHead from "./ListHead.vue";
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
      ListHead,
    },
  }
</script>

<style scoped>
  .GamesList {
    text-align: left;
  }
</style>
