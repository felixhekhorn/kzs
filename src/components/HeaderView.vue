<template>
  <q-btn v-if="hasBack" flat round dense icon="arrow_back" @click="onBack" />
  <q-toolbar-title>
    Knickzettelspiel
  </q-toolbar-title>
  <div v-if="hasLogout" ><q-icon flat round dense name="account_circle" left=true />&nbsp;{{currentUser.name}}</div>
  <q-btn v-if="hasLogout" flat round dense icon="logout"  @click="onLogout" />
</template>

<script>
  import {
    mapState
  } from 'vuex'

  export default {
    computed: {
      ...mapState([
        "currentUser", "state"
      ]),
      hasBack() {
        return this.state == "showGame";
      },
      hasLogout() {
        return this.state != "login";
      },
    },
    methods: {
      onBack() {
        if (this.state == "showGame")
          return this.$store.commit("listGames");
      },
      onLogout(){
        if (this.state != "login") {
          this.$store.dispatch("logout");
          return this.$store.commit("logout");
        }
      }
    }
  }
</script>

<style scoped>
</style>
