<template>
    <div>
        <user-profile-patient :patient="user"/>
    </div>
</template>

<script>
import UserProfilePatient from "@/views/admin/usersManagement/userProfile/UserProfilePatient";
import { mapState } from "vuex";

export default {
    name: "HealthReportCard",

    components: {
        UserProfilePatient,
    },

    computed: {
        ...mapState([
            'user',
        ])
    },
}
</script>

<style scoped>

</style>