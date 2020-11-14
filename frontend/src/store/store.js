import Vue from 'vue';
import Vuex from 'vuex';
import http from "@/http-common";

Vue.use(Vuex);

export const store = new Vuex.Store({
        state: {
            doctorLoginActive: false,
            patientLoginActive: false,
            healthcareLoginActive: false,
            adminLoginActive: false,
            access_token: localStorage.getItem('access_token') || null, // if exists: load, else: null, later set in retrieveToken.
            refresh_token: localStorage.getItem('refresh_token') || null, // if exists: load, else: null, later set in retrieveToken.
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
            SET_ACCESS_TOKEN (state, access) {
              localStorage.setItem('access_token', access)
              state.access_token = access
            },
            SET_REFRESH_TOKEN (state, refresh) {
              localStorage.setItem('refresh_token', refresh)
              state.refresh_token = refresh
            },
        },

        actions: {
            loginUser(context, credentials) {
                return new Promise((resolve, reject) => {
                    http.post('/token/', {
                        username: credentials.username,
                        password: credentials.password
                    })
                        .then(response => {
                            console.log('retrieveToken().then()', response);
                            context.commit('SET_ACCESS_TOKEN', response.data.access)
                            context.commit('SET_REFRESH_TOKEN', response.data.refresh)
                            resolve()
                        })
                        .catch(error => {
                            console.log(error)
                            reject(error)  // propagate back to login dialog?
                        })
                })
            },
            registerUser(context, data) {
                return new Promise((resolve, reject) => {
                    http.post('/register/', {
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
        }
    })
;
