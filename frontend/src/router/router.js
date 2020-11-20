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
      component: () => import('@/views/general/MainPage'),
    },
    {
      path: '/patients',
      name: 'patients',
      component: () => import('@/views/doctor/patientsOverview/PatientsOverview'),
    },
    // // //

        
    // Information for patients
    {
      path: '/my-health-concerns',
      name: 'HealthConcerns',
      component: () => import('@/views/patient/healthConcernsOverview/HealthConcernsOverview'),
    },
    // // //
    

    // Patients management modules
    {
      path: '/patient-add',
      name: 'patientAdd',
      component: () => import('@/views/admin/usersManagement/newUserModules/PatientAdd'),
    },
    {
      path: '/health-concern-detail/:id',
      name: 'healthConcernDetail',
      props: true,
      component: () => import('@/components/ConcernDetail'),
    },
    {
      path: '/new-examination-request/:id',
      name: 'newExaminationRequest',
      props: true,
      component: () => import('@/views/doctor/examinations/NewExaminationRequest'),
    },
    {
      path: '/examination/:id',
      name: 'newExamination',
      props: true,
      component: () => import('@/views/doctor/examinations/NewExamination'),
    },
    {
      path: '/examine/:id',
      name: 'examine',
      props: true,
      component: () => import('@/views/doctor/examinations/Examine'),
    },
    {
      path: '/assigned-tickets',
      name: 'assignedTickets',
      component: () => import('@/views/doctor/examinations/ManageAssignedTickets'),
    },
    {
      path: '/health-concerns',
      name: 'healthConcerns',
      component: () => import('@/views/doctor/healthConcerns/HealthConcerns'),
    },
    // // //
    

    // Healthcare worker module
    {
      path: '/examination-actions-overview',
      name: 'examinationActionsOverview',
      component: () => import('@/views/healthcare-worker/examinationActions/ExaminationActionsOverview'),
    },
    {
      path: '/examination-action-add',
      name: 'examinationActionAdd',
      component: () => import('@/views/healthcare-worker/examinationActions/ExaminationActionAdd'),
    },
    {
      path: '/manage-requests',
      name: 'manageTransactionsRequests',
      component: () => import('@/views/healthcare-worker/transactionRequests/TransactionsManager'),
    },
    // // //


    // Admin module
    {
      path: '/users-overview',
      name: 'usersOverview',
      component: () => import('@/views/admin/usersManagement/usersOverview/UsersOverview'),
    },
    // // //

    // Show profile
    {
      path: '/profile/:role/:id',
      name: 'profile',
      props: true,
      component: () => import('@/views/admin/usersManagement/userProfile/UserProfile'),
    },
    {
      path: '/doctor-add',
      name: 'doctorAdd',
      component: () => import('@/views/admin/usersManagement/newUserModules/DoctorAdd'),
    },
    {
      path: '/healthcare-worker-add',
      name: 'healthcareWorkerAdd',
      component: () => import('@/views/admin/usersManagement/newUserModules/HealthcareWorkerAdd'),
    },
    // // //

    // Edit profile
    {
      path: '/edit-profile/:role/:id',
      name: 'edit-profile',
      props: true,
      component: () => import('@/views/general/EditProfile'),
    },
    // // //
    {
      path: 'page-not-found',
      name: 'pageNotFound',
      component: () => import('@/views/general/PageNotFound'),
    },

    {
      path: '*',
      name: 'pageNotFound',
      component: () => import('@/views/general/PageNotFound'),
    }
  ]
});
