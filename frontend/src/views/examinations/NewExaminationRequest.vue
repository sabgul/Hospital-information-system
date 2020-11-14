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
        showSuccessMessage() {
          const position = 'top-right';
          const progress = 'auto';
          const duration = '6000';
          const color = 'success';

          const noti = this.$vs.notification({
                duration,
                progress,
                color,
                position,
                title: 'Hooray!🎉',
                text: 'New ticket was successfully created.'
            });
            console.log(noti);
        },

        showErrorMessage(e) {
            const position = 'top-right';
            const progress = 'auto';
            const duration = '6000';
            const color = 'danger';

            const noti = this.$vs.notification({
                  duration,
                  progress,
                  color,
                  position,
                  title: 'Whoops!😓: ' + e.message,
                  text: 'Something went wrong. Try again later of contact support.',
              });
              console.log(noti);
        },

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
                    this.showSuccessMessage();
                })
                .catch(e => {
                    this.showErrorMessage(e);
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