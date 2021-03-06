import Vue from 'vue';
import Router from 'vue-router';
import {store} from '@/store/store';

Vue.use(Router);

const router = new Router({
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
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        // // //


        // Information for patients
        {
            path: '/my-health-report-card',
            name: 'healthReportCard',
            component: () => import('@/views/patient/healthReportCard/HealthReportCard'),
            meta: {
                requiresAuth: true,
                allowsPatient: true,
            }
        },
        // // //


        // Patients management modules
        {
            path: '/patient-add',
            name: 'patientAdd',
            component: () => import('@/views/admin/usersManagement/newUserModules/PatientAdd'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        {
            path: '/health-concern-detail/:id',
            name: 'healthConcernDetail',
            props: true,
            component: () => import('@/views/doctor/healthConcerns/ConcernDetail'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
                allowsPatient: true,
            }
        },
        {
            path: '/new-examination-request/:id',
            name: 'newExaminationRequest',
            props: true,
            component: () => import('@/views/doctor/examinations/NewExaminationRequest'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        {
            path: '/examination/:id',
            name: 'newExamination',
            props: true,
            component: () => import('@/views/doctor/examinations/NewExamination'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        {
            path: '/examine/:id',
            name: 'examine',
            props: true,
            component: () => import('@/views/doctor/examinations/Examine'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        {
            path: '/assigned-tickets',
            name: 'assignedTickets',
            component: () => import('@/views/doctor/examinations/ManageAssignedTickets'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        {
            path: '/health-concerns',
            name: 'healthConcerns',
            component: () => import('@/views/doctor/healthConcerns/HealthConcerns'),
            meta: {
                requiresAuth: true,
                allowsDoctor: true,
            }
        },
        // // //


        // Healthcare worker module
        {
            path: '/examination-actions-overview',
            name: 'examinationActionsOverview',
            component: () => import('@/views/healthcare-worker/examinationActions/ExaminationActionsOverview'),
            meta: {
                requiresAuth: true,
                allowsHealthcareworker: true,
            }
        },
        {
            path: '/examination-action-add',
            name: 'examinationActionAdd',
            component: () => import('@/views/healthcare-worker/examinationActions/ExaminationActionAdd'),
            meta: {
                requiresAuth: true,
                allowsHealthcareworker: true,
            }
        },
        {
            path: '/manage-requests',
            name: 'manageTransactionsRequests',
            component: () => import('@/views/healthcare-worker/transactionRequests/TransactionsManager'),
            meta: {
                requiresAuth: true,
                allowsHealthcareworker: true,
            }
        },
        // // //


        // Admin module
        {
            path: '/users-overview',
            name: 'usersOverview',
            component: () => import('@/views/admin/usersManagement/usersOverview/UsersOverview'),
            meta: {
                requiresAuth: true,
            }
        },
        // // //

        // Show profile
        {
            path: '/profile/:role/:id',
            name: 'profile',
            props: true,
            component: () => import('@/views/general/userProfile/UserProfile'),
            meta: {
                requiresAuth: true,
                allowsPatient: true,
                allowsDoctor: true,
                allowsHealthcareworker: true,
            }
        },
        {
            path: '/doctor-add',
            name: 'doctorAdd',
            component: () => import('@/views/admin/usersManagement/newUserModules/DoctorAdd'),
            meta: {
                requiresAuth: true,
            }
        },
        {
            path: '/healthcare-worker-add',
            name: 'healthcareWorkerAdd',
            component: () => import('@/views/admin/usersManagement/newUserModules/HealthcareWorkerAdd'),
            meta: {
                requiresAuth: true,
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
                requiresAuth: true,
                allowsPatient: true,
                allowsDoctor: true,
                allowsHealthcareworker: true,
            }
        },
        // // //
        {
            path: '/page-not-found',
            name: 'pageNotFound',
            component: () => import('@/views/general/PageNotFound'),
        },

        {
            path: '/*',
            name: 'pageNotFound',
            component: () => import('@/views/general/PageNotFound'),
        }
    ]
});

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!store.getters.isAuthenticated) {
            next('/');
            return;
        }

        // admin case missing intentionally - they are allowed everywhere

        if (store.state.userRole === 'patient') {
            if (!to.matched.some((record) => record.meta.allowsPatient)) {
                next('/');
                return;
            }
        } else if (store.state.userRole === 'doctor') {
            if (!to.matched.some((record) => record.meta.allowsDoctor)) {
                next('/');
                return;
            }
        } else if (store.state.userRole === 'healthcareworker') {
            if (!to.matched.some((record) => record.meta.allowsHealthcareworker)) {
                next('/');
                return;
            }
        }
    }
    next();
})

export default router;
