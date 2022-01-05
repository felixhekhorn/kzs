<template>
  <q-item @click="onClick" clickable>
    <q-item-section top avatar dense>
      <q-avatar :icon="avatar" />
    </q-item-section>
    <q-item-section>
      <q-item-label>{{game.title}}</q-item-label>
      <q-item-label caption lines="1">
        <PlayerList :game="game" />
        <q-icon name="article" />&nbsp;{{game.entries.length}}
        <q-icon name="event" />&nbsp;{{ctime.format("DD.MM.YY HH:mm")}}
      </q-item-label>
    </q-item-section>
    <template v-if="mode=='list'">
      <q-item-section side top>
        <q-btn v-if="canStart" @click="onStart" round icon="start" />
      </q-item-section>
    </template>
    <q-item-section side top>
      <q-btn v-if="canShare" @click="onShare" round icon="share" />
    </q-item-section>
    <q-item-section v-if="mode=='show' && canEnd" side top>
      <q-btn @click="onEnd" round icon="flag" />
    </q-item-section>
  </q-item>
</template>

<script>
  import {
    mapState
  } from 'vuex';

  import dayjs from 'dayjs';
  import 'dayjs/locale/de';
  dayjs.locale('de');

  import PlayerList from "./PlayerList.vue"

  export default {
    props: {
      game: Object,
      mode: String
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
        return this.game.state == 'init' && this.game.user_id == this.currentUser.id && this.game.players
          .length >= 3
      },
      canOpen() {
        return this.game.state != 'init';
      },
      canShare() {
        return this.game.state != 'finished';
      },
      canEnd() {
        return this.game.user_id == this.currentUser.id && this.game.state == "running"
      },
      ...mapState(["currentUser"])
    },
    methods: {
      onStart() {
        this.$store.dispatch("startGame", this.game.id);
      },
      onShare() {},
      onEnd() {
        this.$store.dispatch("endGame");
      },
      onClick(){
        if (this.mode == "list" && this.canOpen)
          this.$store.commit("openGame", this.game.id);
      },
    },
    components: {
      PlayerList
    }
  }
</script>

<style scoped>
</style>
