<template>
    <div>
        <div class="main__content">
            <h1>{{ user.name }}</h1>

            <h4><b>Role</b>: {{ (role.charAt(0).toUpperCase() + role.slice(1)).replace(/-/g, ' ') }}</h4>

            <div class="info__basic">
                <h5><b>Date of birth</b>: {{ formatDate(user.date_of_birth) }}</h5>
                <h5><b>Age</b>: {{ getAge(user.date_of_birth) }}</h5>
                <h5><b>Email address</b>: {{ user.email_field ? user.email_field : 'Email not stated' }}</h5>
                <h5><b>Phone number</b>: {{ user.phone_number ? '+' + user.phone_number : 'Phone number not stated' }}</h5>
            </div>

            <h6><b>User activity</b>: {{ user.user_active ? 'Active' : 'Inactive' }}</h6>
            
            <div class="user__pic">
                <vs-card type="2">
                    <template #img>
                        <img
                            src="@/assets/user-illu.jpg"
                            alt=""
                            style="cursor: default;"
                        >
                    </template>

                    <template #interactions>
                        <vs-tooltip>
                            <vs-button @click="redirectToEdit(user.id, role)">
                                <box-icon
                                    name='comment-edit'
                                    animation='tada-hover'
                                />
                            </vs-button>

                            <template #tooltip>
                                  Edit profile
                            </template>
                        </vs-tooltip>
                    </template>
                </vs-card>
            </div>
        </div>

        <div 
            class="main__content"
            v-if="role === 'doctor'"
        >
            <user-profile-doctor :doctor="user"/>
        </div>

        <div 
            class="main__content"
            v-if="role === 'patient'"
        >
            <user-profile-patient :patient="user"/>
        </div>

        <div 
            class="main__content"
            v-if="role === 'health-insurance-worker'"
        >
            <user-profile-hc-worker :worker="user"/>
        </div>
    </div>
</template>


<script>
import PatientsService from '@/services/patientsService.js';
import DoctorsService from '@/services/doctorsService.js';
import HealthcareWorkersService from '@/services/healthcareWorkersService.js';
import UserProfileDoctor from "@/views/usersManagement/UserProfileDoctor";
import UserProfileHcWorker from "@/views/usersManagement/UserProfileHcWorker";
import UserProfilePatient from "@/views/usersManagement/UserProfilePatient";

export default {
    name: 'UserProfile', 
    
    props: {
        id: String, 
        role: String,
    },

    components: {
        UserProfileDoctor,
        UserProfileHcWorker,
        UserProfilePatient,
    },

    data:() => ({
        user: {},
    }),

    async created() {
        if(this.role === 'patient') {
            PatientsService.get(this.id)
            .then(response => {
                this.user = response.data
            })
            .catch(e => {
                console.log(e);
            });
        }

        if(this.role === 'doctor') {
            DoctorsService.get(this.id)
            .then(response => {
                this.user = response.data
            })
            .catch(e => {
                console.log(e);
            });
        }

        if(this.role === 'health-insurance-worker') {
            HealthcareWorkersService.get(this.id)
            .then(response => {
                this.user = response.data
            })
            .catch(e => {
                console.log(e);
            });
        }
    },
    
    methods: {
        formatDate(date) {
            const day = date.slice(8, 10);
            const month = date.slice(5, 7);
            const year = date.slice(0, 4);
            return day + '. ' + month + '. ' + year;
        },

        getAge(dateString) {
            var today = new Date();
            var birthDate = new Date(dateString);
            var age = today.getFullYear() - birthDate.getFullYear();
            var m = today.getMonth() - birthDate.getMonth();

            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }
            if(age === 0) {
                return m + ' months';
            }
            return age + ' years';
        },

        redirectToEdit(id, role) {
          this.$router.push({ name: 'edit-profile', params: { id: id, role: role }});
        }
    },
}
</script>

<style scoped>
    box-icon {
        fill: #fbfbfb;
    }

    .user__pic {
        position: absolute;
        right: 16%;
        top: 5.5em;
        width: 20%;
        height: 20%;
    }

    .info__basic {
        padding-bottom: 2em;
        padding-top: 1em;
    }

    @media only screen and (max-width: 1200px) {
        .user__pic {
            display: none;
        }
    }   
</style>