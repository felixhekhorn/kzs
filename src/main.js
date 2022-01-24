import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";
import i18n from "./i18n";

const app = createApp(App);
app.use(i18n);
app.use(Quasar, quasarUserOptions);
app.use(store);
app.mount("#app");
