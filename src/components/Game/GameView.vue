<template>
  <div class="GameView">
    <h1>{{game.title}}</h1>
    <div class="players">
      <PlayerList :game="game" />
    </div>
    <div class="entries">
      <div v-for="entry in game.entries" :key="entry.id" class="Entry">
        <EntryView :entry="entry" :style="entryBodyStyles[entry.id]" />
      </div>
      <div v-if="game.next_player_user_id == user.id && game.state != 'finished'">
        <textarea v-model="message" placeholder="und dann geschah etwas Seltsames:"></textarea>
        <button @click="addEntry">Senden</button>
      </div>
    </div>
  </div>
</template>

<script>
  import {
    mapState
  } from 'vuex';

  import EntryView from "./EntryView.vue";
  import PlayerList from "../PlayerList.vue";

  export default {
    data() {
      return {
        message: ""
      }
    },
    props: {
      "id": String,
    },
    computed: {
      entryBodyStyles() {
        let styles = {};
        // set default for most
        this.game.entries.forEach(e => {
          styles[e.id] = {
            "display": this.game.state == "finished" ? "visible" : "none"
          }
        });
        // show eventually last
        if (this.game.entries.length > 0 && this.game.next_player_user_id == this.user.id && this.game.state !=
          'finished') {
          const le = this.game.entries[this.game.entries.length - 1];
          styles[le.id].display = "visible";
        }
        return styles;
      },
      ...mapState({
        user: "currentUser",
        game: "currentGame",
      })
    },
    methods: {
      addEntry() {
        this.message = this.message.trim();
        if (this.message)
          this.$store.dispatch('addEntry', this.message);
        this.message = "";
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
