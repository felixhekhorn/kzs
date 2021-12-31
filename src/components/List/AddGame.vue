<template>
  <div class="AddGame">
    <div><button>Neues Spiel</button></div>
    <div><input v-model="joinSlug" placeholder="Spielkennung eingeben" /><button>Spiel beitreten</button></div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        joinSlug: ""
      }
    },
    props: {},
    computed: {
    },
    components: {
    },
  }
</script>

<style scoped>
</style>
