<template>
    <div>
        <div class="main__content">
            <h1>
              Assigned tickets
            </h1>

            <p>
                You can see all the tickets assigned to you below. Ticket indicates a request for a particular examination issued by another doctor. <br>
                Please review any new tickets and perform all the necessary actions. The record of the examination based on particular ticket can be added <br>
                by clicking on <b>Examination based on this ticket</b>. Any necessary reports and detailed information of the examination can be added there.
            </p>
        </div>

        <div class="main__content">
            <h4>
                Filter results
            </h4>

          <form action="#" v-on:submit.prevent="getFiltered">
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
                            Cancelled
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
                    >
                        Apply filter
                    </vs-button>
                </div>
            </div>
          </form>
        </div>

        <div
            class="main__content"
            v-if="tickets.length === 0"
            style="text-align: center;"
        >
            <h4>No tickets were assigned to you!</h4>
            <img src="../../../assets/relax.svg" alt="">
        </div>

        <div
            v-else
            class="main__content"
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
                    <span @click="redirectToProfile(ticket.concern.patient.user.id, 'patient')" class="redirect__profile">{{ ticket.concern.patient.user.first_name }} {{ ticket.concern.patient.user.last_name }}</span>
                </h5>

                <h5>
                    Concern:
                    <span @click="showConcernDetail(ticket.concern.id)" class="redirect__profile">{{ ticket.concern.name }}</span>
                </h5>

                <h5>
                    Ticket created by:
                    <span @click="redirectToProfile(ticket.created_by.user.id, 'doctor')" class="redirect__profile">{{ ticket.created_by.user.first_name }} {{ ticket.created_by.user.first_name }}</span>
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
                        Examination based on this ticket
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
import StateUtils from "@/utils/stateUtils";

import { mapState } from "vuex";

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

    computed: {
        ...mapState([
            'user',
            'userRole',
        ])
    },

    async created() {
        if(this.userRole === 'admin') {
            ExaminationRequestsService.getAll()
            .then(response => {
                this.tickets = response.data;
            })
        } else {
            ExaminationRequestsService.getAllByCurrentUser(this.user.id)
            .then(response => {
                this.tickets = response.data;
            })
        }

    },

    methods: {
        getDate(rawDate) {
            return DateUtils.getDateForFrontend(rawDate);
        },

        getState(rawState) {
            return StateUtils.getTicketState(rawState);
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
                assigned_to: ticket.assigned_to.user.id,
                created_by: ticket.created_by.user.id
            }

            ExaminationRequestsService.update(ticketId, newTicket)
            .then(response => {
                console.log(response);

                ExaminationRequestsService.getFiltered(this.filter)
                .then(response => {
                    this.tickets = response.data;
                })
            })
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
        },

        async clearFilter() {
            this.filter.state = '';

            ExaminationRequestsService.getAll()
            .then(response => {
                this.tickets = response.data;
            })
        },

        async getFiltered() {
            ExaminationRequestsService.getFiltered(this.filter)
            .then(response => {
                this.tickets = response.data;
            })
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

    img {
        display: block;
        margin: 2em auto;
        width: 60%;
    }
</style>
