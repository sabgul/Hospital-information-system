import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    doctorLoginActive: false,
    patientLoginActive: false,
    healthcareLoginActive: false,
    adminLoginActive: false,
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
    }
  },
});
