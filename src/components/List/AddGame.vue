<template>
  <div class="AddGame">
    <div><input v-model="newTitle" placeholder="Spieletitel" ><button @click="onNewGame" >Neues Spiel</button></div>
    <div><input v-model="joinSlug" placeholder="Spielkennung eingeben" /><button @click="onJoinGame">Spiel
        beitreten</button></div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        newTitle: "",
        joinSlug: ""
      }
    },
    props: {},
    computed: {},
    components: {},
    methods: {
      onNewGame(){
        this.newTitle = this.newTitle.trim();
        if (this.newTitle)
          this.$store.dispatch("newGame", this.newTitle);
        this.newTitle = "";
      },
      onJoinGame() {
        this.joinSlug = this.joinSlug.trim()
        if (this.joinSlug)
          this.$store.dispatch("joinGame", this.joinSlug);
        this.joinSlug = ""
      },
    },
  }
</script>

<style scoped>
</style>
