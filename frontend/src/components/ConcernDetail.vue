<template>
  <div>
      <div class="main__content">
          <h1>
            Detail of health concern <b>{{ concern.name }}</b>
          </h1>

          <div class="info__basic">
              <h5><b>Patient</b>: {{ concern.patient.name }}</h5>
              <h5><b>Doctor</b>: {{ concern.doctor.name }}</h5>
              <h5><b>State</b>: {{ getState(concern.state) }}</h5>
              <h5><b>Description</b>: {{ concern.description }}</h5>

              <div style="margin-top: 3em">
                  <vs-button class="buttons" @click="redirectToNewRequest(concern.id)">
                      New examination request
                  </vs-button>

                  <vs-button
                      danger
                      class="buttons"
                      @click="reassign(concern)"
                  >
                      Assign to another doctor
                  </vs-button>
              </div>
          </div>
      </div>

      <div class="main__content">
          <h1>
              Passed examinations
          </h1>

          <vs-card-group>
            <vs-card v-for="card in 6" v-bind:key="card.id">
                <template #title>
                    <h3>Pot with a plant</h3>
                </template>

                <template #img>
                  <img src="../assets/user-illu.jpg" alt="">
                </template>

                <template #text>
                    <p>
                        Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                    </p>
                </template>

<!--                <template #interactions>-->
<!--                    <vs-button danger icon>-->
<!--                        <box-icon name='home'/>-->
<!--                    </vs-button>-->

<!--                    <vs-button class="btn-chat" shadow primary icon>-->
<!--                        <box-icon style="fill: #000;" name='message-square-detail'/>-->
<!--                        <span class="span">-->
<!--                            54-->
<!--                        </span>-->
<!--                    </vs-button>-->
<!--                </template>-->
            </vs-card>

            <vs-card>
                <template #title>
                    <h3>New examination request</h3>
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
          <h1>
            Doctors reports related to <b>{{ concern.name }}</b>
          </h1>
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
import HealthConcernsService from "@/services/healthConcernsService";
import DoctorsService from "@/services/doctorsService";

export default {
  name: "ConcernDetail",

  props: {
    id: String,
  },

  data:() => ({
      activeAssign: false,
      toReassign: {},
      newDoc: -1,

      concern: {},
      availableDoctors: [],
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

      redirectToNewRequest(healthConcernId) {
          this.$router.push({ name: 'newExaminationRequest', params: {id: healthConcernId }});
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