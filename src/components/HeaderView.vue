<template>
<div class="header" >
  <div v-if="hasLogout" class="logout">
    Angemeldet als {{currentUser.name}}
    <button @click="onLogout">Abmelden</button>
  </div>
  <div v-if="hasBack" class="back"><button @click="onBack">zurück</button></div>
<div class="clearer" ></div>
  </div>
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
.back {
  text-align: left;
}
.logout {
  width: 80%;
  float: right;
  text-align: right;
}

.clearer {
  clear: right;
}
</style>
