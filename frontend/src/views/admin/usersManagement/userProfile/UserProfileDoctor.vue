<template>
  <div>
    <h3>Specific details for Doctor role</h3>
    <br>
    <h5><b>Specializes in:</b> {{ doctor.specializes_in.length === 0 ? 'not stated' : doctor.specializes_in }}</h5>

    <br>

    <h5><b>Assigned patients:</b></h5>

    <patients-table :patients="assignedPatients"/>
  </div>
</template>

<script>
import PatientsService from "@/services/patientsService";
import PatientsTable from "@/components/PatientsTable";

export default {
  name: "UserProfileDoctor",

  components: {
    PatientsTable,
  },

  data:() => ({
        assignedPatients: [],
  }),

  props: {
    doctor: {},
  },

  async created() {
      PatientsService.getAllByDoctor(this.doctor.id)
          .then(response => {
              this.assignedPatients = response.data;
          })
  }
}
</script>

<style scoped>

</style>