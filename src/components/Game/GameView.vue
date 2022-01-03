<template>
  <div class="GameView">
    <h1>{{game.title}}</h1>
    <div>
      <PlayerList :game="game" />
      <button v-if="canEnd" @click="onEnd">Beenden</button>
    </div>
    <div class="entries">
      <div v-for="entry in game.entries" :key="entry.id" class="Entry">
        <EntryView :entry="entry" :visible="visibles[entry.id]" />
      </div>
      <div v-if="canSend">
        <textarea v-model="message" placeholder="und dann geschah etwas Seltsames:"></textarea>
        <button @click="addEntry">Senden</button>
      </div>
    </div>
  </div>
</template>

<script>
  import {
    mapState
  } from 'vuex'

  import EntryView from "./EntryView.vue"
  import PlayerList from "../PlayerList.vue"

  export default {
    data() {
      return {
        message: ""
      }
    },
    computed: {
      visibles() {
        let styles = {};
        // set default for most
        this.game.entries.forEach(e => {
          styles[e.id] = this.game.state == "finished"
        });
        // show eventually last
        if (this.game.entries.length > 0 && this.canSend) {
          const le = this.game.entries[this.game.entries.length - 1];
          styles[le.id] = true;
        }
        return styles;
      },
      canSend() {
        return this.game.next_player_user_id == this.currentUser.id && this.game.state != "finished"
      },
      canEnd() {
        return this.game.user_id == this.currentUser.id && this.game.state == "running"
      },
      game() {
        return this.games[this.currentGameId];
      },
      ...mapState(["currentUser", "currentGameId", "games"])
    },
    methods: {
      addEntry() {
        this.message = this.message.trim();
        if (this.message)
          this.$store.dispatch("addEntry", this.message);
        this.message = "";
      },
      onEnd() {
        this.$store.dispatch("endGame");
      },
    },
    components: {
      EntryView,
      PlayerList,
    }
  }
</script>

<style scoped>
</style>
