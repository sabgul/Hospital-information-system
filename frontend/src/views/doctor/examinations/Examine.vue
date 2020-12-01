<template>
  <div>
    <div class="main__content">
      <h1>
        Creating examination for health concern {{ aboutConcern.name }}
        of patient {{ aboutConcern.patient.user.first_name }} {{ aboutConcern.patient.user.last_name }}
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

      <h5>Brief description of the examination</h5>

      <textarea
          v-model="examinationDescription"
          placeholder="Briefly describe this examination.."
      />

      <div class="actions">
        <h5>
          Medical actions made during this examination:
        </h5>

        <span v-if="chosenActions.length === 0">
                    No actions selected
                </span>

        <div
            v-for="(action, index) in chosenActions"
            v-bind:key="index"
            class="action__within__examination"
        >
          <div>
            <span><b>{{ action.actionData.name }}</b> <br> ({{ getPricing(action.actionData.is_action_paid) }})</span>
          </div>

          <div class="buttons__action">
            <div
                class="overpay__switch"
                v-if="action.actionData.is_action_paid"
            >
              <vs-switch
                  v-model="action.cover"
                  success
                  style="bottom: 7px;"
              >
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
          <span style="margin-left: 1em">
                        Add new action
                    </span>
        </vs-button>

        <br>

        <br>
      </div>
    </div>

    <div class="main__content">
      <h3>Attach the Doctor's report</h3>

      <br>

      <h5>Author: <b>{{ user.first_name }} {{ user.last_name }}</b></h5>
      <h5>Regarding the concern: <b>{{ aboutConcern.name }}</b></h5>

      <br>

      <h6>Text of the report</h6>

      <textarea
          v-model="reportDescription"
          placeholder="Type the content of report here.."
      />

      <br>
      <br>

      <h6>Add image to report</h6>

      <div class="upload__wrapper">
        <button class="upload__btn">
            Choose an image
        </button>

        <input
            type="file"
            id="file"
            ref="file"
            accept="image/*"
            v-on:change="handleFileUpload()"
        />

        <span id="file__chosen">{{ fileName ? fileName : 'No file Chosen' }}</span>
      </div>
    </div>

    <div class="main__content">
      <vs-checkbox
          v-model="markConcernEnded"
          class="ticket__checkbox"
      >
        Mark health problem as resolved
      </vs-checkbox>

      <vs-button
          success
          @click="saveExamination()"
      >
        Save
      </vs-button>
    </div>

    <vs-dialog
        width="500px"
        v-model="activeActionAdd"
    >
      <template #header>
        <h5 class="popup__headline">
          Select actions performed during the examination
        </h5>
      </template>

      <vs-select
          v-model="actionToAdd"
          class="popup__center"
          label="Actions"
          color="primary"
          style="width: 300px !important;"
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
import {mapState} from "vuex";

export default {
  name: "Examine",

  computed: {
    ...mapState([
      'user',
    ])
  },

  props: {
    id: String,
  },

  data: () => ({
    aboutConcern: {},

    examinationDate: '',

    activeActionAdd: false,
    actionToAdd: '',

    examinationDescription: '',
    reportDescription: '',

    markConcernEnded: false,

    chosenActions: [],
    availableActions: [],

    askToCover: true,     // if false, patient pays it on their own

    file: '',
    fileName: '',
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

    const date = new Date();
    let day = date.getDate();
    let month = date.getMonth();
    month += 1;
    const year = date.getFullYear();

    this.examinationDate = year + '-' + month + '-' + day;
  },

  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
      this.fileName = this.$refs.file.files[0].name;
    },

    addAction() {
      this.activeActionAdd = true;
    },

    async addActionFinal() {
      ExaminationActionsService.get(this.actionToAdd)
          .then(response => {
            this.chosenActions.push({actionData: response.data, cover: true});
            this.activeActionAdd = false;
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
        concern: this.aboutConcern.id,
        request_based_on: null,
        actions: this.chosenActions.map(action => action.actionData.name),
        description: this.examinationDescription,
      }

      ExaminationsService.create(newExamination)
          .then(response => {
            NotificationsUtils.successPopup('Examination created.', this.$vs);

            let idOfNewExamination = response.data.id;

            let formData = new FormData();
            if(this.file) {
              formData.append('photo', this.file, this.file.name);
            }
            formData.append('created_by', this.user.id);
            formData.append('about_concern', this.aboutConcern.id);
            formData.append('description', this.reportDescription);
            formData.append('during_examination', idOfNewExamination);

            DoctorsReportsService.create(formData)
                .then(response => {
                  console.log(response);
                })
                .catch(e => {
                  NotificationsUtils.failPopup(e, this.$vs);
                });

            this.chosenActions.forEach(action => {
              if (action.cover) {
                const newRequest = {
                  examination_action: action.actionData.name,
                  request_state: 'UD',
                  related_to_patient: this.aboutConcern.patient.user.id,
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

      const newConcern = {
        name: this.aboutConcern.name,
        description: this.aboutConcern.description,
        state: this.markConcernEnded ? 'ED' : 'ON',
        patient: this.aboutConcern.patient.user.id,
        doctor: this.aboutConcern.doctor.user.id
      }

      HealthConcernsService.update(this.aboutConcern.id, newConcern)
          .then(response => {
            console.log(response);
          })
          .catch(e => {
            NotificationsUtils.failPopup(e, this.$vs);
          });

      await this.$router.go(-1);
    },
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
  justify-content: space-between;
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

.ticket__checkbox {
  float: left;
  margin-right: 2em;
}

textarea {
  border-radius: 12px;
  width: 60%;
}

.upload__wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.upload__btn {
  border: 2px solid gray;
  color: gray;
  background-color: white;
  padding: 8px 20px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: bold;
}

.upload__wrapper input[type=file] {
  font-size: 100px;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
}

#file__chosen {
  margin-left: 0.5em;
}
</style>
