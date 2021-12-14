<template>
  <div class="GameView">
    <h1>{{game.title}}</h1>
    <div>
      <div v-for="entry in game.entries" :key="entry.id">
        <span>{{entry.user.name}}</span>
        <p>{{entry.body}}</p>
      </div>
      <div>
        <textarea v-model="message"></textarea>
        <button @click="addEntry">Senden</button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    emits: ["addEntry"],
    data() {
      return {
        message: "Bla"
      }
    },
    props: {
      game: Object,
    },
    methods: {
      addEntry() {
        this.message = this.message.trim()
        if (this.message)
          this.$emit('addEntry', this.game.id, this.message);
      }
    }
  }
</script>

<style scoped>
</style>
