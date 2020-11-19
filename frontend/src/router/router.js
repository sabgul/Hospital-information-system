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
      meta: { // TODO add for all other
        requiresAuth: true
      }
    },

    {
      path: '/doctors',
      name: 'doctors',
      component: () => import('@/views/doctorsOverview/DoctorsOverview'),
      meta: {
        requiresAuth: true
      }
    },
    // // //

        
    // Information for patients
    {
      path: '/health-concerns',
      name: 'HealthConcerns',
      component: () => import('@/views/healthConcernsOverview/HealthConcernsOverview'),
      meta: {
        requiresAuth: true
      }
    },
    // // //
    

    // Patients management modules
    {
      path: '/patient-add',
      name: 'patientAdd',
      component: () => import('@/views/patientsOverview/PatientAdd'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/patient-detail',
      name: 'patientDetail',
      component: () => import('@/views/patientDetail/PatientDetail'),
      meta: {
        requiresAuth: true
      }
    },
    // // //
    

    // Healthcare worker module
    {
      path: '/examination-actions-overview',
      name: 'examinationActionsOverview',
      component: () => import('@/views/hcWorkerActions/ExaminationActionsOverview'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/examination-action-add',
      name: 'examinationActionAdd',
      component: () => import('@/views/hcWorkerActions/ExaminationActionAdd'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/manage-requests',
      name: 'manageTransactionsRequests',
      component: () => import('@/views/transactionRequests/TransactionsManager'),
      meta: {
        requiresAuth: true
      }
    },
    // // //


    // Admin module
    {
      path: '/users-overview',
      name: 'usersOverview',
      component: () => import('@/views/usersManagement/UsersOverview'),
      meta: {
        requiresAuth: true
      }
    },
    // // //

    // Show profile
    {
      path: '/profile/:role/:id',
      name: 'profile',
      props: true,
      component: () => import('@/views/usersManagement/UserProfile'),
      meta: {
        requiresAuth: true
      }
    },
    // // //

    // Edit profile
    {
      path: '/edit-profile/:role/:id',
      name: 'edit-profile',
      props: true,
      component: () => import('@/views/general/EditProfile'),
      meta: {
        requiresAuth: true
      }
    }
    // // //
  ]
});
