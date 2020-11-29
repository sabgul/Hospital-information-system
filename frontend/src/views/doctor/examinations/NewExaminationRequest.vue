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
            <div class="first__row">
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
                        :key="doctor.user.id"
                        :label="doctor.user.first_name"
                        :value="doctor.user.id"
                    >
                        {{ doctor.user.first_name }}
                    </vs-option>
              </vs-select>
            </div>

            <vs-button
                @click="addNewExamination()"
                :disabled=" chosenDoctor === -1"
                class="submit__row"
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

import NotificationsUtils from "@/utils/notificationsUtils"

import { mapState } from "vuex";

export default {
    name: 'NewExaminationRequest',

    props: {
      id: String,
    },

    computed: {
        ...mapState([
            'user',
        ])
    },

    data:() => ({
        chosenDoctor: -1,

        relatedConcern: {},
        availableDoctors: [],
    }),

    async created() {
        DoctorsService.getAll()
            .then(response => {
                this.availableDoctors = response.data;
            })

        HealthConcernsService.get(this.id)
            .then(response => {
                this.relatedConcern = response.data;
            })
    },

    methods: {
        async addNewExamination() {
            const newTicket = {
                state: 'PD',
                concern: this.id,
                assigned_to: this.chosenDoctor,
                created_by: this.user.id,
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
</style>
