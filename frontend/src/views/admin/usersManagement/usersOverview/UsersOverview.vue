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
          <h4>
            Filter results
          </h4>

          <div class="wrapper">
            <div class="left__filter__row">
              <vs-select
                v-model="filter.user_role"
                label="Role"
                color="primary"
              >
                <vs-option
                  v-for="user in users"
                  :key="user.id"
                  label="meno"
                  :value="user.id"
                >
                  {{ "ajoj" }}
                </vs-option>
              </vs-select>
<!--              HERE I AM DOING THE ROLE FILTER-->
            </div>

            <div class="right__filter__row">
<!--              HERE I AM DOING THE STATE FILTER-->

            </div>

          </div>
        </div>

        <div class="main__content">
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

                        <vs-th>
                            State
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

                        <vs-td>
                          {{ user.userData.user.is_active ? 'Active' : 'Inactive' }}
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
                                        <vs-button icon @click="editUserProfile(user.userData.user.id, user.role)">
                                            <box-icon
                                                name='comment-edit'
                                                animation='tada-hover'
                                            />
                                        </vs-button>

                                        <template #tooltip>
                                            Edit user
                                        </template>
                                    </vs-tooltip>

                                    <vs-tooltip v-if="user.userData.user.is_active">
                                        <vs-button warn icon @click="changeUserActivity(user)">
                                            <box-icon
                                                name='block'
                                                animation='tada-hover'
                                            />
                                        </vs-button>

                                        <template #tooltip>
                                            Make user inactive
                                        </template>
                                    </vs-tooltip>

                                    <vs-tooltip v-if="!user.userData.user.is_active">
                                        <vs-button success icon @click="changeUserActivity(user)">
                                            <box-icon
                                                name='check-circle'
                                                animation='tada-hover'
                                            />
                                        </vs-button>

                                        <template #tooltip>
                                            Make user active
                                        </template>
                                    </vs-tooltip>

                                    <vs-tooltip v-if="user.role !== 'Doctor'">
                                        <vs-button danger icon @click="deleteUserDialog(user)">
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
          <br>
            <template #footer>
                <div class="popup__right">
                    <vs-button
                        danger
                        border
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
import NotificationsUtils from "@/utils/notificationsUtils";
import HealthConcernsService from "@/services/healthConcernsService";

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

        filter: {
            user_role: -1,
            user_state: -1,  // active, inactive
        }
    }),

    async created() {
        await this.getAllUsers();
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

        async getFiltered() {
          HealthConcernsService.getFiltered(this.filter)
              .then(response => {
                  this.users = response.data;
              })
        },

        async changeUserActivity(user) {
            let newUserData = {...user.userData};
            newUserData.user_active = !newUserData.user_active;

            if(user.role === 'Doctor') {
                DoctorsService.update(user.userData.id, newUserData)
                    .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('User activity successfully changed.', this.$vs);
                    this.getAllUsers();
                    this.$forceUpdate();
                })
            }

            if(user.role === 'Health insurance worker') {
                HealthcareWorkersService.update(user.userData.id, newUserData)
                    .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('User activity successfully changed.', this.$vs);
                })
            }

            if(user.role === 'Patient') {
                PatientsService.update(user.userData.id, newUserData)
                    .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('User activity successfully changed.', this.$vs);
                })
            }
        },

        deleteUserDialog(user) {
          this.activeDelete = true;
          this.userToDelete = user;
        },

        async deleteUser() {
          if(this.userToDelete.role === 'Patient') {
            PatientsService.delete(this.userToDelete.userData.id)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Patient successfully deleted.', this.$vs);
                    this.getAllUsers();
                    this.activeDelete = false;
                    this.$forceUpdate();
                })
          }

          if(this.userToDelete.role === 'Health insurance worker') {
            HealthcareWorkersService.delete(this.userToDelete.userData.id)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Health insurance worker successfully deleted.', this.$vs);
                    this.getAllUsers();
                    this.activeDelete = false;
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