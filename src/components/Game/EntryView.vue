<template>
      <div class="Entry">
        <span>{{users[entry.user_id].name}} um {{ctime.format("DD.MM.YY HH:mm")}}</span>
        <p :style="style">{{entry.body}}</p>
      </div>
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
      "style": Object
    },
    computed: {
      ctime() {
        return dayjs(this.entry.ctime)
      },
      ...mapState({
        users: "users",
      })
    },
    methods: {
    }
  }
</script>

<style scoped>
</style>
