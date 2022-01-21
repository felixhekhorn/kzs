import { createStore, createLogger } from "vuex";

const debug = process.env.NODE_ENV !== "production";

export default createStore({
  state() {
    return {
      connection: null,
      has_server: false,
      currentError: "",
      state: "login",
      currentUser: {},
      games: {},
      users: {},
      currentGame: {},
    };
  },
  mutations: {
    setConnection(state, ws) {
      state.connection = ws;
    },
    setHasServer(state, flag) {
      state.has_server = flag;
    },
    setError(state, msg) {
      state.currentError = msg;
    },
    setUser(state, msg) {
      state.currentUser = msg.user;
      sessionStorage.setItem("currentUser.id", state.currentUser.id);
    },
    setGames(state, res) {
      state.games = {
        ...state.games,
        ...res.games,
      };
      state.users = {
        ...state.users,
        ...res.users,
      };
    },
    setEntry(state, res) {
      const g = state.games[res.Entry.game_id];
      g.entries.push(res.Entry);
      g.next_player_user_id = res.next_player_user_id;
    },
    listGames(state) {
      state.state = "listGames";
      state.currentGame = null;
      state.currentError = "";
    },
    startedGame(state, res) {
      state.games[res.game_id].state = "running";
    },
    endedGame(state, res) {
      state.games[res.game_id].state = "finished";
    },
    openGame(state, game_id) {
      state.state = "showGame";
      state.currentGameId = game_id;
      state.currentError = "";
    },
    logout(state) {
      state.state = "login";
      state.currentUser = {};
      state.games = {};
      state.users = {};
      sessionStorage.setItem("currentUser.id", "");
    },
    readFromSession(state) {
      const currentUserId = sessionStorage.getItem("currentUser.id");
      if (currentUserId) {
        state.currentUser = {
          id: currentUserId,
        };
      }
    },
  },
  actions: {
    async send({ state }, data) {
      await state.connection.send(JSON.stringify(data));
    },
    async open({ state, dispatch, commit }) {
      function getWebSocketServer() {
        if (window.location.host === "felixhekhorn.github.io") {
          return "wss://kzs.herokuapp.com/";
        } else if (window.location.host === "localhost:8080") {
          return "ws://localhost:8001/";
        } else if (window.location.host === "192.168.1.80:8080") {
          return "ws://192.168.1.80:8001/";
        } else {
          throw new Error(`Unsupported host: ${window.location.host}`);
        }
      }
      // Establish connection via WebSocket
      const ws = new WebSocket(getWebSocketServer());
      // parse answer
      ws.addEventListener("message", (event) => {
        //console.log('Message from server: ', event.data);
        const res = JSON.parse(event.data);
        if (res.type) dispatch("parse", res);
      });
      // notify in browser
      ws.addEventListener("open", () => {
        commit("setHasServer", true);
        // register current User with the server
        if (Object.keys(state.currentUser).length) dispatch("registerUser");
      });
      ws.addEventListener("close", () => {
        commit("setHasServer", false);
      });
      commit("setConnection", ws);
    },
    async parse({ state, commit, dispatch }, res) {
      commit("setError", "");
      if (res.type == "error") return commit("setError", res.body);
      if (res.type == "loggedIn") {
        commit("setUser", res);
        // Immediately load my games
        // Note that this _could_ be a infinite loop - but it isn't
        dispatch("loadGames");
        return commit("listGames");
      }
      if (
        res.type == "loadedGames" ||
        res.type == "joinedGame" ||
        res.type == "newGame"
      )
        return commit("setGames", res);
      if (res.type == "addEntry") {
        // reset last message
        sessionStorage.setItem("lastEntryBody", "");
        return commit("setEntry", res);
      }
      if (res.type == "startedGame") {
        commit("startedGame", res);
        // open immediately for me, since I'm first
        const g = state.games[res.game_id];
        if (state.currentUser.id == g.user_id) commit("openGame", res.game_id);
        return;
      }
      if (res.type == "endedGame") {
        return commit("endedGame", res);
      }
    },
    async loadGames({ state, dispatch }) {
      return await dispatch("send", {
        type: "loadGames",
        user_id: state.currentUser.id,
      });
    },
    async addEntry({ state, dispatch }, msg) {
      return await dispatch("send", {
        type: "addEntry",
        user_id: state.currentUser.id,
        game_id: state.currentGameId,
        body: msg,
      });
    },
    async startGame({ state, dispatch }, game_id) {
      return await dispatch("send", {
        type: "startGame",
        user_id: state.currentUser.id,
        game_id: game_id,
      });
    },
    async endGame({ state, dispatch }) {
      return await dispatch("send", {
        type: "endGame",
        user_id: state.currentUser.id,
        game_id: state.currentGameId,
      });
    },
    async joinGame({ state, dispatch }, slug) {
      return await dispatch("send", {
        type: "joinGame",
        user_id: state.currentUser.id,
        game_slug: slug,
      });
    },
    async newGame({ state, dispatch }, title) {
      return await dispatch("send", {
        type: "newGame",
        user_id: state.currentUser.id,
        game_title: title,
      });
    },
    async login({ dispatch }, data) {
      return await dispatch("send", {
        type: "login",
        user_name: data.user_name,
        user_password: data.user_password,
      });
    },
    async logout({ state, dispatch }) {
      return await dispatch("send", {
        type: "logout",
        user_id: state.currentUser.id,
      });
    },
    async registerUser({ state, dispatch }) {
      return await dispatch("send", {
        type: "registerUser",
        user_id: state.currentUser.id,
      });
    },
    async newUser({ dispatch }, data) {
      return await dispatch("send", {
        type: "newUser",
        user_name: data.user_name,
        user_password_1: data.user_password_1,
        user_password_2: data.user_password_2,
      });
    },
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});
