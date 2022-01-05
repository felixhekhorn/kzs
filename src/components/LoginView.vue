<template>
  <q-list bordered class="rounded-borders">
    <q-expansion-item group="login_type" expand-separator icon="account_circle" label="Login" default-opened>
      <q-card>
        <q-card-section>
          <q-input v-model="user_name" placeholder="Benutzername">
            <template v-slot:prepend>
              <q-icon round name="account_circle" />
            </template>
          </q-input>
          <q-input v-model="user_password" :type="showPassword ? 'password' : 'text'" placeholder="Passwort">
            <template v-slot:prepend>
              <q-icon round name="password" />
            </template>
            <template v-slot:append>
              <q-icon :name="showPassword ? 'visibility_off' : 'visibility'" @click="showPassword = !showPassword" />
            </template>
          </q-input>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn @click="onLogin" icon-right="login">Anmelden</q-btn>
        </q-card-actions>
      </q-card>
    </q-expansion-item>
    <q-expansion-item group="login_type" expand-separator icon="person_add" label="Registrieren">
      <q-card>
        <q-card-section>
          <q-input v-model="user_name" placeholder="Benutzername">
            <template v-slot:prepend>
              <q-icon round name="account_circle" />
            </template>
          </q-input>
          <q-input v-model="user_password_1" :type="showPassword1 ? 'password' : 'text'" placeholder="Passwort">
            <template v-slot:prepend>
              <q-icon round name="password" />
            </template>
            <template v-slot:append>
              <q-icon :name="showPassword1 ? 'visibility_off' : 'visibility'" @click="showPassword1 = !showPassword1" />
            </template>
          </q-input>
          <q-input v-model="user_password_2" :type="showPassword2 ? 'password' : 'text'" placeholder="Passwort">
            <template v-slot:prepend>
              <q-icon round name="password" />
            </template>
            <template v-slot:append>
              <q-icon :name="showPassword2 ? 'visibility_off' : 'visibility'" @click="showPassword2 = !showPassword2" />
            </template>
          </q-input>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn icon-right="login" @click="onRegister">Registrieren</q-btn>
        </q-card-actions>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>

<script>
  export default {
    data() {
      return {
        user_name: "",
        user_password: "",
        user_password_1: "",
        user_password_2: "",
        showPassword: true,
        showPassword1: true,
        showPassword2: true,
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
      },
      onRegister() {
        this.user_name = this.user_name.trim()
        // sanitazation is on the other side
        this.$store.dispatch("newUser", {
          user_name: this.user_name,
          user_password_1: this.user_password_1,
          user_password_2: this.user_password_2,
        });
      }
    }
  }
</script>

<style>
</style>
