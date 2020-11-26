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

      <file-upload
        :url='url'
        :thumb-url='thumbUrl'
        :headers="headers"
        @change="onFileChange"
      />
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
        url: 'http://your-post.url',
        headers: {'access-token': '<your-token>'},
        filesUploaded: []
    }),

    async created() {
        PatientsService.getAll()
            .then(response => {
            this.patients = response.data;
            })
    },

    methods: {
        thumbUrl (file) {
          return file.myThumbUrlProperty;
        },
        onFileChange (file) {
          // Handle files like:
          this.filesUploaded = file;
        },
    }
}
</script>

<style scoped>
</style>