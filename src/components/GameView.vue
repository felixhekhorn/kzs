<template>
  <div class="GameView">
    <h1>{{game.title}}</h1>
    <div class="entries">
      <div v-for="entry in game.entries" :key="entry.id" class="Entry">
        <span>{{users[entry.user_id].name}}</span>
        <p :style="entryBodyStyles[entry.id]">{{entry.body}}</p>
      </div>
      <div v-if="game.next_player_user_id == user.id">
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

  export default {
    data() {
      return {
        message: ""
      }
    },
    props: {},
    computed: {
      entryBodyStyles() {
        let styles = {};
        this.game.entries.forEach(e => {
          styles[e.id] = {
            "display": "none"
          }
        });
        // show last
        if (this.game.entries.length > 0 && this.game.next_player_user_id == this.user.id) {
          const le = this.game.entries[this.game.entries.length - 1];
          styles[le.id].display = "visible";
        }
        return styles;
      },
      ...mapState({
        users: "users",
        game: "currentGame",
        user: "currentUser"
      })
    },
    methods: {
      addEntry() {
        this.message = this.message.trim();
        if (this.message)
          this.$store.dispatch('addEntry', this.message);
        this.message = "";
      }
    }
  }
</script>

<style scoped>
</style>
