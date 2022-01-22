<template>
  <ListHead />
  <q-list v-if="hasGames" separator>
    <template v-for="game in games" :key="game.id">
      <GameHeadView :game="game" mode="list" />
    </template>
  </q-list>
  <q-banner v-else rounded class="bg-grey-3"> Keine Spiele gefunden. </q-banner>
</template>

<script>
import { mapState } from "vuex";
import GameHeadView from "../GameHeadView.vue";
import ListHead from "./ListHead.vue";
import isObjectEmpty from "../../utils/isObjectEmpty.js";

export default {
  props: {},
  mixins: [isObjectEmpty],
  computed: {
    ...mapState(["games"]),
    hasGames() {
      return !this.isObjectEmpty(this.games);
    },
  },
  components: {
    GameHeadView,
    ListHead,
  },
};
</script>

<style scoped>
.GamesList {
  text-align: left;
}
</style>
