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
      path: '/my-health-concerns',
      name: 'HealthConcerns',
      component: () => import('@/views/healthConcernsOverview/HealthConcernsOverview'),
    },
    // // //
    

    // Patients management modules
    {
      path: '/patient-add',
      name: 'patientAdd',
      component: () => import('@/views/usersManagement/PatientAdd'),
    },
    {
      path: '/patient-detail',
      name: 'patientDetail',
      component: () => import('@/views/patientDetail/PatientDetail'),
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
      component: () => import('@/views/examinations/NewExaminationRequest'),
    },
    {
      path: '/examination/:id',
      name: 'newExamination',
      props: true,
      component: () => import('@/views/examinations/NewExamination'),
    },
    {
      path: '/examine/:id',
      name: 'examine',
      props: true,
      component: () => import('@/views/examinations/Examine'),
    },
    {
      path: '/assigned-tickets',
      name: 'assignedTickets',
      component: () => import('@/views/examinations/ManageAssignedTickets'),
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
    },
    {
      path: '/doctor-add',
      name: 'doctorAdd',
      component: () => import('@/views/usersManagement/DoctorAdd'),
    },
    {
      path: '/healthcare-worker-add',
      name: 'healthcareWorkerAdd',
      component: () => import('@/views/usersManagement/HealthcareWorkerAdd'),
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
      path: '*',
      name: 'pageNotFound',
      component: () => import('@/views/general/PageNotFound'),
    }
  ]
});
