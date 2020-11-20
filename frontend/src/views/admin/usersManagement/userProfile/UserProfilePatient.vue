<template>
  <div>
    <h3>Health report card</h3>
    <br>
    <h5>
        <b>Main doctor: </b>

        <span
            @click="redirectToDocProfile(patient.mainDoctor.id, 'doctor')"
            class="redirect__profile"
        >
            {{ patient.mainDoctor.name }}
        </span>
    </h5>

    <br>

    <h5><b>Patient's health concerns:</b></h5>

   <vs-table
                striped
                class="actions__table"
            >
                <template #header>
                    <vs-input
                        v-model="searchValue"
                        border
                        placeholder="Search"
                    />
                </template>

                <template #thead>
                    <vs-tr>
                        <vs-th>
                            Name of health concern
                        </vs-th>

                        <vs-th>
                            State
                        </vs-th>

                        <vs-th>
                            Actions
                        </vs-th>

                    </vs-tr>
                </template>

                <template #tbody>
                    <vs-tr
                        :key="i"
                        v-for="(concern, i) in $vs.getPage($vs.getSearch(healthConcerns, searchValue), page, max)"
                        :data="concern"
                    >
                        <vs-td>
                            <span @click="redirectToConcernDetail(concern.id)" class="concern__name">
                                {{ concern.name }}
                            </span>
                        </vs-td>

                        <vs-td>
                            {{ getState(concern.state) }}
                        </vs-td>

                        <vs-td>
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
                        </vs-td>

                        <template #expand>
                          <div style="width: 80%;">
                          <p><b>Description: </b>{{ concern.description }}</p>
                          </div>
                          <vs-button
                              class="right__part"
                              border
                              @click="redirectToConcernDetail(concern.id)"
                          >
                                Show more details
                            </vs-button>
                        </template>

                    </vs-tr>
                </template>

                <template #footer>
                    <vs-pagination
                        v-model="page"
                        :length="$vs.getLength(healthConcerns, max)"
                    />
                </template>
            </vs-table>

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
  </div>
</template>

<script>

import HealthConcernsService from "@/services/healthConcernsService";
import DoctorsService from "@/services/doctorsService";
import NotificationsUtils from "@/utils/notificationsUtils";

export default {
  name: "UserProfilePatient",

  data:() => ({
      page: 1,
      max: 5,
      searchValue: '',

      activeAssign: false,
      toReassign: {},
      newDoc: -1,

      healthConcerns: [],
      availableDoctors: [],
  }),

  props: {
      patient: {},
  },

  created() {
    HealthConcernsService.getAllByPatient(this.patient.id)
        .then(response => {
            this.healthConcerns = response.data;
        })

    DoctorsService.getAll()
            .then(response => {
            this.availableDoctors = response.data;
            })
  },

  methods: {
      getState(rawState) {
          if(rawState === 'WT') {
              return 'Waiting';
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

      reassign(concern) {
          this.activeAssign = true;
          this.toReassign = concern;
          this.newDoc = concern.doctor.id;
      },

      finishReassign() {
          let newConcern = {...this.toReassign}
          newConcern.doctor = this.newDoc;
          newConcern.patient = this.toReassign.patient.id;

          HealthConcernsService.update(this.toReassign.id, newConcern)
          .then(response => {
              console.log(response);
              NotificationsUtils.successPopup('Manager of ' + newConcern.name + ' successfully changed.', this.$vs);

              HealthConcernsService.getAll()
                  .then(response => {
                  this.concerns = response.data;
                  })
          })
          .catch(e => {
              NotificationsUtils.failPopup(e, this.$vs);
          });
      },

      redirectToNewRequest(healthConcernId) {
          this.$router.push({ name: 'newExaminationRequest', params: {id: healthConcernId }});
      },

      redirectToExamination(healthConcernId) {
          this.$router.push({ name: 'examine', params: { id: healthConcernId }});
      },

      redirectToDocProfile(userId, role) {
          this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }});
          this.$router.go();
      },

      redirectToConcernDetail(concernId) {
         this.$router.push({ name: 'healthConcernDetail', params: {id: concernId }});
      }
  }
}
</script>

<style scoped>
    .redirect__profile:hover, .concern__name:hover {
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }

    .right__part {
      position: absolute;
      right: 10px;
      top: 0;
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
</style>