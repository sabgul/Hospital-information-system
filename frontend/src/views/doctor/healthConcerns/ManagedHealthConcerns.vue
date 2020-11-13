<template>
    <div>
        <div class="main__content">
            <h1 class="patients__header">
                Manage patients health concerns
            </h1>

            <p>
                All health concerns of your patients are shown in table below.<br>
                To show more details about particular concern expand given table row.
            </p>
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
                            Name of health concern
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
                            {{ concern.name }}
                        </vs-td>

                        <vs-td>
                            {{ concern.patient.name }}
                        </vs-td>

                        <vs-td>
                            {{ getState(concern.state) }}
                        </vs-td>

                        <vs-td>
                            <vs-button class="buttons">
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
                          <p><b>Description: </b>{{ concern.description }}</p>

                          <vs-button class="right__part" border>
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
import HealthConcernsService from '@/services/healthConcernsService';
import DoctorsService from '@/services/doctorsService';

export default {
    name: 'ManagedHealthConcerns',

    data:() => ({
        page: 1,
        max: 5,
        searchValue: '',

        activeAssign: false,
        toReassign: {},
        newDoc: -1,

        concerns: [],
        availableDoctors: [],
    }),

    async created() {
        HealthConcernsService.getAll()
            .then(response => {
            this.concerns = response.data;
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
    },

    methods: {
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

        reassign(concern) {
            this.activeAssign = true;
            this.toReassign = concern;
            this.newDoc = concern.doctor.id;
        },

        finishReassign() {
            const position = 'top-right';
            const progress = 'auto';
            const duration = '6000';

            let newConcern = {...this.toReassign}
            newConcern.doctor = this.newDoc;
            newConcern.patient = this.toReassign.patient.id;

          console.log(newConcern);

            HealthConcernsService.update(this.toReassign.id, newConcern)
            .then(response => {
                var color = '';
                response ? color = 'success' : color = 'success';

                const noti = this.$vs.notification({
                    duration,
                    progress,
                    color,
                    position,
                    title: 'Hooray!🎉',
                    text: 'Manager of ' + newConcern.name + ' successfully changed.',
                });
                console.log(noti);

                HealthConcernsService.getAll()
                    .then(response => {
                    this.concerns = response.data;
                    })
                    .catch(e => {
                    console.log(e);
                    });
            })
            .catch(e => {
                var color = '';
                    e ? color = 'danger' : color = 'danger';

                    const noti = this.$vs.notification({
                        duration,
                        progress,
                        color,
                        position,
                        title: 'Whoops!😓: ' + e.message,
                        text: 'There was an error in changing the manager. Try again later or contact support.',
                    });
                    console.log(noti);
            });
        },
    },
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