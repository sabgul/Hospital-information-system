<template>
    <div>
        <div class="main__content">
          <h1>
            Editing <b>{{ userData.first_name }} {{ userData.last_name }}</b>'s profile
          </h1>
        </div>

        <div class="main__content">
          <div class="wrapper">
                <div class="first__row">
                    <vs-input
                        label="First name"
                        color="primary"
                        v-model="newUserData.first_name"
                    >
                      <template #message-danger v-if="newUserData.first_name.length === 0">
                        Required
                      </template>
                    </vs-input>

                    <br>

                    <vs-input
                        label="Last name"
                        color="primary"
                        v-model="newUserData.last_name"
                    >
                      <template #message-danger v-if="newUserData.last_name.length === 0">
                        Required
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
<!--                  <vs-input-->
<!--                      v-if="role === 'doctor'"-->
<!--                      label="Doctor specialisation"-->
<!--                      color="primary"-->
<!--                      v-model="newUserData.specializes_in"-->
<!--                  />-->

<!--                  <vs-input-->
<!--                      v-if="role === 'health-insurance-worker'"-->
<!--                      label="Insurance company"-->
<!--                      color="primary"-->
<!--                      v-model="newUserData.works_for_company"-->
<!--                  />-->

                  <vs-select
                      v-if="role === 'patient'"
                      v-model="newUserData.main_doctor"
                      label="Main doctor"
                  >
<!--                    TODO: DOES NOT WORK!-->
                     <vs-option v-for="doctor in doctors" :key="doctor.user.id" :label="doctor.user.first_name" :value="doctor.user.id">
                        {{ doctor.user.first_name }}
                    </vs-option>
                  </vs-select>

                </div>

                <div class="submit__row" style="margin-bottom: 5em; margin-top: 2em;">
                    <vs-button @click="resetUserData" style="padding: 3px 25px;" border>
                        Reset unsaved
                    </vs-button>

                    <vs-button
                        @click="saveChanges"
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
// import HealthcareWorkersService from "@/services/healthcareWorkersService";
import UsersService from "@/services/usersService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'EditProfile',

    props: {
        id: String,
        role: String,
    },

    data:() => ({
      userData: {},
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
      UsersService.get(this.id)
          .then(response => {
              this.userData = response.data;
              this.newUserData = {...this.userData};
            })

      if(this.role === 'patient') {
          PatientsService.get(this.id)
          .then(response => {
            console.log(response.data);
              this.userData = response.data;
              this.newUserData = {...this.userData};
          })
      }

      if(this.role === 'doctor') {
          DoctorsService.get(this.id)
          .then(response => {
              this.userData = response.data;
              this.newUserData = {...this.userData};
          })
      }

      // if(this.role === 'health-insurance-worker') {
      //     HealthcareWorkersService.get(this.id)
      //     .then(response => {
      //       console.log(response.data);
      //         this.userData = response.data;
      //         this.newUserData = {...this.userData};
      //     })
      // }
    },

    methods: {
        formatDate(date) {
          console.log(date);
            const day = date.slice(8, 10);
            const month = date.slice(5, 7);
            const year = date.slice(0, 4);

            return year + '-' + month + '-' + day
        },

        resetUserData() {
          this.newUserData = {...this.userData};
        },

        saveChanges() {
          let updatedInfo;

          if(this.role === 'doctor') {
            updatedInfo = {
              user: {
                first_name: this.newUserData.user.first_name,
                last_name: this.newUserData.user.last_name,
                date_of_birth: this.formatDate(this.newUserData.user.date_of_birth),
                phone_number: this.newUserData.user.phone_number,
              },
              specializes_in: this.newUserData.specializes_in,
            };

            DoctorsService.update(this.id, updatedInfo)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('User data successfully edited.', this.$vs);
                this.userData = {...updatedInfo};
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });
          }

          if(this.role === 'health-insurance-worker') {
            // updatedInfo = {
            //   // user: {
            //     first_name: this.newUserData.user.first_name,
            //     last_name: this.newUserData.user.last_name,
            //     date_of_birth: this.formatDate(this.newUserData.user.date_of_birth),
            //     phone_number: this.newUserData.user.phone_number,
            //   // },
            //   // works_for_company: this.newUserData.works_for_company
            // };

            UsersService.update(this.id, this.newUserData)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('User data successfully edited.', this.$vs);
                // this.userData = {...updatedInfo};
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
