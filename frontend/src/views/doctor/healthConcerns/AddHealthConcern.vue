<template>
    <div class="main__content">
        <h1>
          Add new health concern
        </h1>

        <p>
            If you were contacted with your patient who told you about his new health concern, <br>
            add the information here. <br>
            <b>If its a new patient, create an account for him first <span>here</span>!</b>
        </p>

        <br>

      <div class="wrapper">
        <div class="left__row">
            <vs-input
              v-model="newConcern.name"
              label="Name of health concern"
              placeholder="Type name of health concern"
              class="input__items"
              primary
            >
              <template
                  #message-warn
                  v-if="newConcern.name.length === 0"
              >
                  Required
              </template>

              <template
                  #message-danger
                  v-if="newConcern.name.length > 250"
              >
                  Message too long!
              </template>
          </vs-input>

          <vs-select
              v-model="newConcern.patient"
              class="input__items"
              label="Patient"
              placeholder="Choose a patient"
              color="primary"
          >
              <template
                  #message-warn
                  v-if="newConcern.patient === -1"
              >
                  Required
              </template>

              <vs-option
                  v-for="patient in availablePatients"
                  :key="patient.id"
                  :label="patient.name"
                  :value="patient.id"
              >
                  {{ patient.name }}
              </vs-option>
          </vs-select>
        </div>

        <div class="right__row">
            <vs-input
                v-model="newConcern.description"
                label="Description"
                placeholder="Briefly describe given concern"
                class="input__items"
            >
              <template
                  #message-danger
                  v-if="newConcern.description.length > 2000"
              >
                  Message too long!
              </template>
            </vs-input>

            <vs-select
              v-model="newConcern.doctor"
              class="input__items"
              label="Doctor"
              placeholder="Choose a doctor"
              color="primary"
            >
              <template
                  #message-warn
                  v-if="newConcern.doctor === -1"
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
        </div>

        <div class="third__row">
            <vs-select
                v-model="newConcern.state"
                label="Concern state"
                color="primary"
            >
                <vs-option
                    value="WT"
                    label="Waiting for examination"
                >
                    Waiting for examination
                </vs-option>

                <vs-option
                    value="ON"
                    label="Ongoing"
                >
                    Ongoing
                </vs-option>

                <vs-option
                    value="TL"
                    label="Terminal"
                >
                    Terminal
                </vs-option>

                <vs-option
                    value="ED"
                    label="Ended"
                >
                    Ended
                </vs-option>
            </vs-select>
        </div>

        <vs-button
            @click="addNewExamination()"
            :disabled=" newConcern.name.length === 0 ||
                        newConcern.name.length > 250 ||
                        newConcern.doctor === -1 ||
                        newConcern.patient === -1 ||
                        newConcern.description.length > 2000"
            class="filter__submit"
        >
            Submit
        </vs-button>
      </div>
    </div>
</template>


<script>
import HealthConcernsService from "@/services/healthConcernsService";
import PatientsService from "@/services/patientsService";
import DoctorsService from "@/services/doctorsService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'AddHealthConcern',

    data:() => ({
        newConcern: {
          name: '',
          description: '',
          state: 'WT',
          patient: -1,
          doctor: -1, // TODO tu bude id current usera
        },
        availablePatients: [],
        availableDoctors: [],
    }),

    async created() {
        PatientsService.getAll()
            .then(response => {
            this.availablePatients = response.data;
            })
            .catch(e => {
            console.log(e);
            });

        DoctorsService.getAll()
            .then(response => {
            this.availableDoctors = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },

    methods: {
        async addNewExamination() {
            HealthConcernsService.create(this.newConcern)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Health concern added to database.', this.$vs);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
        }
    },
}
</script>

<style scoped>
    h1 {
        margin-top: 0.5em;
        margin-bottom: 1em;
    }

    .main__content {
        padding: 20px 20px 20px 25px;
        margin-top: 20px;
        margin-left: 25%;
        margin-right: 15%;
        background-color: #ffffff;
        box-shadow:
            0 1.3px 20.1px rgba(0, 0, 0, 0.003),
            0 4.2px 44.8px rgba(0, 0, 0, 0.003),
            0 19px 76px rgba(0, 0, 0, 0.06);
        border-radius: 10px;
    }

    .input__items {
        padding: 16px 0;
        margin-left: 6px;
    }

    .wrapper {
        display: flex;
        padding-top: 2em;
    }

    .left__row {
        width: 200px;
        margin-top: auto;
        margin-bottom: 1em;
    }

    .right__row {
        padding-left: 2em;
        flex-grow: 1;
        margin-top: auto;
        margin-bottom: 1em;
    }

    .third__row {
        padding-left: 0;
        flex-grow: 2;
        margin-top: auto;
        margin-bottom: 3em;
    }

    .filter__submit {
        margin-left: auto;
        order: 3;
        margin-top: 5em;
        margin-right: 1em;
        height: 4em;
        width: 8em;
    }

    .concern__description {
      height: 100px;
    }
</style>