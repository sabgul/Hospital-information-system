<template>
    <div>
        <div class="main__content">
            <h1>Users overview</h1>

            <p>
                In this module you can see the list of all users in this system.<br>
                You can manage particular information by clicking on a given user.
            </p>
        </div>

        <div class="main__content">
            <h5>
                All system users
            </h5>

            <br>

            <vs-table
                striped
                class="users__table"
            >
                <template #header>
                    <vs-input
                        v-model="searchValue"
                        border
                        placeholder="Search"
                    />
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
                            <span
                                @click="showUserProfile(user.userData.user.id, user.role)"
                                class="redirect__profile"
                            >
                                {{ user.userData.user.first_name }} {{ user.userData.user.last_name }}
                            </span>
                        </vs-td>

                        <vs-td>
                            <b>{{ user.role }}</b>
                        </vs-td>

                        <vs-td>
                            {{ getDate(user.userData.user.date_of_birth) }}
                        </vs-td>

                        <vs-td>
                            {{ getEmailContact(user.userData.user.email) }}
                        </vs-td>

                        <template #expand>
                            <div class="expanded__item">
                                <div class="expanded__item">
                                    <vs-avatar
                                        @click="showUserProfile(user.userData.user.id, user.role)"
                                        class="redirect__profile"
                                    >
                                        <img
                                            src="@/assets/user-illu.jpg"
                                            alt=""
                                        >
                                    </vs-avatar>

                                    <b>
                                        <span
                                            class="user__name redirect__profile"
                                            @click="showUserProfile(user.userData.user.id, user.role)"
                                        >
                                            {{ user.userData.user.first_name }} {{ user.userData.user.last_name }}
                                        </span>
                                    </b>
                                </div>

                                <div class="expanded__item right">
                                    <vs-tooltip>
                                        <vs-button
                                            icon
                                            @click="editUserProfile(user.userData.user.id, user.role)"
                                        >
                                            <box-icon
                                                name='comment-edit'
                                                animation='tada-hover'
                                            />
                                        </vs-button>

                                        <template #tooltip>
                                            Edit user
                                        </template>
                                    </vs-tooltip>

                                    <vs-tooltip>
                                        <vs-button
                                            danger
                                            icon
                                            @click="deleteUserDialog(user)"
                                        >
                                            <box-icon
                                                name='trash'
                                                animation='tada-hover'
                                            />
                                        </vs-button>

                                        <template #tooltip>
                                            Remove user
                                        </template>
                                    </vs-tooltip>
                                </div>
                            </div>
                        </template>
                    </vs-tr>
                </template>
        
                <template #footer>
                    <vs-pagination
                        v-model="page"
                        :length="$vs.getLength(users, max)"
                    />
                </template>
            </vs-table>
        </div>

        <vs-dialog
            width="500px"
            v-model="activeDelete"
        >
            <template #header>
                <h5>
                    Are you sure you want to delete <b>{{ userToDelete.userData.name }}</b>?
                </h5>
            </template>

            <br>

            <p v-if="userToDelete.role === 'Doctor'">
                Please choose a new doctor who will be responsible for <br> patients, examinations and other responsibilities of doctor currently being removed:
            </p>

            <vs-select
                v-if="userToDelete.role === 'Doctor'"
                v-model="doctorToReplace"
                class="popup__center"
                label="Choose responsible doctor"
                color="primary"
            >
                <template
                    #message-warn
                    v-if="doctorToReplace === -1"
                >
                    Required
                </template>

                <vs-option
                    v-for="doctor in availableWithoutDeleted"
                    :key="doctor.user.id"
                    :label="doctor.user.first_name"
                    :value="doctor.user.id"
                >
                    {{ doctor.user.first_name }}
                </vs-option>
            </vs-select>

            <br>

            <template #footer>
                <div class="popup__right">
                    <vs-button
                        danger
                        border
                        :disabled="doctorToReplace === -1 && userToDelete.role === 'Doctor'"
                        @click="deleteUser()"
                    >
                        Delete
                    </vs-button>
                </div>
            </template>
        </vs-dialog>
    </div>
</template>


<script>
import PatientsService from '@/services/patientsService.js';
import DoctorsService from '@/services/doctorsService.js';
import HealthcareWorkersService from '@/services/healthcareWorkersService.js';
import UsersService from "@/services/usersService";

import NotificationsUtils from "@/utils/notificationsUtils";
import DateUtils from "@/utils/dateUtils";

export default {
    name: 'UsersOverview',    

    data:() => ({
        users: [],
        page: 1,
        max: 5,
        searchValue: '',

        userToDelete: {},
        activeDelete: false,

        availableDoctors: [],
        doctorToReplace: -1,
    }),

    async created() {
        await this.getAllUsers();
    },

    computed: {
        // Array of all doctor except of the one being deleted
        availableWithoutDeleted() {
            return this.availableDoctors.filter((doctor) => doctor.user.id !== this.userToDelete.userData.user.id);
        }
    },

    methods: {
        getDate(date) {
          return DateUtils.getDateForFrontend(date);
        },

        async getAllUsers() {
            this.users = [];
            PatientsService.getAll()
            .then(response => {
                response.data.forEach(patient => this.users.push({userData: patient, role: 'Patient'}));
            })

            DoctorsService.getAll()
            .then(response => {
                response.data.forEach(doctor => this.users.push({userData: doctor, role: 'Doctor'}));
                this.availableDoctors = response.data;
            })

            HealthcareWorkersService.getAll()
            .then(response => {
                response.data.forEach(worker => this.users.push({userData: worker, role: 'Health insurance worker'}));
            })
        },

        getEmailContact(fetchedEmail) {
            return fetchedEmail ? fetchedEmail : 'Email not stated';
        },

        showUserProfile(userId, role) {
            this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }})
        },

        editUserProfile(userId, role) {
            this.$router.push({ name: 'edit-profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }})
        },

        deleteUserDialog(user) {
            this.activeDelete = true;
            this.userToDelete = user;
        },

        async deleteUser() {
            if(this.userToDelete.role === 'Patient') {
                PatientsService.delete(this.userToDelete.userData.user.id)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Patient successfully deleted.', this.$vs);
                    this.getAllUsers();
                    this.activeDelete = false;

                    UsersService.delete(this.userToDelete.userData.user.id)
                    .then(response => {
                        console.log(response);
                    })

                    this.$forceUpdate();
                })
            }

            if(this.userToDelete.role === 'Health insurance worker') {
                HealthcareWorkersService.delete(this.userToDelete.userData.user.id)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Health insurance worker successfully deleted.', this.$vs);
                    this.getAllUsers();
                    this.activeDelete = false;

                    UsersService.delete(this.userToDelete.userData.user.id)
                    .then(response => {
                        console.log(response);
                    })

                    this.$forceUpdate();
                })
            }

            if(this.userToDelete.role === 'Doctor') {
                DoctorsService.deleteWithNewResponsible(this.userToDelete.userData.user.id, this.doctorToReplace)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Health insurance worker successfully deleted.', this.$vs);
                    this.getAllUsers();
                    this.activeDelete = false;

                    UsersService.delete(this.userToDelete.userData.user.id)
                    .then(response => {
                        console.log(response);
                    })

                    this.$forceUpdate();
                })
            }
        }
    },
}
</script>

<style scoped>
    box-icon {
        fill: #fbfbfb;
    }

    .users__table {
      width: 80%;
      margin: 1em auto 0;
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
