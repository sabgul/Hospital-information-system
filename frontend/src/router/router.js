import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
  mode: 'history',

  routes: [
    {
      path: '/',
      name: 'homepage',
      component: () => import('@/views/mainPage/MainPage'),
    },
    {
      path: '/patients',
      name: 'patients',
      component: () => import('@/views/patientsOverview/PatientsOverview'),
    },
    {
      path: '/patientAdd',
      name: 'patientAdd',
      component: () => import('@/views/patientsOverview/PatientAdd'),
    },
  ]
});
