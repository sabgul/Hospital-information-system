<template>
  <div>
      <div class="main__content">
          <h1>
              Creating examination according to ticket related to health concern {{ examinationAboutTicket.concern.name }}
              of patient {{ examinationAboutTicket.concern.patient.user.first_name }} {{ examinationAboutTicket.concern.patient.user.last_name }}
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

          <h5>Description</h5>

          <textarea
              v-model="examinationDescription"
              placeholder="Briefly describe examination.."
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
                    <span><b>{{ action.actionData.name }}</b> <br> ({{getPricing(action.actionData.is_action_paid)}})</span>
                </div>

                <div class="buttons__action">
                    <div class="overpay__switch" v-if="action.is_action_paid">
                       <vs-switch v-model="askToCover" success style="bottom: 7px;">
                          <template #off>
                          Paid by patient
                          </template>

                          <template #on>
                          Paid by insurance company
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

          <h5>Author: <b>{{ currentUserName }}</b></h5>
          <h5>About concern: <b>{{ examinationAboutTicket.concern.name }}</b></h5>
          <h5>Based on ticket number <b>{{ examinationAboutTicket.id }}</b></h5>

          <br>

          <h6>Report text</h6>
          <textarea
              v-model="reportDescription"
              placeholder="Put text of report here.."
          />
      </div>

      <div class="main__content">
          <vs-checkbox v-model="markTicketResolved" class="ticket__checkbox">
            Mark concern as ended
          </vs-checkbox>

          <vs-checkbox v-model="markConcernEnded" class="ticket__checkbox">
            Mark ticket as resolved
          </vs-checkbox>

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
                  Select actions performed during examination
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
import ExaminationRequestsService from "@/services/examinationRequestsService";
import ExaminationActionsService from "@/services/examinationActionsService";
import TransactionRequestsService from "@/services/transactionRequestsService";
import ExaminationsService from "@/services/examinationsService";
import HealthConcernsService from "@/services/healthConcernsService";
import DoctorsReportsService from "@/services/doctorsReportsService";

import NotificationsUtils from "@/utils/notificationsUtils";
import DateUtils from "@/utils/dateUtils";
import {mapState} from "vuex";

export default {
    name: "NewExamination",

    props: {
        id: String,
    },

    computed: {
        ...mapState([
            'user',
        ]),

        currentUserName() {
          return this.user.first_name + ' ' + this.user.last_name;
        }
    },

    data:() => ({
        examinationAboutTicket: {},
        examinationDate: '',

        activeActionAdd: false,
        actionToAdd: '',

        examinationDescription: '',
        reportDescription: '',

        chosenActions: [],
        availableActions: [],

        markTicketResolved: true,
        markConcernEnded: false,

        askToCover: true,     // if false, patient pays it on his own
    }),

    async created() {
        ExaminationRequestsService.get(this.id)
            .then(response => {
            this.examinationAboutTicket = response.data;
            })
            .catch(e => {
            console.log(e);
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

        async addActionFinal() {
            ExaminationActionsService.get(this.actionToAdd)
                .then(response => {
                     this.chosenActions.push({ actionData: response.data, cover: true });
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

        async saveExamination() {
          // adding new examination into DB
            const newExamination = {
                date_of_examination: DateUtils.getDateForBackend(this.examinationDate),
                examinating_doctor: this.user.id,
                request_based_on: this.examinationAboutTicket.id,
                concern: this.examinationAboutTicket.concern.id,
                actions: this.chosenActions.map(action => action.actionData.name),
                description: this.examinationDescription,
            }

            ExaminationsService.create(newExamination)
            .then(response => {
                NotificationsUtils.successPopup('Examination created.', this.$vs);

                let idOfNewExamination = response.data.id;
                const newReport = {
                    created_by: this.user.id,
                    about_concern: this.examinationAboutTicket.concern.id,
                    description: this.reportDescription,
                    during_examination: idOfNewExamination,
                    // file: formData,
                }

                DoctorsReportsService.create(newReport)
                .then(response => {
                    console.log(response);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });

                this.chosenActions.forEach(action => {
                    if(action.cover) {
                        const newRequest = {
                            examination_action: action.actionData.name,
                            request_state: 'UD',
                            related_to_patient: this.examinationAboutTicket.concern.patient.user.id,
                            during_examination: idOfNewExamination,
                            transaction_approver: action.actionData.action_manager.user.id,
                        }

                        TransactionRequestsService.create(newRequest)
                        .then(response => {
                              console.log(response);
                        })
                        .catch(e => {
                            NotificationsUtils.failPopup(e, this.$vs);
                        });
                    }
                })
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });

            // Ticket is set to be resolved
            if(this.markTicketResolved) {
                const newTicketData = {
                    concern: this.examinationAboutTicket.concern.id,
                    created_by: this.examinationAboutTicket.created_by.user.id,
                    assigned_to: this.user.id,
                    state: 'RD'
                };

                ExaminationRequestsService.update(this.examinationAboutTicket.id, newTicketData)
                .then(response => {
                    console.log(response);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
            }

            const newConcern = {
                name: this.examinationAboutTicket.concern.name,
                description: this.examinationAboutTicket.concern.description,
                state: this.markConcernEnded ? 'ED' : 'ON',
                patient: this.examinationAboutTicket.concern.patient.user.id,
                doctor: this.examinationAboutTicket.concern.doctor.user.id
            }

            HealthConcernsService.update(this.examinationAboutTicket.concern.id, newConcern)
                .then(response => {
                    console.log(response);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });

            await this.$router.go(-1);
        }
    }
}
</script>

<style scoped>
    .actions, .button, .input {
      margin-top: 2em;
    }

    .popup__headline {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 0.5em;
        width: 80%;
        text-align: center;
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

    .ticket__checkbox {
      float: left;
      margin-right: 2em;
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
