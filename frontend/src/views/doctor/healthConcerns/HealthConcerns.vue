<template>
  <div>
    <div class="main__content">
                <h1>
          Health concerns
        </h1>
    </div>

    <div class="main__content">
        <h4>Add health concern</h4>

        <br>

        <p>
            If you were contacted with your patient who told you about his new health concern, <br>
            add the information here. <br>
            <b>If its a new patient, create an account for him first <span>here</span>!</b>
        </p>

        <br>

      <div class="wrapper">
          <div class="first__row">
              <vs-input
                  v-model="newConcern.name"
                  label="Type of health concern"
                  placeholder="Type name"
                  class="input__items"
                  primary
              >
                <template
                  #message-warn
                  v-if="newConcern.name.length === 0"
                >
                  Required field
                </template>

                <template
                  #message-danger
                  v-if="newConcern.name.length > 250"
                >
                 Too many characters
                </template>
              </vs-input>

              <vs-select
                v-model="newConcern.patient"
                class="input__items"
                label="Patient"
                placeholder="Choose a patient"
                color="primary"
                filter
              >
                  <template
                    #message-warn
                    v-if="newConcern.patient === -1"
                  >
                      Required field
                  </template>

                  <vs-option
                    v-for="(patient, id) in availablePatients"
                    :key="id"
                    :label="patient.name"
                    :value="patient.id"
                  >
                    aaa
                  </vs-option>
              </vs-select>
          </div>

          <div class="second__row">
              <vs-input
                  v-model="newConcern.description"
                  label="Description"
                  placeholder="Type brief description"
                  class="input__items"
              >
                <template
                    #message-danger
                    v-if="newConcern.description.length > 2000"
                >
                    Too many characters
                </template>
              </vs-input>

              <vs-select
                v-model="newConcern.doctor"
                class="input__items"
                label="Doctor"
                placeholder="Choose a doctor"
                color="primary"
                filter
              >
                <template
                    #message-warn
                    v-if="newConcern.doctor === -1"
                >
                    Required field
                </template>

                <vs-option
                    v-for="(doc, id) in availableDoctors"
                    :key="id"
                    :label="doc.name"
                    :value="doc.id"
                >
                    {{ doc.name }}
                </vs-option>
              </vs-select>
          </div>

          <div class="third__row__single">
              <vs-select
                v-model="newConcern.state"
                label="State of examination"
                color="primary"
              >
                <vs-option
                    value="WT"
                    label="Waiting"
                >
                    Waiting for examination
                </vs-option>

                <vs-option
                    value="ON"
                    label="Ongoing"
                >
                    Ongoing
                </vs-option>

                <vs-option
                    value="ED"
                    label="Ended"
                >
                    Ended
                </vs-option>
              </vs-select>
          </div>

          <div class="submit__row">
              <vs-button
                  @click="addNewExamination()"
                  :disabled=" newConcern.name.length === 0 ||
                              newConcern.name.length > 250 ||
                              newConcern.doctor === -1 ||
                              newConcern.patient === -1 ||
                              newConcern.description.length > 2000"
              >
                  Submit
              </vs-button>
          </div>
      </div>
    </div>

    <div class="main__content">
        <h4>Health concerns overview</h4>

        <br>

        <p>
           Here you can see all health concerns you manage. <br>
           You can filter the results by patient and/or by examination state. <br>
           You can use Search tab in table as well.
        </p>
    </div>

    <div class="main__content">
      <h4>
        Filter results
      </h4>

      <div class="wrapper" style="height: 130px;">
        <div class="left__filter__row">
          <vs-select
            v-model="filter.patient_name"
            label="Patient"
            color="primary"
          >
            <vs-option
              v-for="patient in availablePatients"
              :key="patient.id"
              label="patient.name"
              :value="patient.id"
            >
              {{ patient.name }}

            </vs-option>

          </vs-select>
        </div>

        <div class="right__filter__row">
          <vs-select
            v-model="filter.state_of_concern"
            label="State of examination"
            color="primary"
          >
            <vs-option
              value="WT"
              label="Waiting"
            >
              Waiting
            </vs-option>
            <vs-option
              value="ON"
              label="Ongoing"
            >
              Ongoing
            </vs-option>
            <vs-option
              value="ED"
              label="Ended"
            >
              Ended
            </vs-option>
          </vs-select>
        </div>

        <div
            class="submit__row"
            style="margin-top: 0;"
        >
            <vs-button
                @click="clearFilter()"
                border
            >
                Clear filter
            </vs-button>

            <vs-button
                @click="getFiltered()"
            >
                Apply filter
            </vs-button>
        </div>
      </div>
    </div>

    <div class="main__content">

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
                            Type of health concern
                        </vs-th>

                        <vs-th>
                            Patient
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
                        v-for="(concern, i) in $vs.getPage($vs.getSearch(concerns, searchValue), page, max)"
                        :data="concern"
                    >
                        <vs-td>
                          <span @click="showConcernDetail(concern.id)" class="redirect__profile">{{ concern.name }}</span>
                        </vs-td>

                        <vs-td>
                           <span @click="redirectToPatientProfile(concern.patient.id, 'patient')" class="redirect__profile">{{ concern.patient.name }}</span>
                        </vs-td>

                        <vs-td>
                            {{ getState(concern.state) }}
                        </vs-td>

                        <vs-td>
                            <vs-button
                                border
                                class="buttons"
                                @click="redirectToExamine(concern.id)"
                                style="width: 120px;"
                            >
                                Examine
                            </vs-button>

                            <vs-button
                                class="buttons"
                                @click="redirectToNewRequest(concern.id)"
                            >
                                New examination request
                            </vs-button>

                            <vs-button
                                danger
                                class="buttons"
                                @click="reassign(concern)"
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
                              @click="showConcernDetail(concern.id)"
                          >
                                Show more details
                            </vs-button>
                        </template>

                    </vs-tr>
                </template>

                <template #footer>
                    <vs-pagination
                        v-model="page"
                        :length="$vs.getLength(concerns, max)"
                    />
                </template>
            </vs-table>
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
   </div>
