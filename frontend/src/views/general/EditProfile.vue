<template>
    <div>
        <div class="main__content">
          <h1>
            Editing <b>{{ user.name }}</b>'s profile
          </h1>
        </div>

        <div class="main__content">
          <div class="wrapper">
                <div class="first__row">
                    <vs-input
                        label="Name"
                        color="primary"
                        v-model="newUserData.name"
                    >
                      <template #message-danger v-if="newUserData.name.length === 0">
                        Required
                      </template>
                    </vs-input>

                  <br>

                  <vs-input
                      label="Email"
                      color="primary"
                      v-model="newUserData.email_field"
                  >
                    <template #message-danger v-if="!isEmailValid">
                      Valid email required
                    </template>
                  </vs-input>
                </div>

                <div class="second__row">
                    <vs-input
                        v-model="newUserData.date_of_birth"
                        label="Date of birth"
                        color="primary"
                        type="date"
                    />

                  <br>

                  <vs-input
                      label="Phone number"
                      color="primary"
                      v-model="newUserData.phone_number"
                  />
                </div>

                <div class="third__row">
                  <vs-input
                      v-if="role === 'doctor'"
                      label="Doctor specialisation"
                      color="primary"
                      v-model="newUserData.specializes_in"
                  />

                  <vs-input
                      v-if="role === 'health-insurance-worker'"
                      label="Insurance company"
                      color="primary"
                      v-model="newUserData.works_for_company"
                  />

                  <vs-select
                      v-if="role === 'patient'"
                      v-model="newUserData.main_doctor"
                      label="Main doctor"
                  >
<!--                    TODO: DOES NOT WORK!-->
                     <vs-option v-for="doctor in doctors" :key="doctor.id" :label="doctor.name" :value="doctor.id">
                        {{ doctor.name }}
                    </vs-option>
                  </vs-select>

                </div>

                <div class="submit__row" style="margin-bottom: 5em; margin-top: 2em;">
                    <vs-button @click="resetUserData" style="padding: 3px 25px;" border>
                        Reset unsaved
                    </vs-button>

                    <vs-button
                        @click="saveChanges"
                        :disabled="!isEmailValid"
                        style="padding: 3px 28px;">
                        Save changes
                    </vs-button>
                </div>
            </div>
        </div>

        <img src="../../assets/profile_edit.svg" alt="" class="background__img">
    </div>
</template>


<script>
import PatientsService from "@/services/patientsService";
import DoctorsService from "@/services/doctorsService";
import HealthcareWorkersService from "@/services/healthcareWorkersService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'EditProfile',

    props: {
        id: String,
        role: String,
    },

    data:() => ({
      user: {},
      newUserData: {},
      doctors: [],
    }),

    async mounted() {
        DoctorsService.getAll()
            .then(response => {
            this.doctors = response.data;
            })
    },

    async created() {
      if(this.role === 'patient') {
          PatientsService.get(this.id)
          .then(response => {
              this.user = response.data;
              this.newUserData = {...this.user};
          })
      }

      if(this.role === 'doctor') {
          DoctorsService.get(this.id)
          .then(response => {
              this.user = response.data;
              this.newUserData = {...this.user};
          })
      }

      if(this.role === 'health-insurance-worker') {
          HealthcareWorkersService.get(this.id)
          .then(response => {
              this.user = response.data;
              this.newUserData = {...this.user};
          })
      }
    },

    computed: {
        isEmailValid() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newUserData.email_field);
        },
    },

    methods: {
        formatDate(date) {
            const day = date.slice(8, 10);
            const month = date.slice(5, 7);
            const year = date.slice(0, 4);

            return year + '-' + month + '-' + day
        },

        resetUserData() {
          this.newUserData = {...this.user};
        },

        saveChanges() {
          let updatedInfo;

          if(this.role === 'doctor') {
            updatedInfo = {
              name: this.newUserData.name,
              date_of_birth: this.formatDate(this.newUserData.date_of_birth),
              email_field: this.newUserData.email_field,
              phone_number: this.newUserData.phone_number,
              specializes_in: this.newUserData.specializes_in,
              user_active: true,
              active_from: this.formatDate(this.user.active_from)
            };

            DoctorsService.update(this.id, updatedInfo)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('User data successfully edited.', this.$vs);
                this.user = {...updatedInfo};
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });
          }

          if(this.role === 'health-insurance-worker') {
            updatedInfo = {
              name: this.newUserData.name,
              date_of_birth: this.formatDate(this.newUserData.date_of_birth),
              email_field: this.newUserData.email_field,
              phone_number: this.newUserData.phone_number,
              user_active: true,
              active_from: this.formatDate(this.user.active_from),
              works_for_company: this.newUserData.works_for_company
            };

            HealthcareWorkersService.update(this.id, updatedInfo)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('User data successfully edited.', this.$vs);
                this.user = {...updatedInfo};
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });
          }
        }
    },
}
</script>

<style scoped>
    box-icon {
        fill: #fbfbfb;
    }

    .background__img {
      position: absolute;
      right: 0;
      bottom: 0;
      width: 35%;
    }
</style>
