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

        <div class="main__content">
            <h4>
                Filter results
            </h4>

            <div class="wrapper">
                <div class="first__row">
                    <vs-select
                        v-model="filter.state"
                        label="State"
                        color="primary"
                    >
                        <vs-option
                            value="PD"
                            label="Pending"
                        >
                            Pending
                        </vs-option>

                        <vs-option
                            value="CD"
                            label="Canceled"
                        >
                            Canceled
                        </vs-option>

                        <vs-option
                            value="RD"
                            label="Resolved"
                        >
                            Resolved
                        </vs-option>
                    </vs-select>
                </div>

                <div class="submit__row" style="padding-bottom: 6em; margin-top: 0;">
                    <vs-button
                        style="padding: 3px 16px;"
                        border
                        @click="clearFilter()"
                    >
                        Clear filter
                    </vs-button>

                    <vs-button
                        style="padding: 3px 42px;"
                        @click="getFiltered()"
                    >
                        Filter
                    </vs-button>
                </div>
            </div>
        </div>

        <div class="main__content"
            v-for="ticket in tickets"
            :key="ticket.id"
        >
            <div class="concern__content">
                <h5>
                    Created on: {{ getDate(ticket.created_timestamp) }}
                </h5>

                <h5>
                  State: <b>{{ getState(ticket.state) }}</b>
                </h5>

                <h5>
                    Patient:
                  <span @click="redirectToProfile(ticket.concern.patient.id, 'patient')" class="redirect__profile">{{ ticket.concern.patient.name }}</span>
                </h5>

                <h5>
                    Concern:
                <span @click="showConcernDetail(ticket.concern.id)" class="redirect__profile">{{ ticket.concern.name }}</span>
                </h5>

                <h5>
                    Ticket created by:
                    <span @click="redirectToProfile(ticket.created_by.id, 'doctor')" class="redirect__profile">{{ ticket.created_by.name }}</span>
                </h5>

                <div class="button__area">
                    <vs-button
                        v-if="ticket.state === 'PD'"
                        warn
                        border
                        class="button__top"
                        @click="cancelRequest(ticket, ticket.id)"
                    >
                        Cancel ticket
                    </vs-button>

                    <vs-button
                        v-if="ticket.state === 'PD'"
                        @click="examine(ticket.id)"
                    >
                        Examine based on this ticket
                    </vs-button>

                    <vs-button
                        v-if="ticket.state !== 'PD'"
                        warn
                        @click="removeTicket(ticket.id)"
                    >
                        Remove old ticket
                    </vs-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ExaminationRequestsService from "@/services/examinationRequestsService";

import DateUtils from "@/utils/dateUtils";

export default {
    name: "ManageAssignedTickets",

    data:() => ({
        tickets: [],
        patients: [],
        doctors: [],

        filter: {
          patient: -1,
          doctor: -1,
          state: '',
        }
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
            return DateUtils.getDateForFrontend(rawDate);
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

        redirectToProfile(userId, role) {
        this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }});
        },

        showConcernDetail(concernId) {
            this.$router.push({ name: 'healthConcernDetail', params: {id: concernId }})
        },

        async cancelRequest(ticket, ticketId) {
            const newTicket = {
              id: ticketId,
              created_timestamp: ticket.created_timestamp,
              state: 'CD',
              concern: ticket.concern.id,
              created_by: ticket.created_by.id
            }

            ExaminationRequestsService.update(ticketId, newTicket)
                .then(response => {
                  console.log(response);

                  ExaminationRequestsService.getFiltered(this.filter)
                      .then(response => {
                      this.tickets = response.data;
                      })
                      .catch(e => {
                      console.log(e);
                      });
                })
                .catch(e => {
                console.log(e);
                });
        },

        async removeTicket(ticketId) {
          ExaminationRequestsService.delete(ticketId)
                .then(response => {
                  console.log(response);

                  ExaminationRequestsService.getFiltered(this.filter)
                      .then(response => {
                      this.tickets = response.data;
                      })
                      .catch(e => {
                      console.log(e);
                      });
                })
                .catch(e => {
                console.log(e);
                });
        },

        async clearFilter() {
            this.filter.state = '';

            ExaminationRequestsService.getAll()
                .then(response => {
                this.tickets = response.data;
                })
                .catch(e => {
                console.log(e);
                });
        },

        async getFiltered() {
            ExaminationRequestsService.getFiltered(this.filter)
                .then(response => {
                this.tickets = response.data;
                })
                .catch(e => {
                console.log(e);
                });
        },

        examine(ticketId) {
            this.$router.push({ name: 'newExamination', params: { id: ticketId}});
        }
    },
}

</script>

<style scoped>
    .button__area {
      margin-top: 2em;
    }

    .button__top {
      margin-bottom: 0.5em;
    }

    .redirect__profile:hover {
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }

</style>