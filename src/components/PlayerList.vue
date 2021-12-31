<template>
    Mitspieler:
    <span v-for="player in game.players" :key="player.id"
      :class="playerClasses[player.id]">{{users[player.user_id].name}}</span>
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
      ]),
      playerClasses(){
        let classes = {};
        this.game.players.forEach(p => {
          let cls = ['Player'];
          if (this.game.state != "finished" && this.game.next_player_user_id == p.user_id)
            cls = [...cls, 'ActivePlayer'];
          classes[p.id] = cls;
        });
        return classes;
      }
    },
    methods: {
    }
  }
</script>

<style scoped>
  .Player::after {
    content: ", "
  }

  .Player.ActivePlayer {
    font-weight: bold;
  }
</style>
