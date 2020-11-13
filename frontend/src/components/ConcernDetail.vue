<template>
  <div>
    <div class="main__content">
        <h1>
          Detail of health concern <b>{{ concern.name }}</b>
        </h1>

        <div class="info__basic">
            <h5><b>Patient</b>: {{ concern.patient.name }}</h5>
            <h5><b>State</b>: {{ getState(concern.state) }}</h5>
            <h5><b>Description</b>: {{ concern.description }}</h5>

            <h1>TODOO</h1>
        </div>
    </div>
  </div>
</template>

<script>
import HealthConcernsService from "@/services/healthConcernsService";

export default {
  name: "ConcernDetail",

  props: {
    id: String,
  },

  data:() => ({
      concern: {},
  }),

  async created() {
      HealthConcernsService.get(this.id)
          .then(response => {
              this.concern = response.data;
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
</style>