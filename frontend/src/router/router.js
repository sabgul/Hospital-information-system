import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
  mode: 'history',

  routes: [
    // General routes
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
      path: '/doctors',
      name: 'doctors',
      component: () => import('@/views/doctorsOverview/DoctorsOverview'),
    },
    // // //

        
    // Information for patients
    {
      path: '/health-concerns',
      name: 'HealthConcerns',
      component: () => import('@/views/healthConcernsOverview/HealthConcernsOverview'),
    },
    // // //
    

    // Patients management modules
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
    // // //
    

    // Healthcare worker module
    {
      path: '/examination-actions-overview',
      name: 'examinationActionsOverview',
      component: () => import('@/views/hcWorkerActions/ExaminationActionsOverview'),
    },
    {
      path: '/examination-action-add',
      name: 'examinationActionAdd',
      component: () => import('@/views/hcWorkerActions/ExaminationActionAdd'),
    },
    {
      path: '/manage-requests',
      name: 'manageTransactionsRequests',
      component: () => import('@/views/transactionRequests/TransactionsManager'),
    },
    // // //


    // Admin module
    {
      path: '/users-overview',
      name: 'usersOverview',
      component: () => import('@/views/usersManagement/UsersOverview'),
    },
    // // //

    // Show profile
    {
      path: '/profile/:role/:id',
      name: 'profile',
      props: true,
      component: () => import('@/views/usersManagement/UserProfile'),
    }
    // // //
  ]
});
