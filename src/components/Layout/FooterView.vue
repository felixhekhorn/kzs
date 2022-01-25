<template>
  &copy; F. Hekhorn 2021-2022
  <a target="_blank" href="https://github.com/felixhekhorn/kzs"
    ><img
      src="img/GitHub-Mark-32px.png"
      alt="GitHub"
      style="max-height: 17px; vertical-align: text-bottom"
  /></a>
  v{{ version }}
</template>

<script>
export default {
  computed: {
    version() {
      return process.env.VUE_APP_VERSION;
    },
  },
};
</script>

<style scoped></style>
