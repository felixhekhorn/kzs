<template>
  <q-chat-message
    :name="users[entry.user_id].name"
    :text="body"
    v-bind="sent"
    :stamp="$d(ctime.toDate(), 'full')"
  />
</template>

<script>
import { mapState } from "vuex";

import dayjs from "../../utils/myDayJS";

export default {
  props: {
    entry: Object,
    visible: Boolean,
  },
  computed: {
    ctime() {
      return dayjs.utc(this.entry.ctime + "Z");
    },
    body() {
      return this.visible ? [this.entry.body] : ["..."];
    },
    sent() {
      return this.entry.user_id == this.currentUser.id ? { sent: true } : {};
    },
    ...mapState(["users", "currentUser"]),
  },
  methods: {},
};
</script>

<style scoped></style>
