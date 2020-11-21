import Vue from 'vue';
import Vuex from 'vuex';
import axios_instance from "@/http-common";

Vue.use(Vuex);

export const store = new Vuex.Store({
        state: {
            doctorLoginActive: false,
            patientLoginActive: false,
            healthcareLoginActive: false,
            adminLoginActive: false,
            access_token: localStorage.getItem('access_token') || null, // if exists: load, else: null, later set in retrieveToken.
            refresh_token: localStorage.getItem('refresh_token') || null, // if exists: load, else: null, later set in retrieveToken.
            user: {}
        },

        getters: {
            // should be outside the store, as it might not yet exist when this is called
            user_full_name() {
                if (this.state.user) {
                    return `${this.state.user.first_name} ${this.state.user.last_name}`
                }
                else {
                    return "Name Surname"
                }
            },
        },

        mutations: {
            SET_ADMIN_LOGIN(state) {
                state.adminLoginActive = !state.adminLoginActive;
            },

            SET_DOCTOR_LOGIN(state) {
                state.doctorLoginActive = !state.doctorLoginActive;
            },

            SET_PATIENT_LOGIN(state) {
                state.patientLoginActive = !state.patientLoginActive;
            },

            SET_HEALTHCARE_LOGIN(state) {
                state.healthcareLoginActive = !state.healthcareLoginActive;
            },
            SET_ACCESS_TOKEN(state, access) {
                localStorage.setItem('access_token', access)
                state.access_token = access
            },
            SET_REFRESH_TOKEN(state, refresh) {
                localStorage.setItem('refresh_token', refresh)
                state.refresh_token = refresh
            },
            SET_USER(state, user) {
                state.user = user
            },
        },

        actions: {
            loginUser(context, credentials) {
                return new Promise((resolve, reject) => {
                    axios_instance.post('/token/', credentials)
                        .then(response => {
                            context.commit('SET_ACCESS_TOKEN', response.data.access)
                            context.commit('SET_REFRESH_TOKEN', response.data.refresh)

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
                if (context.getters.loggedIn) {
                    return new Promise((resolve, ) => {  // removed second param 'reject'
                        axios_instance.post('/token/logout/')
                            .then(() => {
                                localStorage.removeItem('access_token')
                                localStorage.removeItem('refresh_token')
                                context.commit('SET_ACCESS_TOKEN', null)
                                context.commit('SET_REFRESH_TOKEN', null)
                            })
                            .catch(err => {
                                localStorage.removeItem('access_token')
                                localStorage.removeItem('refresh_token')
                                context.commit('SET_ACCESS_TOKEN', null)
                                context.commit('SET_REFRESH_TOKEN', null)
                                resolve(err)
                            })
                    })
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

        }
    })
;
