<template>
    <div>
        <div class="main__content">
            <h1>
              Tickets assigned to me
            </h1>

            <p>
                You can see all tickets assigned to you right here..
            </p>
        </div>

        <div class="main__content"
            v-for="ticket in tickets"
            :key="ticket.id"
        >
            <div class="concern__content">
                <h4>
                    Created on: {{ getDate(ticket.created_timestamp) }}
                </h4>

                <h4>
                    State: {{ getState(ticket.state) }}
                </h4>

                <h4>
                    Patient: {{ ticket.concern.patient.name }}
                </h4>

                <h4>
                    Concern: {{ ticket.concern.name }}
                </h4>

                <h4>
                  Ticket created by doctor <b>{{ ticket.created_by.name }}</b>
                </h4>

                <div class="button__area">
                    <vs-button warn border>
                        Cancel ticket
                    </vs-button>

                    <vs-button @click="examine(ticket.id)">
                        Examine based on this ticket
                    </vs-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ExaminationRequestsService from "@/services/examinationRequestsService";

export default {
    name: "ManageAssignedTickets",

    data:() => ({
        tickets: [],
    }),

    async created() {
        ExaminationRequestsService.getAll()
            .then(response => {
            this.tickets = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },

    methods: {
        getDate(rawDate) {
            const year = rawDate.slice(0, 4);
            const month = rawDate.slice(5, 7);
            const day = rawDate.slice(8, 10);
            const time = rawDate.slice(11, 19);

            return day + '. ' + month + '. ' + year + ' ' + time;
        },

        getState(rawState) {
            if(rawState === 'PD') {
              return 'Ticket is waiting. Examine your patient!'
            }

            if(rawState === 'CD') {
              return 'Examination request was canceled.'
            }

            if(rawState === 'RD') {
              return 'Ticket already resolved.'
            }
        },

        examine(ticketId) {
            this.$router.push({ name: 'newExamination', params: { id: ticketId}});
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

    .button__area {
      margin-top: 2em;
    }
</style>