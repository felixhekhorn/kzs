<template>
  <div>
    <input v-model="user_name" placeholder="Benutzername" />
    <input v-model="user_password" placeholder="Passwort" />
    <button @click="onLogin">Anmelden</button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        user_name: "",
        user_password: ""
      };
    },
    methods: {
      onLogin() {
        this.user_name = this.user_name.trim()
        this.user_password = this.user_password.trim()
        if (!this.user_name || !this.user_password)
          return;
        this.$store.dispatch("login", {
          user_name: this.user_name,
          user_password: this.user_password
        });
      }
    }
  }
</script>

<style>
</style>
