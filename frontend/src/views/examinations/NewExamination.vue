<template>
  <div>
      <div class="main__content">
          <h1>
              Creating examination according to ticket related to health concern {{ examinationAboutTicket.concern.name }}
              of patient {{ examinationAboutTicket.concern.patient.name }}
          </h1>
      </div>

      <div class="main__content">
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
                  v-for="action in chosenActions"
                  v-bind:key="action.id"
              >
                  <span>{{ action.name }}</span>
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
          </div>
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

        successPopup() {
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
              text: 'Examination action added into list of actions for given examination.'
          });
          console.log(noti);
        },

        failPopup(e) {
          const position = 'top-right';
          const progress = 'auto';
          const duration = '6000';
          var color = 'danger';

          const noti = this.$vs.notification({
              duration,
              progress,
              color,
              position,
              title: 'Whoops!😓: ' + e.message,
              text: 'Try again later or contact support.'
          });
          console.log(noti);
        },

        addActionFinal() {
            ExaminationActionsService.get(this.actionToAdd)
                .then(response => {
                    this.chosenActions.push(response.data);
                    this.successPopup();
                })
                .catch(e => {
                    this.failPopup(e);
                });
        },

        getPricing(value) {
            return value ? 'PAID' : 'FREE';
        }
    }
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
</style>