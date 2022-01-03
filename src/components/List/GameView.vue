<template>
  <q-item-section top avatar>
    <q-avatar :icon="avatar" />
  </q-item-section>
  <q-item-section>
    <q-item-label>{{game.title}}</q-item-label>
    <q-item-label caption lines="1">
      <PlayerList :game="game" /> <span class="slug">{{game.slug}}</span>
    </q-item-label>
  </q-item-section>
  <!--<div>
    <h2 class="title">{{game.title}}</h2>
    <span class="numEntries">{{game.entries.length}} Beiträge - vom
      {{ctime.format("DD.MM.YY HH:mm")}}</span>
    <button v-if="game.state != 'init'" @click="onOpenGame">Öffnen</button>
    <button v-if="canStart" @click="onStartGame">Starten</button>
    <div>
      <PlayerList :game="game" /> <span class="slug">{{game.slug}}</span></div>
  </div>-->
</template>

<script>
  import {
    mapState
  } from 'vuex';

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
      avatar() {
        if (this.game.state == "running")
          return "play_arrow";
        if (this.game.state == "init")
          return "not_started";
        if (this.game.state == "finished")
          return "flag";
        return "";
      },
      canStart() {
        return this.game.state == 'init' && this.game.next_player_user_id == this.currentUser.id && this.game.players
          .length >= 3
      },
      ...mapState(["currentUser"])
    },
    methods: {
      onOpenGame() {
        this.$store.commit("openGame", this.game.id);
      },
      onStartGame() {
        this.$store.dispatch("startGame", this.game.id);
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

  .slug {
    font-family: monospace;
  }
</style>
