<template>
  <div>
    <div class="main__content">
        <h1 class="patients__header">All patients</h1>

        <vs-table striped class="patients__table">
            <template #header>
                <vs-input v-model="searchValue" border placeholder="Search" />
            </template>

            <template #thead>
                <vs-tr>
                    <vs-th>
                        Name
                    </vs-th>

                    <vs-th>
                        Date of birth
                    </vs-th>

                    <vs-th>
                        Email contact
                    </vs-th>

                    <vs-th>
                        Main Doctor
                    </vs-th>
                </vs-tr>
            </template>

            <template #tbody>
                <vs-tr
                    :key="i"
                    v-for="(patient, i) in $vs.getPage($vs.getSearch(patients, searchValue), page, max)"
                    :data="patient"
                >
                    <vs-td>
                        {{ patient.name }}
                    </vs-td>

                    <vs-td>
                        {{ patient.date_of_birth }}
                    </vs-td>

                    <vs-td>
                        {{ patient.email_field }}
                    </vs-td>

                    <vs-td>
                        {{ patient.mainDoctor.name }}
                    </vs-td>
                </vs-tr>
            </template>

            <template #footer>
                <vs-pagination v-model="page" :length="$vs.getLength(patients, max)" />
            </template>
        </vs-table>
    </div>
  </div>
</template>

<script>
import PatientsService from "@/services/patientsService";

export default {
    name: 'PatientsOverview',    

    components: {
        
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
        padding: 20px 20px 20px 280px;
    }

    .patients__header {
        margin-left: 15%;
    }

    .patients__table {
        margin: 0 auto;
        width: 70%;
        margin-top: 1em;
    }
</style>