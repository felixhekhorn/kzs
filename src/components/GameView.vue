<template>
  <div class="GameView">
    <h1>{{game.title}}</h1>
    <div>
      <div v-for="entry in game.entries" :key="entry.id">
        <span>{{entry.user.name}}</span>
        <p>{{entry.body}}</p>
      </div>
      <div><textarea v-model="message" ></textarea></div>
    </div>
  </div>
</template>

<script>
  export default {
    emits: [],
    data() {
      return {
        message: "Bla"
      }
    },
    props: {
      game: Object,
    }
  }
</script>

<style scoped>
</style>
