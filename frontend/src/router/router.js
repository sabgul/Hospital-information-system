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
      path: '/patient-add',
      name: 'patientAdd',
      component: () => import('@/views/patientsOverview/PatientAdd'),
    },
    {
      path: '/patient-detail',
      name: 'patientDetail',
      component: () => import('@/views/patientDetail/PatientDetail'),
    },
    {
      path: '/examination-action-add',
      name: 'examinationActionAdd',
      component: () => import('@/views/hcWorkerActions/ExaminationActionAdd'),
    },
    {
      path: '/health-concerns',
      name: 'HealthConcerns',
      component: () => import('@/views/healthConcernsOverview/HealthConcernsOverview'),
    },
  ]
});
