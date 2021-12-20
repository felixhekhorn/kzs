<template>
  <div class="GamesList">
    <div v-for="game in games" :key="game.id">
      <GamesListItem :game="game" :users="users" />
    </div>
  </div>
</template>

<script>
  import GamesListItem from "./GamesListItem.vue";

  export default {
    emits: ['openGame'],
    props: {
      games: Object,
      users: Object,
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
