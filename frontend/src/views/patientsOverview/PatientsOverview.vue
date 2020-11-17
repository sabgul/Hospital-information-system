<template>
  <div>
    <div class="main__content">
      <h1>All patients</h1>

      <p>
          TODO nejaky text
      </p>
    </div>

    <div class="main__content">
      <patients-table :patients="patients"/>
    </div>
  </div>
</template>

<script>
import PatientsService from "@/services/patientsService";
import PatientsTable from "@/components/PatientsTable";

export default {
    name: 'PatientsOverview',    

    components: {
        PatientsTable,
    },

    data:() => ({
        patients: [],
        page: 1,
        max: 10,
        searchValue: '',
    }),

    async created() {
        PatientsService.getAll()
            .then(response => {
            this.patients = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },

    methods: {
    },
}
</script>

<style scoped>
</style>