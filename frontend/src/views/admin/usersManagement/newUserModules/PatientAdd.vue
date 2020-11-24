<template>
    <div class="main__content">
        <h1>
            Add new patient
        </h1>

        <p>
            Create new patient in the database of patients.<br>
            Some of the basic patient information are necessary to state, but patient can manage his profile later.
        </p>

        <br>

        <div class="wrapper">
            <div class="first__row">
                <vs-input
                    v-model="newPatient.name"
                    label="Name of patient"
                    placeholder="Type name of new patient"
                    class="input__items"
                    primary
                >
                    <template
                        #message-warn
                        v-if="newPatient.name.length === 0"
                    >
                        Required
                    </template>
                </vs-input>

                <vs-input
                    type="date"
                    v-model="newPatient.date_of_birth"
                    label="Date of birth"
                    class="input__items"
                >
                  <template
                      #message-warn
                      v-if="!validDateOfBirth"
                  >
                      Required field
                   </template>
                </vs-input>
            </div>

            <div class="second__row">
                <vs-select
                    v-model="newPatient.main_doctor_id"
                    class="input__items"
                    label="Main doctor"
                    color="primary"
                >
                    <template
                        #message-warn
                        v-if="newPatient.main_doctor_id === -1"
                    >
                        Required
                    </template>

                    <vs-option
                        v-for="doctor in availableDoctors"
                        :key="doctor.id"
                        :label="doctor.name"
                        :value="doctor.id"
                    >
                        {{ doctor.name }}
                    </vs-option>
                </vs-select>

                <vs-select
                    v-model="newPatient.gender"
                    label="Sex"
                    color="primary"
                    class="input__items"
                 >
                   <vs-option
                      value="M"
                      label="Male"
                   >
                     Male
                   </vs-option>

                   <vs-option
                      value="F"
                      label="Female"
                   >
                     Female
                   </vs-option>

                   <vs-option
                      value="O"
                      label="Other"
                   >
                     Other
                   </vs-option>
                 </vs-select>
            </div>

            <div class="third__row">
                <vs-input
                    v-model="newPatient.email_field"
                    label="Email address"
                    class="input__items"
                >
                    <template
                        v-if="validEmail"
                        #message-success
                    >
                        Valid email
                    </template>

                    <template
                        v-if="!validEmail && newPatient.email_field !== ''"
                        #message-danger
                    >
                        Invalid email
                    </template>

                    <template
                        #message-warn
                        v-if="newPatient.email_field.length === 0"
                    >
                        Required
                    </template>
                </vs-input>

                <vs-input
                  v-model="newPatient.phone_number"
                  label="Phone number"
                  class="input__items"
                >
                  <template
                      v-if="validNumber"
                      #message-success
                  >
                      Valid phone number
                  </template>

                  <template
                      v-if="!validNumber && newPatient.phone_number !== ''"
                      #message-danger
                  >
                      Invalid phone number
                  </template>
                </vs-input>
            </div>

            <div class="submit__row">
                  <vs-button
                      @click="createPatient()"
                      :disabled=" newPatient.name.length === 0 ||
                                  newPatient.main_doctor_id === -1 ||
                                  !validDateOfBirth ||
                                  (!validEmail && newPatient.email_field.length !== 0) ||
                                  (!validNumber && newPatient.phone_number.length !== 0)"
                  >
                      Submit
                  </vs-button>
            </div>
        </div>
    </div>
</template>


<script>
import PatientsService from "@/services/patientsService";
import DoctorsService from "@/services/doctorsService";

import NotificationsUtils from "@/utils/notificationsUtils";
import DateUtils from "@/utils/dateUtils";

export default {
    name: 'PatientAdd',    

    data:() => ({
        newPatient: {
            'name': '',
            'gender': 'O',
            'main_doctor_id': -1,
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
        },

        availableDoctors: [],
    }),

    computed: {
        validEmail() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newPatient.email_field);
        },

        validNumber() {
          return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newPatient.phone_number);
        },

        validDateOfBirth() {
          return this.newPatient.date_of_birth.length !== 0;
        }
    },

    async created() {
        DoctorsService.getAll()
            .then(response => {
            this.availableDoctors = response.data;
            })
    },

    methods: {
        async createPatient() {
            let data = {
                name: this.newPatient.name,
                gender: this.newPatient.gender,
                main_doctor: this.newPatient.main_doctor_id,
                date_of_birth: DateUtils.getDateForBackend(this.newPatient.date_of_birth),
                email_field: this.newPatient.email_field,
                phone_number: this.newPatient.phone_number
            };

            if(data.date_of_birth === '') {
                data.date_of_birth = null;
            }

            PatientsService.create(data)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('New patient was added to the database.', this.$vs);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
        },
    },
}
</script>

<style scoped>
    .input__items {
        padding: 16px 0;
        margin-left: 6px;
    }

    .vs-button {
        float: right;
        padding: 5px 30px;
    }
</style>
