<template>
    Mitspieler:
    <span v-for="player in game.players" :key="player.id"
      :class="['Player', game.next_player_user_id == player.user_id ? 'Active' : '']">{{users[player.user_id].name}}</span>
</template>

<script>
  import {
    mapState
  } from 'vuex';

  export default {
    props: {
      game: Object,
    },
    computed: {
      ...mapState([
        "users"
      ])
    },
    methods: {
    }
  }
</script>

<style scoped>
  .Player::after {
    content: ", "
  }

  .Player.Active {
    font-weight: bold;
  }
</style>
