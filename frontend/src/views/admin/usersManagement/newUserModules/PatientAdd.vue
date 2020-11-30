<template>
    <div class="main__content">
        <h1>
            Add new patient
        </h1>

        <p>
            Create a new patient.<br>
              Some fields are required but can be edited later.
        </p>

        <br>

        <form action="#" v-on:submit.prevent="createPatient">
            <div class="wrapper">
                <div class="first__row">
                    <vs-input
                        v-model="newPatient.first_name"
                        label="First name of patient"
                        placeholder="Type first name of new patient"
                        class="input__items"
                        primary
                    >
                        <template
                            #message-warn
                            v-if="newPatient.first_name.length === 0"
                        >
                            Required
                        </template>

                        <template
                            #message-danger
                            v-if="newPatient.first_name.length >= 30"
                        >
                            Name too long
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newPatient.last_name"
                        label="Last name of patient"
                        placeholder="Type last name of new patient"
                        class="input__items"
                        primary
                    >
                        <template
                            #message-warn
                            v-if="newPatient.last_name.length === 0"
                        >
                            Required
                        </template>

                        <template
                            #message-danger
                            v-if="newPatient.last_name.length >= 30"
                        >
                            Name too long
                        </template>
                    </vs-input>

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

                <div class="second__row">
                     <vs-input
                        v-model="newPatient.email_field"
                        label="Email address"
                        class="input__items"
                     >
                        <template
                            v-if="validEmail && newPatient.email_field.length < 40"
                            #message-success
                        >
                            Valid email
                        </template>

                        <template
                            v-if="(!validEmail && newPatient.email_field !== '') || newPatient.email_field.length >= 40"
                            #message-danger
                        >
                            Invalid or too long email
                        </template>

                        <template
                            #message-warn
                            v-if="newPatient.email_field.length === 0"
                        >
                            Required
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newPatient.password"
                        label="Password"
                        placeholder="Type password"
                        class="input__items"
                        type="password"
                        :progress="getProgress"
                        :visible-password="hasVisiblePassword"
                        @click-icon="hasVisiblePassword = !hasVisiblePassword"
                        icon-after
                        primary
                    >
                        <template #icon>
                           <box-icon v-if="!hasVisiblePassword" name="hide" />
                           <box-icon v-else name="show" />
                        </template>

                        <template v-if="getProgress >= 100" #message-success>
                              Secure password
                        </template>

                        <template
                            v-if="newPatient.password.length === 0"
                            #message-warn
                        >
                            Required
                        </template>

                        <template
                            v-if="newPatient.password.length >= 128"
                            #message-danger
                        >
                            Password too long
                        </template>
                    </vs-input>

                    <vs-select
                        v-if="userRole === 'admin'"
                        v-model="newPatient.main_doctor_id"
                        class="input__items"
                        label="Main doctor"
                        color="primary"
                        :key="availableDoctors.length"
                    >
                        <template
                            #message-warn
                            v-if="newPatient.main_doctor_id === -1"
                        >
                            Required
                        </template>

                        <vs-option
                            v-for="doctor in availableDoctors"
                            :key="doctor.user.id"
                            :label="getFullName(doctor.user)"
                            :value="doctor.user.id"
                        >
                            {{ doctor.user.first_name }} {{ doctor.user.last_name }}
                        </vs-option>
                    </vs-select>
                </div>

                <div class="third__row">
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

                    <vs-input
                        v-model="newPatient.phone_number"
                        label="Phone number"
                        placeholder="Eg +42012312313"
                        class="input__items"
                    >
                        <template
                            v-if="validNumber"
                            #message-success
                        >
                            Valid phone number
                        </template>

                        <template
                            v-if="(!validNumber && newPatient.phone_number !== '') || newPatient.phone_number.length > 13"
                            #message-danger
                        >
                            Invalid or too long phone number
                        </template>
                    </vs-input>
                </div>

                <div class="submit__row">
                    <vs-button
                        :disabled=" newPatient.first_name.length === 0 ||
                                    newPatient.first_name.length >= 30 ||
                                    newPatient.last_name.length === 0 ||
                                    newPatient.last_name.length >= 30 ||
                                    (newPatient.main_doctor_id === -1  && userRole === 'admin') ||
                                    !validDateOfBirth ||
                                    (!validEmail && newPatient.email_field.length !== 0) ||
                                    (!validNumber && newPatient.phone_number.length !== 0) ||
                                    newPatient.password.length >= 128 ||
                                    newPatient.phone_number.length > 13 ||
                                    newPatient.email_field.length >= 40"
                    >
                        Submit
                    </vs-button>
                </div>
            </div>
        </form>
    </div>
</template>


<script>
import PatientsService from "@/services/patientsService";
import DoctorsService from "@/services/doctorsService";

import NotificationsUtils from "@/utils/notificationsUtils";
import DateUtils from "@/utils/dateUtils";
import {mapState} from "vuex";

export default {
    name: 'PatientAdd',    

    data:() => ({
        hasVisiblePassword: false,
        newPatient: {
            'first_name': '',
            'last_name': '',
            'gender': 'O',
            'main_doctor_id': -1,
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
            'password': '',
        },

        availableDoctors: [],
    }),

    computed: {
        getProgress() {
          let progress = 0

          // at least one number

          if (/\d/.test(this.newPatient.password)) {
            progress += 20
          }

          // at least one capital letter

          if (/(.*[A-Z].*)/.test(this.newPatient.password)) {
            progress += 20
          }

          // at least one lowercase

          if (/(.*[a-z].*)/.test(this.newPatient.password)) {
            progress += 20
          }

          // more than 5 digits

          if (this.newPatient.password.length >= 6) {
            progress += 20
          }

          // at least one special character

          if (/[^A-Za-z0-9]/.test(this.newPatient.password)) {
            progress += 20
          }

          return progress
        },

        validEmail() {
            return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newPatient.email_field);
        },

        validNumber() {
            return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newPatient.phone_number);
        },

        validDateOfBirth() {
            return this.newPatient.date_of_birth.length !== 0;
        },

        ...mapState([
            'user',
            'userRole',
        ]),
    },

    async created() {
        if(this.userRole === 'admin') {
            DoctorsService.getAll()
            .then(response => {
                this.availableDoctors = response.data;
            })
        } else {
          this.newPatient.main_doctor_id = this.user.id;
        }
    },

    methods: {
        async createPatient() {
            let data = {
                first_name: this.newPatient.first_name,
                last_name: this.newPatient.last_name,
                gender: this.newPatient.gender,
                main_doctor: this.newPatient.main_doctor_id,
                date_of_birth: DateUtils.getDateForBackend(this.newPatient.date_of_birth),
                email: this.newPatient.email_field,
                phone_number: this.newPatient.phone_number,
                password: this.newPatient.password,
            };

            if(data.date_of_birth === '') {
                data.date_of_birth = null;
            }

            PatientsService.create(data)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('New patient was added to the database.', this.$vs);
                this.clearFields();
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });
        },

        getFullName(usr) {
          return usr.first_name + ' ' + usr.last_name;
        },

        clearFields() {
            this.newPatient = {
                'first_name': '',
                'last_name': '',
                'gender': 'O',
                'main_doctor_id': this.userRole === 'admin' ? -1 : this.user.id,
                'date_of_birth': '',
                'email_field': '',
                'phone_number': '',
                'password': '',
            }
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

    box-icon {
        fill: #000;
    }
</style>
