<template>
    <div class="main__content">
        <h1>
          Create a new ticket for <b>{{ relatedConcern.name }}</b>
        </h1>

        <p>
            Create new examination request(ticket) for a health concern of your patient. <br>
            You can assign the ticket either to you or another doctor, usually some specialist.
        </p>

        <br>

      <div class="wrapper">
        <div class="left__row">
            <vs-select
              v-model="chosenDoctor"
              class="input__items"
              label="Assign a doctor for ticket"
              placeholder="Assign a doctor for ticket"
              color="primary"
            >
              <template
                  #message-warn
                  v-if="chosenDoctor === -1"
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

        <vs-button
            @click="addNewExamination()"
            :disabled=" chosenDoctor === -1"
            class="filter__submit"
        >
            Submit
        </vs-button>
      </div>
    </div>
</template>


<script>
import HealthConcernsService from "@/services/healthConcernsService";
import DoctorsService from "@/services/doctorsService";
import ExaminationRequestsService from "@/services/examinationRequestsService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'NewExaminationRequest',

    props: {
      id: String,
    },

    data:() => ({
        chosenDoctor: -1, // TODO tu bude id current usera

        relatedConcern: {},
        availableDoctors: [],
    }),

    async created() {
        DoctorsService.getAll()
            .then(response => {
            this.availableDoctors = response.data;
            })
            .catch(e => {
            console.log(e);
            });

        HealthConcernsService.get(this.id)
            .then(response => {
              this.relatedConcern = response.data;
            })
            .catch(e => {
              console.log(e);
            });
    },

    methods: {
        async addNewExamination() {
            const newTicket = {
              state: 'PD',
              concern: this.id,
              doctor: this.chosenDoctor,
              created_by: this.chosenDoctor, // TODO toto bude current user!!
            }

            ExaminationRequestsService.create(newTicket)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Examination request was successfully added into database.', this.$vs);
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