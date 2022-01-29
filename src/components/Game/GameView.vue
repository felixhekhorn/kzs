<template>
  <div class="GameView">
    <div class="entries">
      <div v-for="entry in game.entries" :key="entry.id" class="Entry">
        <EntryView :entry="entry" :visible="visibles[entry.id]" />
      </div>
      <div v-if="canSend">
        <q-input
          v-model="message"
          autogrow
          :placeholder="$t(inputPlaceholderKey)"
          @keyup="onKeyUp"
        >
          <template v-slot:append>
            <q-btn @click="addEntry" round icon="send" />
          </template>
        </q-input>
      </div>
    </div>
    <q-page-sticky expand position="top">
      <q-list class="gameHeadList bg-white text-center">
        <GameHeadView :game="game" mode="show" />
      </q-list>
    </q-page-sticky>
  </div>
</template>

<script>
import { mapState } from "vuex";

import EntryView from "./EntryView.vue";
import GameHeadView from "../GameHeadView.vue";

export default {
  data() {
    return {
      message: "",
    };
  },
  computed: {
    visibles() {
      let styles = {};
      // set default for most
      this.game.entries.forEach((e) => {
        styles[e.id] = this.game.state == "finished";
      });
      // show eventually last
      if (this.game.entries.length > 0 && this.canSend) {
        const le = this.game.entries[this.game.entries.length - 1];
        styles[le.id] = true;
      }
      return styles;
    },
    canSend() {
      return (
        this.game.next_player_user_id == this.currentUser.id &&
        this.game.state != "finished"
      );
    },
    inputPlaceholderKey() {
      if (this.game.entries.length == 0) return "placeholder-start";
      return "placeholder-continue";
    },
    game() {
      return this.games[this.currentGameId];
    },
    ...mapState(["currentUser", "currentGameId", "games"]),
  },
  methods: {
    addEntry() {
      this.message = this.message.trim();
      if (this.message) {
        sessionStorage.setItem("lastEntryBody", this.message);
        this.$store.dispatch("addEntry", this.message);
      }
      this.message = "";
    },
    onKeyUp() {
      sessionStorage.setItem("lastEntryBody", this.message.trim());
    },
  },
  created() {
    // restore last message in case the connection got lost
    const lastMsg = sessionStorage.getItem("lastEntryBody");
    if (lastMsg) this.message = lastMsg;
  },
  components: {
    EntryView,
    GameHeadView,
  },
};
</script>

<style scoped lang="scss">
@import "../../styles/quasar.variables.scss";

.gameHeadList {
  width: 100%;
  max-width: $layout-max-width;
}

.entries {
  padding-top: 57px;
}
</style>