</template>

<script>
import PatientsService from "@/services/patientsService";
import DoctorsService from "@/services/doctorsService";
import HealthConcernsService from "@/services/healthConcernsService";
import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: "HealthConcerns",

    data:() => ({
        searchValue: '',
        page: 1,
        max: 5,

        activeAssign: false,
        toReassign: {},
        newDoc: -1,

        newConcern: {
          name: '',
          description: '',
          state: 'WT',
          patient: -1,
          doctor: -1, // TODO tu bude id current usera
        },

        availablePatients: [],
        availableDoctors: [],

        concerns: [],

      filter: {
          patient_name: -1,
          state_of_concern: -1,
      }

    }),

    async created() {
        PatientsService.getAll()
            .then(response => {
            this.availablePatients = response.data;
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

        HealthConcernsService.getAll()
            .then(response => {
            this.concerns = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },

    methods: {
        async addNewExamination() {
            HealthConcernsService.create(this.newConcern)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Health concern added to database.', this.$vs);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
        },

    redirectToPatientProfile(userId, role) {
        this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }});
        // this.$router.go();
    },

      async getFiltered() {
          HealthConcernsService.getFiltered(this.filter)
              .then(response => {
                  this.concerns = response.data;
              })
      },

      async clearFilter() {
          this.filter.patient_name = -1;
          this.filter.state_of_concern = -1;

          HealthConcernsService.getAll()
          .then(response => {
            this.concerns = response.data;
          })
          .catch(e => {
            console.log(e);
          });
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

        showConcernDetail(concernId) {
            this.$router.push({ name: 'healthConcernDetail', params: {id: concernId }})
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
                    .catch(e => {
                    console.log(e);
                    });
            })
            .catch(e => {
                NotificationsUtils.failPopup(e, this.$vs);
            });
        },

        redirectToNewRequest(healthConcernId) {
            this.$router.push({ name: 'newExaminationRequest', params: {id: healthConcernId }});
        },

        redirectToExamine(healthConcernId) {
            this.$router.push({ name: 'examine', params: { id: healthConcernId }});
        },
    }
}
</script>

<style scoped>
    .input__items {
        padding: 16px 0;
        margin-left: 6px;
    }

    .actions__table {
        width: 80%;
        margin: 1em auto 0;
    }

    .buttons {
      margin: 5px 0;
    }

    .right__part {
      position: absolute;
      right: 10px;
      top: 0;
    }

    .concern__description {
      height: 100px;
    }

    .redirect__profile:hover {
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }
</style>