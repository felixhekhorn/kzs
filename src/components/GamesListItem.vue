<template>
  <div>
    <h2 class="title">{{game.title}}</h2>
    <span class="numEntries">{{game.entries.length}} Beiträge - vom
      {{gameCTime.format("DD.MM.YY HH:II")}}</span>
    <button @click="onOpenGame">Öffnen</button>
  </div>
  <div class="players">
    Mitspieler:
    <span v-for="player in game.players" :key="player.id" class="Player">{{users[player.user_id].name}}</span>
  </div>
</template>

<script>
  import {
    mapState
  } from 'vuex';

  import dayjs from 'dayjs';
  import 'dayjs/locale/de';
  dayjs.locale('de');

  export default {
    props: {
      game: Object,
    },
    computed: {
      gameCTime() {
        return dayjs(this.game.ctime)
      },
      ...mapState([
        "users"
      ])
    },
    methods: {
      onOpenGame() {
        this.$store.commit("openGame", this.game);
      }
    }
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
