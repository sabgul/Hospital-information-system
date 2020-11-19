<template>
  <div>
      <div class="main__content">
          <h1>
            Detail of health concern <b>{{ concern.name }}</b>
          </h1>

          <div class="info__basic wrapper">
              <div class="first__row" style="width: 500px;">
                  <h5><b>Patient</b>: {{ concern.patient.name }}</h5>
                  <h5><b>Doctor</b>: {{ concern.doctor.name }}</h5>
                  <h5><b>State</b>: {{ getState(concern.state) }}</h5>
                  <h5><b>Description</b>: {{ concern.description }}</h5>
              </div>

              <div class="submit__row" style="margin-top: 1em; margin-right: 4em;">
                  <vs-button border @click="redirectToExamination(concern.id)" style="width: 170px;">
                      Examine
                  </vs-button>

                  <vs-button class="buttons" @click="redirectToNewRequest(concern.id)" style="width: 170px;">
                      New examination request
                  </vs-button>

                  <vs-button
                      danger
                      class="buttons"
                      @click="reassign(concern)"
                      style="width: 170px;"
                  >
                      Assign to another doctor
                  </vs-button>
              </div>
          </div>
      </div>

      <div class="main__content">
          <h5>
              Passed examinations
          </h5>

          <vs-card-group>
            <vs-card v-for="examination in examinations" v-bind:key="examination.id"  @click="showExaminationDialog(examination)">
                <template #title>
                    <h3>{{ getDate(examination.date_of_examination) }}</h3>
                </template>

                <template #img>
                  <img src="../assets/examination.svg" alt="" width="200px;height=150px;">
                </template>

                <template #text>
                    <p>
                    </p>
                </template>

                <template #interactions>
                    <vs-button class="btn-chat" shadow primary icon @click="showExaminationDialog(examination)">
                        <box-icon style="fill: #000; margin-right: 0.5em;" name='message-square-detail'/>
                        <span class="span">
                            Show actions and description
                        </span>
                    </vs-button>
                </template>
            </vs-card>

            <vs-card @click="redirectToExamination(id)">
                <template #title>
                    <h3>Examine</h3>
                </template>

                <template #img>
                  <img src="../assets/new-examination-request.svg" alt="" style="width:200px;height:150px;">
                </template>

               <template #text>
                    <p>
                        Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                    </p>
                </template>
            </vs-card>
        </vs-card-group>
      </div>

      <div class="main__content">
          <h5>
              Doctor reports related to this health concern
          </h5>

          <vs-card-group>
            <vs-card v-for="report in reports" v-bind:key="report.id" @click="showReportDialog(report)">
                <template #img>
                  <img src="../assets/missing-image.svg" alt="">
                </template>

                <template #text>
                    <p style="margin-top: 1em;">
                      {{ report.description }}
                    </p>
                </template>

                <template #interactions>
                    <vs-button class="btn-chat" shadow primary icon @click="showReportDialog(report)">
                        <box-icon style="fill: #000; margin-right: 0.5em;" name='message-square-detail'/>
                        <span class="span">
                            Show attached files
                        </span>
                    </vs-button>
                </template>
            </vs-card>
        </vs-card-group>
      </div>
    
      <vs-dialog
          width="500px"
          v-model="activeAssign"
      >
          <template #header>
              <h5>
                  Select new manager of <b>{{ toReassign.name }}</b>
              </h5>
          </template>

          <vs-select
              v-model="newDoc"
              class="popup__center"
              label="Doctor"
              placeholder="Choose a doctor"
              color="primary"
              >
                  <vs-option
                      v-for="doctor in availableDoctors"
                      :key="doctor.id"
                      :label="doctor.name"
                      :value="doctor.id"
                  >
                      {{ doctor.name }}
                  </vs-option>
          </vs-select>

          <template #footer>
              <div class="popup__right">
                  <vs-button
                      success
                      @click="finishReassign()"
                  >
                      Save
                  </vs-button>
              </div>
          </template>
      </vs-dialog>

        <vs-dialog
            width="500px"
            v-model="activeExaminationDetail"
        >
            <template #header>
                <h5>
                    Examination date: {{ detailExamination.date_of_examination }}
                </h5>
            </template>

            <div style="padding-left: 1em;">
              <h6>Brief description of examination:</h6>

              <p> {{ detailExamination.description }} </p>

              <h6>Actions made during this examination:</h6>

              <div
                  v-for="(action, index) in detailExamination.actions"
                  v-bind:key="index"
              >
                <div>
                    <span>{{ index+1 }}. <b>{{ action }}</b></span>
                </div>
              </div>
            </div>
        </vs-dialog>

        <vs-dialog
            width="500px"
            v-model="activeReportDetail"
        >
            <div style="padding: 1.5em;">
              <h6><b>Date</b>: {{ detailReport.date_of_created }}</h6>

              <br>

              <p><b>Description</b>: {{ detailReport.description }}</p>

              <br>

              <h6><b>Attached files</b>: No attached files</h6>
            </div>

        </vs-dialog>
  </div>
