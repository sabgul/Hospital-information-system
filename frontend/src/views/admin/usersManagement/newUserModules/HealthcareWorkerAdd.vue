<template>
    <div>
      <div class="main__content">
          <h1>
              Add new healthcare worker
          </h1>

          <p>
              Create new doctor in the database of doctors.<br>
              Some of the basic patient information are necessary to state, but doctor(or you) can manage his profile later.
          </p>

          <br>

          <div class="wrapper">
              <div class="first__row">
                  <vs-input
                      v-model="newWorker.name"
                      label="Name of worker"
                      placeholder="Type name"
                      class="input__items"
                      primary
                  >
                      <template
                          #message-warn
                          v-if="newWorker.name.length === 0"
                      >
                          Required
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
                      v-model="newWorker.works_for_company"
                      label="Works for company"
                      placeholder="Name of company"
                      class="input__items"
                  >
                      <template
                          v-if="newWorker.works_for_company.length >= 250"
                          #message-danger
                      >
                          Text too long
                      </template>
                  </vs-input>
              </div>

              <div class="third__row">
                    <vs-input
                        v-model="newWorker.email_field"
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
                            v-if="!validEmail && newWorker.email_field !== ''"
                            #message-danger
                        >
                            Invalid email
                        </template>

                        <template
                            #message-warn
                            v-if="newWorker.email_field.length === 0"
                        >
                            Required
                        </template>
                    </vs-input>

                    <vs-input
                        v-model="newWorker.phone_number"
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
                            v-if="!validNumber && newWorker.phone_number !== ''"
                            #message-danger
                        >
                            Invalid phone number
                        </template>
                    </vs-input>
              </div>

              <div class="submit__row">
                  <vs-button
                      @click="createWorker()"
                      :disabled=" newWorker.name.length === 0 ||
                                  newWorker.main_doctor_id === -1 ||
                                  newWorker.date_of_birth === '' ||
                                  (!validEmail && newWorker.email_field.length !== 0) ||
                                  (!validNumber && newWorker.phone_number.length !== 0)"
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
            'name': '',
            'gender': 'O',
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
            'works_for_company': '',
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
                name: this.newWorker.name,
                gender: this.newWorker.gender,
                works_for_company: this.newWorker.works_for_company,
                date_of_birth: DateUtils.getDateForBackend(this.newWorker.date_of_birth),
                email_field: this.newWorker.email_field,
                phone_number: this.newWorker.phone_number
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
</style>