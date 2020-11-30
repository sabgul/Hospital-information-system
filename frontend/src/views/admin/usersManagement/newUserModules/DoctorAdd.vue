<template>
    <div>
        <div class="main__content">
            <h1>
                Add new doctor
            </h1>

            <p>
                Create a new doctor in the database of doctors.<br>
                Some fields are required. Profile details can be edited later.
            </p>

            <br>

            <form action="#" v-on:submit.prevent="createDoctor">
                <div class="wrapper">
                    <div class="first__row">
                        <vs-input
                            v-model="newDoctor.first_name"
                            label="First name of doctor"
                            placeholder="Type first name of new doctor"
                            class="input__items"
                            primary
                        >
                            <template
                                #message-warn
                                v-if="newDoctor.first_name.length === 0"
                            >
                                Required
                            </template>

                            <template
                                #message-danger
                                v-if="newDoctor.first_name.length >= 30"
                            >
                                Name too long
                            </template>
                        </vs-input>

                        <vs-input
                            v-model="newDoctor.last_name"
                            label="Last name of doctor"
                            placeholder="Type last name of new doctor"
                            class="input__items"
                            primary
                        >
                            <template
                                #message-warn
                                v-if="newDoctor.last_name.length === 0"
                            >
                                Required
                            </template>

                            <template
                                #message-danger
                                v-if="newDoctor.last_name.length >= 30"
                            >
                                Name too long
                            </template>
                        </vs-input>

                        <vs-select
                            v-model="newDoctor.gender"
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
                            v-model="newDoctor.email_field"
                            label="Email address"
                            placeholder="Type email"
                            class="input__items"
                            primary
                        >
                            <template
                                v-if="validEmail && newDoctor.email_field.length < 40"
                                #message-success
                            >
                                Valid email
                            </template>

                            <template
                                v-if="(!validEmail && newDoctor.email_field !== '') || newDoctor.email_field.length >= 40"
                                #message-danger
                            >
                                Invalid or too long email
                            </template>

                            <template
                                #message-warn
                                v-if="newDoctor.email_field.length === 0"
                            >
                                Required
                            </template>
                        </vs-input>

                        <vs-input
                            v-model="newDoctor.password"
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
                              <box-icon v-if="!hasVisiblePassword" name="hide"/>
                              <box-icon v-else name="show"/>
                            </template>

                            <template v-if="getProgress >= 100" #message-success>
                              Secure password
                            </template>

                            <template
                                v-if="newDoctor.password.length === 0"
                                #message-warn
                            >
                                Required
                            </template>

                            <template
                                v-if="newDoctor.password.length >= 128"
                                #message-danger
                            >
                                Password too long
                            </template>
                        </vs-input>

                        <vs-input
                            v-model="newDoctor.specializes_in"
                            label="Specializes in"
                            placeholder="Type specialization"
                            class="input__items"
                        >
                            <template
                                v-if="newDoctor.specializes_in.length >= 254"
                                #message-danger
                            >
                                Specialization too long
                            </template>
                        </vs-input>
                    </div>

                    <div class="third__row">
                          <vs-input
                              type="date"
                              v-model="newDoctor.date_of_birth"
                              label="Date of birth"
                              class="input__items"
                              primary
                          >
                              <template
                                  #message-warn
                                  v-if="newDoctor.date_of_birth === ''"
                              >
                                  Required field
                              </template>
                          </vs-input>

                          <vs-input
                              v-model="newDoctor.phone_number"
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
                                  v-if="(!validNumber && newDoctor.phone_number !== '') || newDoctor.phone_number.length > 13"
                                  #message-danger
                              >
                                  Invalid or too long phone number
                              </template>
                          </vs-input>
                    </div>

                    <div class="submit__row">
                        <vs-button
                            :disabled=" newDoctor.first_name.length === 0 ||
                                        newDoctor.first_name.length >= 30 ||
                                        newDoctor.last_name.length === 0 ||
                                        newDoctor.last_name.length >= 30 ||
                                        newDoctor.main_doctor_id === -1 ||
                                        newDoctor.date_of_birth === '' ||
                                        newDoctor.password.length === 0 ||
                                        (!validEmail && newDoctor.email_field.length !== 0) ||
                                        (!validNumber && newDoctor.phone_number.length !== 0) ||
                                        newDoctor.password.length >= 128 ||
                                        newDoctor.phone_number.length > 13 ||
                                        newDoctor.email_field.length >= 40 ||
                                        newDoctor.specializes_in.length >= 254"
                        >
                            Submit
                        </vs-button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import DoctorsService from "@/services/doctorsService";

import DateUtils from "@/utils/dateUtils";
import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: "DoctorAdd",

    data:() => ({
        hasVisiblePassword: false,
        newDoctor: {
            'first_name': '',
            'last_name': '',
            'gender': 'O',
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
            'specializes_in': '',
            'password': '',
        },
    }),

    computed: {
        getProgress() {
          let progress = 0

          // at least one number

          if (/\d/.test(this.newDoctor.password)) {
            progress += 20
          }

          // at least one capital letter

          if (/(.*[A-Z].*)/.test(this.newDoctor.password)) {
            progress += 20
          }

          // at least one lowercase

          if (/(.*[a-z].*)/.test(this.newDoctor.password)) {
            progress += 20
          }

          // more than 5 digits

          if (this.newDoctor.password.length >= 6) {
            progress += 20
          }

          // at least one special character

          if (/[^A-Za-z0-9]/.test(this.newDoctor.password)) {
            progress += 20
          }

          return progress
        },

        validEmail() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newDoctor.email_field);
        },

        validNumber() {
          return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newDoctor.phone_number);
        },
    },

    methods: {
        async createDoctor() {
            let data = {
                first_name: this.newDoctor.first_name,
                last_name: this.newDoctor.last_name ,
                gender: this.newDoctor.gender,
                specializes_in: this.newDoctor.specializes_in,
                date_of_birth: DateUtils.getDateForBackend(this.newDoctor.date_of_birth),
                email: this.newDoctor.email_field,
                phone_number: this.newDoctor.phone_number,
                password: this.newDoctor.password,
            };

            if(data.date_of_birth === '') {
                data.date_of_birth = null;
            }

            DoctorsService.create(data)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('New doctor was added to the database.', this.$vs);
                this.clearFields();
            })
            .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
            });
        },

        clearFields() {

            this.newDoctor = {
                'first_name': '',
                'last_name': '',
                'gender': 'O',
                'date_of_birth': '',
                'email_field': '',
                'phone_number': '',
                'specializes_in': '',
                'password': '',
            }
        }
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
