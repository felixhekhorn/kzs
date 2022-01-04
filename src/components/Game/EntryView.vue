<template>
    <q-chat-message
        :name="users[entry.user_id].name"
        :text="body"
        v-bind="sent"
        :stamp="ctime.format('DD.MM.YY HH:mm')"
      />
</template>

<script>
  import {
    mapState
  } from 'vuex';

  import dayjs from 'dayjs';
  import 'dayjs/locale/de';
  dayjs.locale('de');

  export default {
    props: {
      "entry": Object,
      "visible": Boolean
    },
    computed: {
      ctime() {
        return dayjs(this.entry.ctime)
      },
      body(){
        return this.visible ? [this.entry.body] : ["..."];
      },
      sent(){
        return this.entry.user_id == this.currentUser.id ? {"sent": true} : {};
      },
      ...mapState(["users", "currentUser"])
    },
    methods: {}
  }
</script>

<style scoped>
</style>
