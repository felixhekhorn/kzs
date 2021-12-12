<template>
  <div class="List">
    <div v-for="game in games" :key="game.id" >
      <div>
        <h2 class="title" >{{game.title}}</h2>
        <span class="numEntries" >{{game.entries.length}} Beiträge</span>
      </div>
      <div class="players" >
        Mitspieler:
        <span v-for="player in game.players" :key="player.id" class="Player" >{{player.user.name}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    games: Array,
  }
}
</script>

<style scoped>
.List {
  text-align: left;
}
.Player::after {
  content: ", "
}
</style>
