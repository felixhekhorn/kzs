<template>
  <div>
    <q-chip
      clickable
      :label="$i18n.locale"
      class="bg-white text-black"
      icon="language"
    >
      <q-popup-proxy>
        <q-list>
          <q-item
            v-for="loc in otherLocales"
            :key="loc"
            clickable
            v-close-popup
            @click="setLocale(loc)"
          >
            <q-item-section>
              <q-item-label>{{ loc }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-popup-proxy>
    </q-chip>
  </div>
</template>

<script>
import dayjs from "../../utils/myDayJS";

export default {
  computed: {
    otherLocales() {
      return this.$i18n.availableLocales.filter((e) => e != this.$i18n.locale);
    },
  },
  methods: {
    setLocale(loc) {
      sessionStorage.setItem("currentLocal", loc);
      this.$i18n.locale = loc;
      dayjs.locale(loc);
    },
  },
};
</script>

<style scoped></style>
