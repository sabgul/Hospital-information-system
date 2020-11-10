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
</style>