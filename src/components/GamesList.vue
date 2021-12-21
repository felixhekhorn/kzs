<template>
  <div class="GamesList">
    <div v-for="game in games" :key="game.id">
      <GamesListItem :game="game" />
    </div>
  </div>
</template>

<script>
  import {
    mapState
  } from 'vuex';
  import GamesListItem from "./GamesListItem.vue";

  export default {
    props: {},
    computed: {
      ...mapState([
        "games"
      ])
    },
    components: {
      GamesListItem,
    },
  }
</script>

<style scoped>
  .GamesList {
    text-align: left;
  }

  .Player::after {
    content: ", "
  }
</style>
