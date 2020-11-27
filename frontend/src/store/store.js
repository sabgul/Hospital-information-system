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
                if (context.getters.isAuthenticated) { // todo why not isAuthenticated
                    return new Promise((resolve, ) => {  // removed second param 'reject'
                        axios_instance.post('/token/logout/')
                            .then(() => {
                                localStorage.removeItem('access_token')
                                localStorage.removeItem('refresh_token')
                                context.commit('SET_ACCESS_TOKEN', null)
                                context.commit('SET_REFRESH_TOKEN', null)
                                this.window.sessionStorage.clear();
                            })
                            .catch(err => {
                                localStorage.removeItem('access_token')
                                localStorage.removeItem('refresh_token')
                                context.commit('SET_ACCESS_TOKEN', null)
                                context.commit('SET_REFRESH_TOKEN', null)
                                resolve(err)
                                this.window.sessionStorage.clear();
                            })
                    });

                }
            },

            refreshToken(context) {
                return new Promise((resolve, reject) => {
                    axios_instance.post('/token/refresh/', {
                        refresh: context.state.refreshToken
                    }) // send the stored refresh token to the backend API
                        .then(response => { // if API sends back new access and refresh token update the store
                            console.log('New access successfully generated')
                            context.commit('SET_ACCESS_TOKEN', response.data.access)
                            context.commit('SET_REFRESH_TOKEN', response.data.refresh)
                            resolve(response.data.access)
                        })
                        .catch(err => {
                            console.log(err)
                            reject(err) // error generating new access and refresh token because refresh token has expired
                        })
                })
            }
        },

        getters: {
            user_full_name: state => {
                if (state.user) {
                    return `${state.user.first_name} ${state.user.last_name}`
                }
                else {
                    return "Name Surname"
                }
            },
            isAuthenticated: state => {
                console.log('.')
                return !!state.access_token
            }
        },
    })
;
