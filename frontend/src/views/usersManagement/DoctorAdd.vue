<template>
    <div>
        <div class="main__content">
            <h1>
                Add new doctor
            </h1>

            <p>
                Create new doctor in the database of doctors.<br>
                Some of the basic patient information are necessary to state, but doctor(or you) can manage his profile later.
            </p>

            <br>


            <div class="wrapper">
                <div class="first__row">
                    <vs-input
                        v-model="newDoctor.name"
                        label="Name of doctor"
                        placeholder="Type name of new doctor"
                        class="input__items"
                        primary
                    >
                        <template
                            #message-warn
                            v-if="newDoctor.name.length === 0"
                        >
                            Required
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
                        type="date"
                        v-model="newDoctor.date_of_birth"
                        label="Date of birth"
                        class="input__items"
                    >
                        <template
                            #message-warn
                            v-if="newDoctor.date_of_birth === ''"
                        >
                            Required field
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newDoctor.specializes_in"
                        label="Specializes in"
                        placeholder="Type specialization"
                        class="input__items"
                    >
                        <template
                            v-if="newDoctor.specializes_in.length >= 250"
                            #message-danger
                        >
                            Text too long
                        </template>
                    </vs-input>
                </div>

                <div class="third__row">
                      <vs-input
                          v-model="newDoctor.email_field"
                          label="Email address"
                          placeholder="Type email"
                          class="input__items"
                      >
                          <template
                              v-if="validEmail"
                              #message-success
                          >
                              Valid email
                          </template>

                          <template
                              v-if="!validEmail && newDoctor.email_field !== ''"
                              #message-danger
                          >
                              Invalid email
                          </template>

                          <template
                              #message-warn
                              v-if="newDoctor.email_field.length === 0"
                          >
                              Required
                          </template>
                      </vs-input>

                      <vs-input
                          v-model="newDoctor.phone_number"
                          label="Phone number"
                          placeholder="Type phone number"
                          class="input__items"
                      >
                          <template
                              v-if="validNumber"
                              #message-success
                          >
                              Valid phone number
                          </template>

                          <template
                              v-if="!validNumber && newDoctor.phone_number !== ''"
                              #message-danger
                          >
                              Invalid phone number
                          </template>
                      </vs-input>
                </div>

                <div class="submit__row">
                    <vs-button
                        @click="createDoctor()"
                        :disabled=" newDoctor.name.length === 0 ||
                                    newDoctor.main_doctor_id === -1 ||
                                    newDoctor.date_of_birth === '' ||
                                    (!validEmail && newDoctor.email_field.length !== 0) ||
                                    (!validNumber && newDoctor.phone_number.length !== 0)"
                    >
                        Submit
                    </vs-button>
                </div>
            </div>
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
        newDoctor: {
            'name': '',
            'gender': 'O',
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
            'specializes_in': '',
        },
    }),

    computed: {
        validEmail() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newDoctor.email_field);
        },

        validNumber() {
          return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newDoctor.phone_number);
        },
    },

    methods: {
        createDoctor() {
            let data = {
                name: this.newDoctor.name,
                gender: this.newDoctor.gender,
                specializes_in: this.newDoctor.specializes_in,
                date_of_birth: DateUtils.getDateForBackend(this.newDoctor.date_of_birth),
                email_field: this.newDoctor.email_field,
                phone_number: this.newDoctor.phone_number
            };

            if(data.date_of_birth === '') {
                data.date_of_birth = null;
            }

            DoctorsService.create(data)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('New doctor was added to the database.', this.$vs);
            })
            .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
            });
        }
    },
}
</script>

<style scoped>
    .input__items {
        padding: 16px 0;
        margin-left: 6px;
    }
</style>