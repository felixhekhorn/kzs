<template>
  <div class="GameView">
    <div class="entries">
      <div v-for="entry in game.entries" :key="entry.id" class="Entry">
        <EntryView :entry="entry" :visible="visibles[entry.id]" />
      </div>
      <div v-if="canSend">
        <q-input v-model="message" autogrow placeholder="und dann geschah etwas Seltsames:">
          <template v-slot:append>
            <q-btn @click="addEntry" round icon="send" />
          </template>
        </q-input>
      </div>
    </div>
    <q-page-sticky expand position="top">
      <q-list style="width:100%;" class="bg-white text-center">
        <q-item>
          <GameHeadView :game="game" mode="show" />
        </q-item>
      </q-list>
    </q-page-sticky>
  </div>
</template>

<script>
  import {
    mapState
  } from 'vuex'

  import EntryView from "./EntryView.vue"
  import GameHeadView from "../GameHeadView.vue"

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
    },
    components: {
      EntryView,
      GameHeadView,
    }
  }
</script>

<style scoped>
  .entries {
    padding-top: 57px;
  }
</style>
