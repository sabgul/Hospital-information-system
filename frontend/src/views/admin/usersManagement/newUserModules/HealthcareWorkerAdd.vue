<template>
    <div>
        <div class="main__content">
            <h1>
                Add new healthcare worker
            </h1>

            <p>
                Create new healthcare worker.<br>
                Some fields are required. Profile details can be edited later.
            </p>

            <br>

            <div class="wrapper">
                <div class="first__row">
                    <vs-input
                        v-model="newWorker.first_name"
                        label="First name of worker"
                        placeholder="Type first name"
                        class="input__items"
                        primary
                    >
                        <template
                            #message-warn
                            v-if="newWorker.first_name.length === 0"
                        >
                            Required
                        </template>

                        <template
                            #message-danger
                            v-if="newWorker.first_name.length >= 30"
                        >
                            Name too long
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newWorker.last_name"
                        label="Last name of worker"
                        placeholder="Type last name"
                        class="input__items"
                        primary
                    >
                        <template
                            #message-warn
                            v-if="newWorker.last_name.length === 0"
                        >
                            Required
                        </template>

                        <template
                            #message-danger
                            v-if="newWorker.last_name.length >= 30"
                        >
                            Name too long
                        </template>
                    </vs-input>

                    <vs-select
                        v-model="newWorker.gender"
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
                        v-model="newWorker.email_field"
                        label="Email address"
                        placeholder="Type email"
                        class="input__items"
                    >
                        <template
                            v-if="validEmail && newWorker.email_field.length < 40"
                            #message-success
                        >
                            Valid email
                        </template>

                        <template
                            v-if="(!validEmail && newWorker.email_field !== '') || newWorker.email_field.length >= 40"
                            #message-danger
                        >
                            Invalid or too long email
                        </template>

                        <template
                            #message-warn
                            v-if="newWorker.email_field.length === 0"
                        >
                            Required
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newWorker.password"
                        label="Password"
                        placeholder="Type password"
                        class="input__items"
                        type="password"
                        primary
                    >
                        <template
                            v-if="newWorker.password.length === 0"
                            #message-warn
                        >
                            Required
                        </template>

                        <template
                            v-if="newWorker.password.length >= 128"
                            #message-danger
                        >
                            Password too long
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newWorker.works_for_company"
                        label="Works for company"
                        placeholder="Name of company"
                        class="input__items"
                    >
                        <template
                            v-if="newWorker.works_for_company.length >= 254"
                            #message-danger
                        >
                            Company name too long
                        </template>
                    </vs-input>
                </div>

                <div class="third__row">
                      <vs-input
                          type="date"
                          v-model="newWorker.date_of_birth"
                          label="Date of birth"
                          class="input__items"
                      >
                          <template
                              #message-warn
                              v-if="newWorker.date_of_birth === ''"
                          >
                              Required field
                          </template>
                      </vs-input>

                      <vs-input
                          v-model="newWorker.phone_number"
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
                              v-if="(!validNumber && newWorker.phone_number !== '') || newWorker.phone_number.length > 13"
                              #message-danger
                          >
                              Invalid or too long phone number
                          </template>
                      </vs-input>
                </div>

                <div class="submit__row">
                    <vs-button
                        @click="createWorker()"
                        :disabled=" newWorker.first_name.length === 0 ||
                                    newWorker.first_name.length >= 30 ||
                                    newWorker.last_name.length === 0 ||
                                    newWorker.last_name.length >= 30 ||
                                    newWorker.main_doctor_id === -1 ||
                                    newWorker.date_of_birth === '' ||
                                    (!validEmail && newWorker.email_field.length !== 0) ||
                                    (!validNumber && newWorker.phone_number.length !== 0) ||
                                    newWorker.password.length >= 128 ||
                                    newWorker.phone_number.length > 13 ||
                                    newWorker.email_field.length >= 40 ||
                                    newWorker.works_for_company.length >= 254"
                    >
                        Submit
                    </vs-button>
                </div>
            </div>
      </div>
    </div>
</template>

<script>
import DateUtils from "@/utils/dateUtils";
import HealthcareWorkersService from "@/services/healthcareWorkersService";
import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: "HealthcareWorkerAdd",

    data:() => ({
        newWorker: {
            'first_name': '',
            'last_name': '',
            'gender': 'O',
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
            'works_for_company': '',
            'password': '',
        },
    }),

    computed: {
        validEmail() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newWorker.email_field);
        },

        validNumber() {
          return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newWorker.phone_number);
        },
    },

    methods: {
        async createWorker() {
            let data = {
                first_name: this.newWorker.first_name,
                last_name: this.newWorker.last_name,
                gender: this.newWorker.gender,
                works_for_company: this.newWorker.works_for_company,
                date_of_birth: DateUtils.getDateForBackend(this.newWorker.date_of_birth),
                email: this.newWorker.email_field,
                phone_number: this.newWorker.phone_number,
                password: this.newWorker.password,
            };

            if(data.date_of_birth === '') {
                data.date_of_birth = null;
            }

            HealthcareWorkersService.create(data)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('New healthcare worker was added to the database.', this.$vs);
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
