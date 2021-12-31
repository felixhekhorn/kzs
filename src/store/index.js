import {
    createStore,
    createLogger
} from 'vuex';

const debug = process.env.NODE_ENV !== 'production';

export default createStore({
    state() {
        return {
            connection: null,
            has_server: false,
            currentError: "",
            currentUser: {
                "id": 1
            },
            games: {},
            users: {},
            state: "listGames",
            currentGame: {},
        }
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
        setUserId(state, user_id) {
            state.currentUser.id = user_id;
        },
        setGames(state, res) {
            state.games = {
                ...state.games,
                ...res.games
            };
            state.users = {
                ...state.users,
                ...res.users
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
        },
        startedGame(state, res) {
            state.games[res.game_id].state = "running";
        },
        openGame(state, game) {
            state.state = "showGame";
            state.currentGame = game;
        },
    },
    actions: {
        async send({
            state
        }, data) {
            state.connection.send(JSON.stringify(data));
        },
        async open({
            //state,
            dispatch,
            commit
        }) {
            // Establish connection via WebSocket
            const ws = new WebSocket("ws://localhost:8001");
            // parse answer
            ws.addEventListener('message', (event) => {
                //console.log('Message from server: ', event.data);
                const res = JSON.parse(event.data);
                if (res.type)
                    dispatch("parse", res);
            });
            // notify in browser
            ws.addEventListener('open', () => {
                commit("setHasServer", true);
            });
            commit("setConnection", ws);
        },
        parse({
            state,
            commit
        }, res) {
            commit("setError", "");
            if (res.type == "error")
                return commit("setError", res.body);
            if (res.type == "loadedGames" || res.type == "joinedGame" || res.type == "newGame")
                return commit("setGames", res);
            if (res.type == "addEntry")
                return commit("setEntry", res);
            if (res.type == "startedGame") {
                commit("startedGame", res);
                // open immediately for me, since I'm first
                const g = state.games[res.game_id];
                if (state.currentUser.id == g.user_id)
                    commit("openGame", g)
                return
            }
        },
        async loadGames({
            state,
            dispatch
        }) {
            return dispatch("send", {
                "type": "loadGames",
                "user_id": state.currentUser.id
            });
        },
        async addEntry({
            state,
            dispatch
        }, msg) {
            return dispatch("send", {
                "type": "addEntry",
                "user_id": state.currentUser.id,
                "game_id": state.currentGame.id,
                "body": msg
            })
        },
        async startGame({
            state,
            dispatch
        }, game) {
            return dispatch("send", {
                "type": "startGame",
                "user_id": state.currentUser.id,
                "game_id": game.id,
            })
        },
        async joinGame({
            state,
            dispatch
        }, slug) {
            return dispatch("send", {
                "type": "joinGame",
                "user_id": state.currentUser.id,
                "game_slug": slug,
            })
        },
        async newGame({
            state,
            dispatch
        }, title) {
            return dispatch("send", {
                "type": "newGame",
                "user_id": state.currentUser.id,
                "game_title": title,
            })
        },
    },
    strict: debug,
    plugins: debug ? [createLogger()] : []
});
