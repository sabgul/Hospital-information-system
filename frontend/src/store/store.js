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
            token: localStorage.getItem('access_token') || null, // if exists: load, else: null, later set in retrieveToken.
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
            retrieveToken(state, token) {
                state.token = token
            },
        },

        actions: {
            retrieveToken(context, credentials) {
                http.post('/token/', {
                    username: credentials.username,
                    password: credentials.password,
                })
                    .then(response => {
                        console.log('retrieveToken().then()', response);
                        const token = response.data.access_token
                        // where to store token:
                        //      local storage (common)
                        //          - can be stolen through XSS
                        //      cookie
                        //          - vulnerable to CSRFX
                        localStorage.setItem('access_token', token)
                        context.commit('retrieveToken', token)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            },
        }
    })
;