</template>

<script>
import HealthConcernsService from "@/services/healthConcernsService";
import ExaminationsService from "@/services/examinationsService";
import DoctorsService from "@/services/doctorsService";
import DoctorsReportsService from "@/services/doctorsReportsService";

import DateUtils from "@/utils/dateUtils";
import NotificationsUtils from "@/utils/notificationsUtils";

export default {
  name: "ConcernDetail",

  props: {
    id: String,
  },

  data:() => ({
      activeAssign: false,

      activeExaminationDetail: false,
      detailExamination: {},

      activeReportDetail: false,
      detailReport: {},

      toReassign: {},
      newDoc: -1,

      concern: {},
      availableDoctors: [],
      examinations: [],
      reports: [],
  }),

  async created() {
      HealthConcernsService.get(this.id)
          .then(response => {
              this.concern = response.data;
          })
          .catch(e => {
              console.log(e);
          });

      DoctorsService.getAll()
            .then(response => {
            this.availableDoctors = response.data;
            })
            .catch(e => {
            console.log(e);
            });

      ExaminationsService.getByConcern(this.id)
            .then(response => {
                this.examinations = response.data;
            })
            .catch(e => {
                console.log(e);
            });

      DoctorsReportsService.getByConcern(this.id)
            .then(response => {
                this.reports = response.data;
            })
            .catch(e => {
                console.log(e);
            });
  },

  methods: {
      getDate(date) {
          return DateUtils.getDateForFrontend(date);
      },

      getState(rawState) {
          if(rawState === 'WT') {
              return 'Waiting for first examination';
          }

          if(rawState === 'ON') {
              return 'Ongoing';
          }

          if(rawState === 'TL') {
              return 'Terminal';
          }

          if(rawState === 'ED') {
              return 'Ended';
          }

          return 'Unknown state';
      },

      redirectToNewRequest(healthConcernId) {
          this.$router.push({ name: 'newExaminationRequest', params: { id: healthConcernId }});
      },

      redirectToExamination(healthConcernId) {
          this.$router.push({ name: 'examine', params: { id: healthConcernId }});
      },

      reassign(concern) {
          this.activeAssign = true;
          this.toReassign = concern;
          this.newDoc = concern.doctor.id;
      },

      showExaminationDialog(examination) {
          this.detailExamination = {...examination};
          this.activeExaminationDetail = true;
      },

      showReportDialog(report) {
          this.detailReport = {...report};
          this.activeReportDetail = true;
      },

      async finishReassign() {
          let newConcern = {...this.toReassign}
          newConcern.doctor = this.newDoc;
          newConcern.patient = this.toReassign.patient.id;

          HealthConcernsService.update(this.toReassign.id, newConcern)
              .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('Manager of ' + newConcern.name + ' successfully changed.', this.$vs);
              })
              .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
              });
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

    .info__basic {
        padding-bottom: 2em;
        padding-top: 1em;
    }

    .popup__center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        padding-bottom: 4em;
        width: 40%;
        margin-top: 2em;
    }

    .popup__right {
      position: absolute;
      right: 1em;
      bottom: 1em;
    }

    box-icon {
        fill: #fbfbfb;
    }
</style>