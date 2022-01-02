<template>
  <div v-if="currentError">{{currentError}}</div>
</template>

<script>
  import {
    mapState
  } from 'vuex'

  export default {
    computed: {
      ...mapState([
        "currentError"
      ]),
    },
  }
</script>

<style>
</style>
