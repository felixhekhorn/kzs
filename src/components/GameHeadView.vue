<template>
  <q-item @click="onClick" clickable>
    <q-item-section top avatar dense>
      <q-avatar :icon="avatar" />
    </q-item-section>
    <q-item-section>
      <q-item-label>{{ game.title }}</q-item-label>
      <q-item-label caption lines="2">
        <PlayerList :game="game" />
        <q-icon name="article" />&nbsp;{{ game.entries.length }}
        <q-icon name="event" />&nbsp;{{ ctime.format("DD.MM.YY HH:mm") }}
      </q-item-label>
    </q-item-section>
    <!-- start -->
    <template v-if="mode == 'list'">
      <q-item-section side top>
        <q-btn v-if="canStart" @click="onShowStart" round icon="start" />
        <q-dialog v-model="showStart">
          <q-card>
            <q-card-section class="row items-center">
              <q-avatar icon="play_arrow" color="primary" text-color="white" />
              <span class="q-ml-sm">{{
                $t("really-start", { title: game.title })
              }}</span>
            </q-card-section>
            <q-card-actions align="right">
              <q-btn :label="$t('cancel')" color="primary" v-close-popup />
              <q-btn
                :label="$t('start')"
                color="primary"
                @click="onStart"
                v-close-popup
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </q-item-section>
    </template>
    <!-- end -->
    <q-item-section v-if="mode == 'show' && canEnd" side top>
      <q-btn @click="onShowEnd" round icon="flag" />
      <q-dialog v-model="showEnd">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="flag" color="primary" text-color="white" />
            <span class="q-ml-sm">{{
              $t("really-end", { title: game.title })
            }}</span>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn :label="$t('cancel')" color="primary" v-close-popup />
            <q-btn
              :label="$t('end')"
              color="primary"
              @click="onEnd"
              v-close-popup
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </q-item-section>
    <!-- share -->
    <q-item-section v-if="canShare" side top>
      <q-btn @click.stop="" round icon="share">
        <q-tooltip anchor="center left" self="center end">{{
          $t("share")
        }}</q-tooltip>
        <q-popup-proxy>
          <q-chip
            :label="game.slug"
            icon="key"
            clickable
            @click="onCopySlug"
            v-close-popup
          />
        </q-popup-proxy>
      </q-btn>
    </q-item-section>
  </q-item>
</template>

<script>
import { mapState } from "vuex";

import dayjs from "dayjs";
import "dayjs/locale/de";
dayjs.locale("de");

import PlayerList from "./PlayerList.vue";

export default {
  data() {
    return {
      showStart: false,
      showEnd: false,
    };
  },
  props: {
    game: Object,
    mode: String,
  },
  computed: {
    ctime() {
      return dayjs(this.game.ctime);
    },
    avatar() {
      if (this.game.state == "running") return "play_arrow";
      if (this.game.state == "init") return "not_started";
      if (this.game.state == "finished") return "flag";
      return "";
    },
    canStart() {
      return (
        this.game.state == "init" &&
        this.game.user_id == this.currentUser.id &&
        this.game.players.length >= 3
      );
    },
    canOpen() {
      return this.game.state != "init";
    },
    canShare() {
      return this.game.state != "finished";
    },
    canEnd() {
      return (
        this.game.user_id == this.currentUser.id && this.game.state == "running"
      );
    },
    ...mapState(["currentUser"]),
  },
  methods: {
    onStart() {
      this.$store.dispatch("startGame", this.game.id);
    },
    onCopySlug() {
      navigator.clipboard.writeText(this.game.slug);
    },
    onShowEnd() {
      this.showEnd = !this.showEnd;
    },
    onShowStart() {
      this.showStart = !this.showStart;
    },
    onEnd() {
      this.$store.dispatch("endGame");
    },
    onClick() {
      if (this.mode == "list" && this.canOpen)
        this.$store.commit("openGame", this.game.id);
    },
  },
  components: {
    PlayerList,
  },
};
</script>

<style scoped></style>
