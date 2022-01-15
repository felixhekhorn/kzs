<template>
  <div class="q-mb-sm">
    <q-btn-group rounded>
      <q-btn
        rounded
        icon="add"
        label="Neu"
        :color="showingNew ? 'primary' : 'white'"
        :text-color="showingNew ? 'white' : 'black'"
        @click="onShowNew"
      />
      <q-btn
        rounded
        icon="link"
        label="Beitreten"
        :color="showingJoin ? 'primary' : 'white'"
        :text-color="showingJoin ? 'white' : 'black'"
        @click="onShowJoin"
      />
      <q-btn rounded icon="refresh" label="Aktualisieren" @click="loadGames" />
    </q-btn-group>
    <div v-if="showingNew">
      <q-input v-model="newTitle" placeholder="Spieltitel">
        <template v-slot:append>
          <q-btn @click="onNewGame" round icon="send" />
        </template>
      </q-input>
    </div>
    <div v-if="showingJoin">
      <q-input v-model="joinSlug" placeholder="Spielkennung">
        <template v-slot:prepend>
          <q-icon round name="key" />
        </template>
        <template v-slot:append>
          <q-btn @click="onJoinGame" round icon="search" />
        </template>
      </q-input>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showingNew: false,
      showingJoin: false,
      newTitle: "",
      joinSlug: "",
    };
  },
  methods: {
    onNewGame() {
      this.newTitle = this.newTitle.trim();
      if (this.newTitle) this.$store.dispatch("newGame", this.newTitle);
      this.newTitle = "";
    },
    onJoinGame() {
      this.joinSlug = this.joinSlug.trim();
      if (this.joinSlug) this.$store.dispatch("joinGame", this.joinSlug);
      this.joinSlug = "";
    },
    onShowNew() {
      this.showingNew = !this.showingNew;
    },
    onShowJoin() {
      this.showingJoin = !this.showingJoin;
    },
    loadGames() {
      this.$store.dispatch("loadGames");
    },
  },
};
</script>

<style scoped></style>
