<template>
  <div>
    <h2 class="title">{{game.title}}</h2>
    <span class="numEntries">{{game.entries.length}} Beiträge - vom
      {{ctime.format("DD.MM.YY HH:mm")}}</span>
    <button v-if="game.state != 'init'" @click="onOpenGame">Öffnen</button>
    <button v-if="game.state == 'init'" @click="onStartGame">Starten</button>
    <PlayerList :game="game" />
  </div>
</template>

<script>
  import dayjs from 'dayjs';
  import 'dayjs/locale/de';
  dayjs.locale('de');

  import PlayerList from "../PlayerList.vue"

  export default {
    props: {
      game: Object,
    },
    computed: {
      ctime() {
        return dayjs(this.game.ctime)
      },
    },
    methods: {
      onOpenGame() {
        this.$store.commit("openGame", this.game);
      },
      onStartGame() {
        this.$store.dispatch("startGame", this.game);
      },
    },
    components: {
      PlayerList
    }
  }
</script>

<style scoped>
  .GamesList {
    text-align: left;
  }
</style>
