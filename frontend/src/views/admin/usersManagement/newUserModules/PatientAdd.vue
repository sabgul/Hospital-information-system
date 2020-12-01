<template>
    <div>
        <div class="main__content">
            <h1>
                Add new patient
            </h1>

            <p>
                In this module profile of a new patient can be created. <br>
                Please fill in all the required fields. In order to provide the patient with secure password, you can follow recommended guidelines described by bar appearing above the password field. <br>
                Any desired modifications can be done in the future, by editing patient's profile.
            </p>
        </div>

        <form action="#" v-on:submit.prevent="createPatient">
            <div class="main__content">
                <h5>
                    Basic information
                </h5>

                <div class="wrapper">
                    <div class="first__row">
                        <vs-input
                            v-model="newPatient.first_name"
                            label="First name of patient"
                            placeholder="Type first name"
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
                            placeholder="Type last name"
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
                    </div>

                    <div class="second__row">
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

                    <div class="third__row">
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
                </div>
            </div>

            <div class="main__content">
                <h5>
                    System access information
                </h5>

                <div class="wrapper">
                    <div class="first__row">
                        <vs-input
                          v-model="newPatient.email_field"
                          label="Email address"
                          placeholder="Type email address"
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
                    </div>

                    <div class="second__row">
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
                    </div>
                </div>
            </div>

            <div class="main__content">
                <h5>
                    Emergency contact information
                </h5>

                <div class="wrapper">
                    <div class="first__row">
                        <vs-input
                            v-model="newPatient.ec_first_name"
                            label="First name of emergency contact"
                            placeholder="Type first name here"
                            class="input__items"
                            primary
                        >
                            <template
                                #message-danger
                                v-if="newPatient.ec_first_name.length >= 30"
                            >
                                Name too long
                            </template>
                        </vs-input>

                        <vs-input
                            v-model="newPatient.ec_last_name"
                            label="Last name of emergency contact"
                            placeholder="Type last name here"
                            class="input__items"
                            primary
                        >
                            <template
                                #message-danger
                                v-if="newPatient.ec_last_name.length >= 30"
                            >
                                Name too long
                            </template>
                        </vs-input>
                    </div>

                    <div class="second__row">
                        <vs-input
                            v-model="newPatient.ec_relationship"
                            label="Relationship"
                            placeholder="Type relationship here"
                            class="input__items"
                            primary
                        >
                            <template
                                #message-danger
                                v-if="newPatient.ec_relationship.length >= 30"
                            >
                                Text too long
                            </template>
                        </vs-input>
                    </div>

                    <div class="third__row">
                        <vs-input
                            v-model="newPatient.ec_contact_number"
                            label="Phone of emergency contact"
                            placeholder="Eg +42012312313"
                            class="input__items"
                        >
                            <template
                                v-if="validContactNum"
                                #message-success
                            >
                                Valid phone number
                            </template>

                            <template
                                v-if="(!validContactNum && newPatient.ec_contact_number !== '') || newPatient.ec_contact_number.length > 13"
                                #message-danger
                            >
                                Invalid or too long phone number
                            </template>
                        </vs-input>
                    </div>
                </div>
            </div>

            <div class="main__content">
                <h5>
                    Medical information
                </h5>

                <div class="wrapper">
                    <div class="first__row">
                        <vs-input
                            v-model="newPatient.height"
                            label="Height(in cm)"
                            class="input__items"
                            type="number"
                            min="0"
                            :change="checkNum()"
                        />

                        <vs-input
                            v-model="newPatient.weight"
                            label="Weight(in kg)"
                            class="input__items"
                            type="number"
                            min="0"
                            :change="checkNum()"
                        />
                    </div>

                    <div class="second__row">
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
                        <vs-switch
                            v-model="newPatient.taking_medications"
                            class="input_switch"
                        >
                            <template #off>
                                No medications
                            </template>

                            <template #on>
                                Takes medications
                            </template>
                        </vs-switch>

                        <vs-input
                            v-if="newPatient.taking_medications"
                            v-model="newPatient.medications"
                            class="input__items vs-input__wide"
                            label="List medications"
                            placeholder="Medications taken by patient"
                        >
                            <template
                                #message-danger
                                v-if="newPatient.medications.length >= 2046"
                            >
                                Text too long
                            </template>
                        </vs-input>
                    </div>
                </div>
            </div>

            <div class="main__content">
                <h5>
                    Submit
                </h5>

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
                                    newPatient.email_field.length >= 40 ||
                                    newPatient.ec_first_name.length >= 30 ||
                                    newPatient.ec_last_name.length >= 30 ||
                                    (!validContactNum && newPatient.ec_contact_number.length !== 0) ||
                                    newPatient.ec_relationship.length >= 30 ||
                                    newPatient.medications.length >= 2046"
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
            'date_of_birth': '',
            'phone_number': '',

            'email_field': '',
            'password': '',

            'main_doctor_id': -1,
            'weight': 0,
            'height': 0,
            'taking_medications': false,
            'medications': '',

            'ec_first_name': '',
            'ec_last_name': '',
            'ec_relationship': '',
            'ec_contact_number': '',
        },

        availableDoctors: [],
    }),

    computed: {
        getProgress() {
            let progress = 0;

            // at least one number
            if (/\d/.test(this.newPatient.password)) {
                progress += 20;
            }

            // at least one capital letter
            if (/(.*[A-Z].*)/.test(this.newPatient.password)) {
                progress += 20;
            }

            // at least one lowercase
            if (/(.*[a-z].*)/.test(this.newPatient.password)) {
                progress += 20;
            }

            // more than 5 digits
            if (this.newPatient.password.length >= 6) {
                progress += 20;
            }

            // at least one special character
            if (/[^A-Za-z0-9]/.test(this.newPatient.password)) {
                progress += 20;
            }

            return progress;
        },

        validEmail() {
            return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newPatient.email_field);
        },

        validNumber() {
            return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newPatient.phone_number);
        },

        validContactNum() {
            return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newPatient.ec_contact_number);
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
        clearMedications() {
          this.newPatient.medications = '';
        },

        checkNum() {
            if(this.newPatient.height < 0) {
                this.newPatient.height = 0;
            }

            if(this.newPatient.weight < 0) {
                this.newPatient.weight = 0;
            }
        },

        async createPatient() {
            let data = {
                first_name: this.newPatient.first_name,
                last_name: this.newPatient.last_name,
                gender: this.newPatient.gender,
                date_of_birth: DateUtils.getDateForBackend(this.newPatient.date_of_birth),
                phone_number: this.newPatient.phone_number,

                email: this.newPatient.email_field,
                password: this.newPatient.password,


                main_doctor: this.newPatient.main_doctor_id,
                weight: this.newPatient.weight,
                height: this.newPatient.height,
                taking_medications: this.newPatient.taking_medications,
                medications: this.newPatient.taking_medications ? this.newPatient.medications : '',

                ec_first_name: this.newPatient.ec_first_name,
                ec_last_name: this.newPatient.ec_last_name,
                ec_relationship: this.newPatient.ec_relationship,
                ec_contact_number: this.newPatient.ec_contact_number,
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
                'date_of_birth': '',
                'phone_number': '',

                'email_field': '',
                'password': '',

                'main_doctor_id': this.userRole === 'admin' ? -1 : this.user.id,
                'weight': 0,
                'height': 0,
                'taking_medications': false,
                'medications': '',

                'ec_first_name': '',
                'ec_last_name': '',
                'ec_relationship': '',
                'ec_contact_number': '',
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

    .input_switch {
        margin-bottom: 2.5em;
        width: 8em;
    }

    .submit__row {
      margin-top: 1em !important;
    }

</style>
