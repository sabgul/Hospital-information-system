<template>
    <div>
        <div class="main__content">
            <h1>Users overview</h1>

            <p>
                In this module you can see list of all users in this system.<br>
                By clicking on given user, you can manage his information.
            </p>
        </div>

        <div class="main__content">
            <vs-table striped class="users__table">
                <template #header>
                    <vs-input v-model="searchValue" border placeholder="Search"/>
                </template>

                <template #thead>
                    <vs-tr>
                        <vs-th>
                            User name
                        </vs-th>

                        <vs-th>
                            Role
                        </vs-th>

                        <vs-th>
                            Date of birth
                        </vs-th>

                        <vs-th>
                            E-mail contact
                        </vs-th>
                    </vs-tr>
                </template>

                <template #tbody>
                    <vs-tr
                        :key="i"
                        v-for="(user, i) in $vs.getPage($vs.getSearch(users, searchValue), page, max)"
                        :data="user"
                    >
                        <vs-td>
                            <span @click="showUserProfile(user.userData.id, user.role)" class="redirect__profile">{{ user.userData.name }}</span>
                        </vs-td>

                        <vs-td>
                            <b>{{ user.role }}</b>
                        </vs-td>

                        <vs-td>
                            {{ user.userData.date_of_birth }}
                        </vs-td>

                        <vs-td>
                            {{ getEmailContact(user.userData.email_field) }}
                        </vs-td>

                        <template #expand>
                            <div class="expanded__item">
                                <div class="expanded__item">
                                    <vs-avatar @click="showUserProfile(user.userData.id, user.role)" class="redirect__profile">
                                        <img src="@/assets/user-illu.jpg" alt="">
                                    </vs-avatar>

                                    <b>
                                        <span class="user__name redirect__profile" @click="showUserProfile(user.userData.id, user.role)">
                                            {{ user.userData.name }}
                                        </span>
                                    </b>
                                </div>

                                <div class="expanded__item right">
                                    <vs-button flat icon>
                                        Send Email
                                    </vs-button>

                                    <vs-button warn>
                                        Edit User
                                    </vs-button>

                                    <vs-button border danger>
                                        Remove User
                                    </vs-button>
                                </div>
                            </div>
                        </template>
                    </vs-tr>
                </template>
        
                <template #footer>
                    <vs-pagination v-model="page" :length="$vs.getLength(users, max)" />
                </template>
            </vs-table>
        </div> 
    </div>
</template>


<script>
import PatientsService from '@/services/patientsService.js';
import DoctorsService from '@/services/doctorsService.js';
import HealthcareWorkersService from '@/services/healthcareWorkersService.js';

export default {
    name: 'UsersOverview',    

    components: {
    },
    
    data:() => ({
        users: [],
        page: 1,
        max: 5,
        searchValue: '',
    }),

    async created() {
        PatientsService.getAll()
        .then(response => {
            response.data.forEach(pacient => this.users.push({userData: pacient, role: 'Pacient'}));
        })
        .catch(e => {
            console.log(e);
        });

        DoctorsService.getAll()
        .then(response => {
            response.data.forEach(doctor => this.users.push({userData: doctor, role: 'Doctor'}));
        })
        .catch(e => {
            console.log(e);
        });

        HealthcareWorkersService.getAll()
        .then(response => {
            response.data.forEach(worker => this.users.push({userData: worker, role: 'Health insurance worker'}));
        })
        .catch(e => {
            console.log(e);
        });
    },
    
    methods: {
        getEmailContact(fetchedEmail) {
            return fetchedEmail ? fetchedEmail : 'Email not stated';
        },

        showUserProfile(userId, role) {
            this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }})
        }
    },
}
</script>

<style scoped>
    h1 {
        margin-top: 0.5em;
        margin-bottom: 1em;
    }

    .main__content {
        padding: 20px 20px 20px 25px;
        margin-top: 20px;
        margin-left: 25%;
        margin-right: 15%;
        background-color: #ffffff;
        box-shadow:
            0 1.3px 20.1px rgba(0, 0, 0, 0.003),
            0 4.2px 44.8px rgba(0, 0, 0, 0.003),
            0 19px 76px rgba(0, 0, 0, 0.06);
        border-radius: 10px;
    }

    .users__table {
        margin: 0 auto;
        width: 80%;
        margin-top: 1em;
    }

    .expanded__item {
        display: flex;
    }

    .right {
        position: absolute;
        right: 10px;
    }

    .user__name {
        position: absolute;
        left: 5em;
        top: 18px;
        font-size: 16px;
    }

    .redirect__profile:hover {
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }
</style>