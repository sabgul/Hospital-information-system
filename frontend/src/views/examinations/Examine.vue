<template>
    <div>
        <div class="main__content">
            <h1>
              Creating examination for health concern {{ aboutConcern.name }}
              of patient {{ aboutConcern.patient.name }}
          </h1>
        </div>

        <div class="main__content">
            <h3>Date of examination & actions</h3>

            <br>

            <vs-input
                label="Date of examination"
                v-model="examinationDate"
                type="date"
                class="input"
            />

            <br>

            <div class="actions">
                <h5>Examination actions made during this examination: </h5>
                <span v-if="chosenActions.length === 0">No actions selected</span>
                <div
                    v-for="(action, index) in chosenActions"
                    v-bind:key="index"
                    class="action__within__examination"
                >
                  <div>
                      <span><b>{{ action.name }}</b> <br> ({{getPricing(action.is_action_paid)}})</span>
                  </div>

                  <div class="buttons__action">
                      <div class="overpay__switch" v-if="action.is_action_paid">
                         <vs-switch v-model="askToCover" success style="bottom: 7px;">
                              <template #off>
                                  Patient is self-payer
                              </template>

                              <template #on>
                                  Ask insurance company to overpay
                              </template>
                         </vs-switch>
                      </div>

                      <div style="display: inline-block">
                         <vs-button
                            icon
                            danger
                            @click="deleteAction(index)"
                         >
                            <box-icon name='trash' style="fill: #fff"/>
                         </vs-button>
                      </div>
                  </div>
                </div>

                <vs-button
                    gradient
                    icon
                    class="button"
                    @click="addAction()"
                >
                    <box-icon name='message-square-add' type='solid' style="fill: #fff"/>
                    <span style="margin-left: 1em">Add new action</span>
                </vs-button>

              <br>
              <br>


            </div>
        </div>

        <div class="main__content">
            <h3>Attach Doctor report</h3>

            <br>

            <h5>Author: <b>TODO...current user</b></h5>
            <h5>About concern: <b>{{ aboutConcern.name }}</b></h5>

            <br>

            <h6>Description</h6>
            <textarea
                v-model="description"
                placeholder="Describe briefly this report.."
            />
        </div>

        <div class="main__content">
            <vs-button success @click="saveExamination()">
                Save
            </vs-button>
        </div>

        <vs-dialog
            width="500px"
            v-model="activeActionAdd"
        >
            <template #header>
                <h5 class="popup__headline">
                    Choose a new action that was made during this examination
                </h5>
            </template>

            <vs-select
                v-model="actionToAdd"
                class="popup__center"
                label="Actions"
                color="primary"
                >
                    <vs-option
                        v-for="action in availableActions"
                        :key="action.id"
                        :label="`[${getPricing(action.is_action_paid)}] ${action.name}`"
                        :value="action.name"
                    >
                        [{{ getPricing(action.is_action_paid) }}] {{ action.name }}
                    </vs-option>
            </vs-select>

            <template #footer>
                <div class="popup__right">
                    <vs-button
                        success
                        :disabled="actionToAdd.length === 0"
                        @click="addActionFinal()"
                    >
                        Add
                    </vs-button>
                </div>
            </template>
        </vs-dialog>
    </div>
</template>

<script>
import HealthConcernsService from "@/services/healthConcernsService";
import NotificationsUtils from "@/utils/notificationsUtils";
import ExaminationActionsService from "@/services/examinationActionsService";
import TransactionRequestsService from "@/services/transactionRequestsService";
import DateUtils from "@/utils/dateUtils";
import ExaminationsService from "@/services/examinationsService";
import DoctorsReportsService from "@/services/doctorsReportsService";

export default {
    name: "Examine",

    props: {
        id: String,
    },

    data:() => ({
        aboutConcern: {},

        examinationDate: '',

        activeActionAdd: false,
        actionToAdd: '',

        description: '',

        chosenActions: [],
        availableActions: [],

        askToCover: true,     // if false, patient pays it on his own
    }),

    async created() {
        HealthConcernsService.get(this.id)
            .then(response => {
                this.aboutConcern = response.data;
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });

        ExaminationActionsService.getAll()
            .then(response => {
            this.availableActions = response.data;
            })
            .catch(e => {
            console.log(e);
            });

        const date = new Date();
        let day = date.getDate();
        let month = date.getMonth();
        month += 1;
        const year = date.getFullYear();

        this.examinationDate = year + '-' + month + '-' + day;
    },

    methods: {
        addAction() {
            this.activeActionAdd = true;
        },

        addActionFinal() {
            ExaminationActionsService.get(this.actionToAdd)
                .then(response => {
                    this.chosenActions.push(response.data);
                    NotificationsUtils.successPopup('Action successfully added into examination.', this.$vs);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
        },

        getPricing(value) {
            return value ? 'PAID' : 'FREE';
        },

        deleteAction(index) {
          this.chosenActions.splice(index, 1);
        },

        overpayQuery(name) {
            const newRequest = {
                examination: 1,
                examination_action: name,
                request_state: 'UD'
            }

            TransactionRequestsService.create(newRequest)
                .then(response => {
                      console.log(response);
                      NotificationsUtils.successPopup('Request to cover this action was sent to insurance company.', this.$vs);
                  })
                  .catch(e => {
                      NotificationsUtils.failPopup(e, this.$vs);
                  });
        },

        async saveExamination() {
          // adding new examination into DB
          const newExamination = {
              date_of_examination: DateUtils.getDateForBackend(this.examinationDate),
              examinating_doctor: this.aboutConcern.doctor.id,    // TODO current user
              concern: this.aboutConcern.id,
              request_based_on: null,
              actions: this.chosenActions.map(action => action.name),
          }

          ExaminationsService.create(newExamination)
              .then(response => {
                  console.log(response);
                  NotificationsUtils.successPopup('Examination created.', this.$vs);
              })
              .catch(e => {
                  NotificationsUtils.failPopup(e, this.$vs);
              });

          const newReport = {
            created_by: this.aboutConcern.doctor.id, // TODO current user
            about_concern: this.aboutConcern.id,
            description: this.description,
          }

          DoctorsReportsService.create(newReport)
              .then(response => {
                  console.log(response);
              })
              .catch(e => {
                  NotificationsUtils.failPopup(e, this.$vs);
              });

          // state of concern is set to be Ongoing
          const newConcern = {
            name: this.aboutConcern.name,
            description: this.aboutConcern.description,
            state: 'ON',
            patient: this.aboutConcern.patient.id,
            doctor: this.aboutConcern.doctor.id
          }

          HealthConcernsService.update(this.aboutConcern.id, newConcern)
              .then(response => {
                  console.log(response);
              })
              .catch(e => {
                  NotificationsUtils.failPopup(e, this.$vs);
              });
        }
    }
}
</script>

<style scoped>
    .actions, .button, .input {
        margin-top: 2em;
    }

    .action__within__examination {
        background-color: #195bff;
        opacity: 0.95;
        color: white;
        padding: 1em 2em;
        border-radius: 10px;
        margin-bottom: 0.5em;
        display: flex;
        justify-content:space-between;
    }

    .buttons__action {
        right: 1em;
        bottom: 1em;
        display: inline-block;
    }

    .overpay__switch {
        display: inline-block;
        width: 15em;
        padding-right: 1em;
    }

    textarea {
        border-radius: 12px;
        width: 60%;
    }
</style>