import Vue from 'vue';
import Vuex from 'vuex';
import axios_instance from "@/http-common";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export const store = new Vuex.Store({
        plugins: [createPersistedState({
            storage: window.sessionStorage,
        })],

        state: {
            doctorLoginWindowActive: false,
            patientLoginWindowActive: false,
            healthcareLoginWindowActive: false,
            adminLoginWindowActive: false,
            access_token: localStorage.getItem('access_token') || null,
            refresh_token: localStorage.getItem('refresh_token') || null,
            user: {},
            userRole: null,
        },

        mutations: {
            SET_ADMIN_LOGIN_WINDOW(state) {
                state.adminLoginWindowActive = !state.adminLoginWindowActive;
            },

            SET_DOCTOR_LOGIN_WINDOW(state) {
                state.doctorLoginWindowActive = !state.doctorLoginWindowActive;
            },

            SET_PATIENT_LOGIN_WINDOW(state) {
                state.patientLoginWindowActive = !state.patientLoginWindowActive;
            },

            SET_HEALTHCARE_LOGIN_WINDOW(state) {
                state.healthcareLoginWindowActive = !state.healthcareLoginWindowActive;
            },

            SET_ACCESS_TOKEN(state, access) {
                localStorage.setItem('access_token', access);
                state.access_token = access;
            },

            SET_REFRESH_TOKEN(state, refresh) {
                localStorage.setItem('refresh_token', refresh);
                state.refresh_token = refresh;
            },

            SET_USER(state, user) {
                state.user = user;
            },

            SET_CURRENT_USER_ROLE(state, role) {
                state.userRole = role;
            },
        },

        actions: {
            loginUser(context, credentials) {
                return new Promise((resolve, reject) => {
                    axios_instance.post('/token/', credentials)
                        .then(response => {
                            context.commit('SET_ACCESS_TOKEN', response.data.access);
                            context.commit('SET_REFRESH_TOKEN', response.data.refresh);
                            context.commit('SET_CURRENT_USER_ROLE', credentials.role);

                            // if token acquired, get user data
                            axios_instance.get('/users/me/')
                                .then(response => {
                                    context.commit('SET_USER', response.data)
                                })
                            // todo handle errors

                            resolve()
                        })
                        .catch(error => {
                            // propagate back to login dialog
                            reject(error)
                        })
                })
            },
            registerUser(context, data) {  // not used yet
                return new Promise((resolve, reject) => {
                    axios_instance.post('/users/', {
                        name: data.name,
                        email: data.email,
                        username: data.username,
                        password: data.password,
                        confirm: data.confirm
                    })
                        .then(response => {
                            resolve(response)
                        })
                        .catch(error => {
                            reject(error)
                        })
                })
            },
            logoutUser(context) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                context.commit('SET_ACCESS_TOKEN', null);
                context.commit('SET_REFRESH_TOKEN', null);
                if (this.window && this.window.sessionStorage)
                    this.window.sessionStorage.clear();
            },

            refreshToken() {
                return new Promise((resolve, reject) => {
                    if (store.state.refresh_token) {
                        axios_instance.post('/token/refresh/', {
                            refresh: store.state.refresh_token
                        })
                            .then(response => {
                                store.commit('SET_ACCESS_TOKEN', response.data.access)
                                store.commit('SET_REFRESH_TOKEN', response.data.refresh)
                                resolve(response.data.access)
                            })
                            .catch(err => {
                                reject(err)
                            })
                    }
                })
            }
        },

        getters: {
            isAuthenticated: state => {
                return !!state.access_token
            }
        },
    })
;
