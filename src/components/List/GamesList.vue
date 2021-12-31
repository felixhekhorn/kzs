<template>
  <AddGame />
  {{hasGames}}
  <div v-if="games" class="GamesList">
    <div v-for="game in games" :key="game.id">
      <div class="players">
        <ListItem :game="game" />
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
  import ListItem from "./ListItem.vue";
  import AddGame from "./AddGame.vue";

  export default {
    props: {},
    computed: {
      ...mapState([
        "games"
      ]),
      hasGames() {
        return true;
      }
    },
    components: {
      ListItem,
      AddGame,
    },
  }
</script>

<style scoped>
  .GamesList {
    text-align: left;
  }
</style>
