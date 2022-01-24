process.env.VUE_APP_VERSION = require("./package.json").version;

module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/kzs/" : "/",
  pluginOptions: {
    quasar: {
      importStrategy: "kebab",
      rtlSupport: false,
    },
    i18n: {
      locale: "de",
      fallbackLocale: "de",
      localeDir: "locales",
      enableLegacy: false,
      runtimeOnly: false,
      compositionOnly: false,
      fullInstall: true,
    },
  },
  transpileDependencies: ["quasar"],
};
