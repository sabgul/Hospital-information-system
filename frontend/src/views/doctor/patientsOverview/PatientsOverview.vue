<template>
    <div>
        <div class="main__content">
            <h1>All patients</h1>

              <br>
              <p>
                This module provides you with an overview of all your patients. More information can be obtained by clicking on the name of patient, which leads to their profile.
              <br>
                There you can see detailed description of their health concerns, as well as their personal information.

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

import { mapState } from "vuex";

export default {
    name: 'PatientsOverview',    

    components: {
        PatientsTable,
    },

    computed: {
        ...mapState([
            'user',
            'userRole',
        ])
    },

    data:() => ({
        patients: [],
        page: 1,
        max: 10,
        searchValue: '',
    }),

    async created() {
        if(this.userRole === 'admin') {
            PatientsService.getAll()
            .then(response => {
                this.patients = response.data;
            })
        }

        if(this.userRole === 'doctor') {
            PatientsService.getAllByDoctor(this.user.id)
            .then(response => {
                this.patients = response.data;
            })
        }
    },
}
</script>
