<template>
  <div class="GamesList">
    <div v-for="game in games" :key="game.id">
      <div>
        <h2 class="title">{{game.title}}</h2>
        <span class="numEntries">{{game.entries.length}} Beiträge</span>
        <button @click="$emit('openGame', game)">Öffnen</button>
      </div>
      <div class="players">
        Mitspieler:
        <span v-for="player in game.players" :key="player.id" class="Player">{{player.user.name}}</span>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    emits: ['openGame'],
    props: {
      games: Array,
    }
  }
</script>

<style scoped>
  .GamesList {
    text-align: left;
  }

  .Player::after {
    content: ", "
  }
</style>
