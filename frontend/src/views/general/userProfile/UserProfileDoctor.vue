<template>
    <div>
        <h3>Specific details for Doctor</h3>

        <br>

        <h5><b>Specializes in:</b> {{ doctor.specializes_in.length === 0 ? 'not stated' : doctor.specializes_in }}</h5>

        <br>

        <div v-if="userRole === 'admin' || (userRole === 'doctor' && user.id === doctor.user.id)">
            <h5><b>Assigned patients:</b></h5>

            <patients-table :patients="assignedPatients"/>
        </div>
    </div>
</template>

<script>
import PatientsService from "@/services/patientsService";
import PatientsTable from "@/components/PatientsTable";
import {mapState} from "vuex";

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

    computed: {
        ...mapState([
            'user',
            'userRole',
        ])
    },

    async created() {
        PatientsService.getAllByDoctor(this.doctor.user.id)
        .then(response => {
            this.assignedPatients = response.data;
        })
    }
}
</script>
