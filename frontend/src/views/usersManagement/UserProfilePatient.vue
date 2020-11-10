<template>
  <div>
    <h3>Specific details for Patient role</h3>
    <br>
    <h5>
      <b>Main doctor: </b>
      <span @click="redirectToDocProfile(patient.mainDoctor.id, 'doctor')" class="redirect__profile">{{ patient.mainDoctor.name }}</span>
    </h5>

    <br>

    <h5><b>Patient's health concerns:</b></h5>

    <div v-for="concern in healthConcerns" :key="concern.id">
        <div class="concern__content">
            <h4>{{ concern.name }}</h4>
            <p>{{ concern.description }}</p>
            Supervised by: <span>{{ concern.doctor.name }}</span>
            <br>
            State: <span>{{ getState(concern.state) }}</span>
        </div>
    </div>

  </div>
</template>

<script>

import HealthConcernsService from "@/services/healthConcernsService";

export default {
  name: "UserProfilePatient",

  components: {
  },

  data:() => ({
    healthConcerns: [],
  }),

  props: {
    patient: {},
  },

  created() {
    HealthConcernsService.getAllByPatient(this.patient.id)
        .then(response => {
            this.healthConcerns = response.data;
        })
        .catch(e => {
            console.log(e);
        });
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

        return 'Uknown state';
    },

    redirectToDocProfile(userId, role) {
        this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }});
        this.$router.go();
    }
  }
}
</script>

<style scoped>
    .concern__content {
        margin: 20px 0;
        padding: 20px 20px 20px 25px;
        margin-right: 15%;
        background-color: #ffffff;
        box-shadow:
            0 1.3px 20.1px rgba(0, 0, 0, 0.003),
            0 4.2px 44.8px rgba(0, 0, 0, 0.003),
            0 19px 76px rgba(0, 0, 0, 0.06);
        border-radius: 10px;
    }

    .redirect__profile:hover {
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }
</style>