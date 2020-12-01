<template>
    <div>
        <h3>Health report card</h3>

        <br>

        <h5>
            <b>Main doctor: </b>

            <span
                @click="redirectToDocProfile(patient.main_doctor.user.id, 'doctor')"
                class="redirect__profile"
            >
                {{ patient.main_doctor.user.first_name }} {{ patient.main_doctor.user.last_name }}
            </span>
        </h5>

        <br>

        <h5>
          <b>Height:</b> {{ patient.height }} cm
        </h5>

        <h5>
          <b>Weight:</b> {{ patient.weight }} kg
        </h5>

        <br>

        <h5 v-if="patient.taking_medications">
            <b>Medications:</b> {{ patient.medications }}
        </h5>

        <h5 v-else>
            <b>No medications taken</b>
        </h5>

        <br>

        <div>
            <h5>
                <b>Emergency contact person:</b>

                <br>

                <span v-if="patient.ec_first_name.length || patient.ec_last_name">
                    Name: {{ patient.ec_first_name }} {{patient.ec_last_name }}
                </span>

                <br>

                <span v-if="patient.ec_relationship.length">
                    Relation: {{ patient.ec_relationship }}
                </span>

                <br>

                <span v-if="patient.ec_contact_number.length">
                    Contact number: <b>{{ patient.ec_contact_number }}</b>
                </span>
            </h5>
        </div>

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

                    <vs-th v-if="userRole === 'patient'">
                        Description
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
                            <b>{{ concern.name }}</b>
                        </span>
                    </vs-td>

                    <vs-td>
                        {{ getState(concern.state) }}
                    </vs-td>

                    <vs-td v-if="userRole === 'patient'">
                        {{ concern.description.length ? concern.description : '-' }}
                    </vs-td>

                    <vs-td>
                        <vs-button
                            v-if="(userRole === 'admin' || userRole === 'doctor') && concern.state !== 'ED'"
                            border
                            @click="redirectToExamination(concern.id)"
                            style="width: 170px;"
                        >
                            Examine
                        </vs-button>

                        <vs-button
                            v-if="(userRole === 'admin' || userRole === 'doctor') && concern.state !== 'ED'"
                            class="buttons"
                            @click="redirectToNewRequest(concern.id)"
                            style="width: 170px;"
                        >
                            New examination request
                        </vs-button>

                        <vs-button
                            v-if="(userRole === 'admin' || userRole === 'doctor') && concern.state !== 'ED'"
                            danger
                            class="buttons"
                            @click="reassign(concern)"
                            style="width: 170px;"
                        >
                            Assign to another doctor
                        </vs-button>

                        <vs-button
                            v-if="userRole === 'patient' || concern.state === 'ED'"
                            class="buttons"
                            border
                            @click="redirectToConcernDetail(concern.id)"
                        >
                              Show more details
                        </vs-button>
                    </vs-td>

                    <template #expand v-if="userRole === 'admin' || userRole === 'doctor'">
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

        <vs-button
            v-if="userRole === 'doctor' || userRole === 'admin'"
            warn
            gradient
            @click="redirectToNewConcern()"
            class="add__concern"
        >
            <box-icon name="plus" style="fill: #fff"/> Add new health concern
        </vs-button>

        <vs-dialog
            width="500px"
            v-model="activeAssign"
        >
            <template #header>
                <h5>
                    Select new manager of <b>{{ toReassign.name }}</b>
                </h5>
            </template>

            <select
                v-model="newDoc"
                class="popup__center"
            >
                    <option
                        v-for="doctor in availableWithoutCurrent"
                        :key="doctor.user.id"
                        :label="doctor.user.first_name"
                        :value="doctor.user.id"
                    >
                        {{ doctor.user.first_name }}
                    </option>
            </select>

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
import StateUtils from "@/utils/stateUtils";

import { mapState } from "vuex";

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

  computed: {
      ...mapState([
          'user',
          'userRole',
      ]),

      availableWithoutCurrent() {
          return this.availableDoctors.filter((doctor) => doctor.user.id !== this.user.id);
      }
  },

  async created() {
      HealthConcernsService.getAllByPatient(this.patient.user.id)
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
          return StateUtils.getExaminationState(rawState);
      },

      reassign(concern) {
          this.activeAssign = true;
          this.toReassign = concern;
          this.newDoc = concern.doctor.id;
      },

      async finishReassign() {
          let newConcern = {...this.toReassign}
          newConcern.doctor = this.newDoc;
          newConcern.patient = this.toReassign.patient.user.id;

          HealthConcernsService.update(this.toReassign.id, newConcern)
          .then(response => {
              console.log(response);
              NotificationsUtils.successPopup('Manager of ' + newConcern.name + ' successfully changed.', this.$vs);

              HealthConcernsService.getAllByPatient(this.patient.id)
              .then(response => {
                  this.healthConcerns = response.data;
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
      },

      redirectToNewConcern() {
          this.$router.push({ name: 'healthConcerns' });
      }
  }
}
</script>

<style scoped>
    .right__part {
        position: absolute;
        right: 10px;
        top: 0;
    }

    select {
        padding-top: 0;
    }

    .actions__table {
        width: 70%;
        margin: 1em auto 0;
    }

    .popup__center {
        font-family: 'Roboto', sans-serif;
        border-radius:10px;
        border:1px solid #f9fcfd;
        background-color: #eef5f8;
        display: block;
        padding-bottom: 1em;
        width: 40%;
        margin: 2em auto 5em;
    }

    .add__concern {
        position: relative;
        margin-top: 2em;
        margin-left: auto;
        margin-right: auto;
    }
</style>
