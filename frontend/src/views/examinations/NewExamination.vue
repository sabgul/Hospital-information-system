<template>
  <div>
      <div class="main__content">
          <h1>
              Creating examination according to ticket related to health concern {{ examinationAboutTicket.concern.name }}
              of patient {{ examinationAboutTicket.concern.patient.name }}
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

              <div
                  v-for="(action, index) in chosenActions"
                  v-bind:key="index"
                  class="action__within__examination"
              >
                <div>
                    <span><b>{{ action.name }}</b> <br> ({{getPricing(action.is_action_paid)}})</span>
                </div>

                <div class="buttons__action">
                    <div style="display: inline-block">
                       <vs-button
                          icon
                          danger
                          @click="deleteAction(index)"
                        >
                            <box-icon name='trash' style="fill: #fff"/>
                        </vs-button>
                    </div>

                  <div style="display: inline-block" v-if="action.is_action_paid">
                       <vs-button
                            icon
                            border
                            color="rgb(255,255,255)"
                            @click="overpayQuery(action.name)"
                        >
                            <box-icon name='dollar-circle' style="fill: #fff"/>
                            Ask Insurance company to overpay
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
          <h3>Attached Doctor report</h3>

          <br>

          <h5>Author: <b>TODO...current user</b></h5>
          <h5>About concern: <b>{{ examinationAboutTicket.concern.name }}</b></h5>
          <h5>Based on ticket number <b>{{ examinationAboutTicket.id }}</b></h5>

          <br>

          <textarea
              v-model="commentary"
              placeholder="Add commentary about this report."
          />
      </div>

      <div class="main__content">
          <vs-button success>
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
import ExaminationRequestsService from "@/services/examinationRequestsService";
import ExaminationActionsService from "@/services/examinationActionsService";
import TransactionRequestsService from "@/services/transactionRequestsService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: "NewExamination",

    props: {
        id: String,
    },

    data:() => ({
        examinationAboutTicket: {},
        examinationDate: '',

        activeActionAdd: false,
        actionToAdd: '',

        commentary: '',

        chosenActions: [],
        availableActions: [],
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

        this.examinationDate = year + '-' + month + '-' + day
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
        }
    }
}
</script>

<style scoped>
    .actions, .button, .input {
      margin-top: 2em;
    }

    .popup__center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        padding-bottom: 4em;
        width: 40%;
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

    .popup__right {
        position: absolute;
        right: 1em;
        bottom: 1em;
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

    textarea {
      border-radius: 12px;
      width: 60%;
    }
</style>