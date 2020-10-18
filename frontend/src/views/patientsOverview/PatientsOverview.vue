<template>
  <div>
    <side-bar/>

    <div class="main__content">
        <h1 class="patients__header">All patients</h1>

        <vs-table striped class="patients__table">
            <template #thead>
                <vs-tr>
                    <vs-th>
                        Name
                    </vs-th>

                    <vs-th>
                        Main Doctor
                    </vs-th>

                    <vs-th>
                        Id
                    </vs-th>
                </vs-tr>
            </template>

            <template #tbody>
                <vs-tr
                    :key="i"
                    v-for="(patient, i) in patients"
                    :data="patient"
                >
                    <vs-td>
                        {{ patient.name }}
                    </vs-td>

                    <vs-td>
                        {{ patient.mainDoctor }}
                    </vs-td>

                    <vs-td>
                        {{ patient.id }}
                    </vs-td>
                </vs-tr>
            </template>
        </vs-table>

        <h3>Add new patient</h3>
            <vs-input 
                v-model="newPatient.name" 
                placeholder="Name"
            />

            <vs-input 
                v-model="newPatient.mainDoctor" 
                placeholder="Main Doctor Name"
            />

            <vs-button @click="createPatient">
                Submit
            </vs-button>
    </div>
  </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue';

export default {
    name: 'PatientsOverview',    

    components: {
        SideBar,
    },

    data:() => ({
        patients: [],
        newPatient: {
            'name': '',
            'mainDoctor': '',
        },
    }),

    async created() {
        var response = await fetch('http://localhost:8000/test/patients/');
        this.patients = await response.json();
    },

    methods: {
        async createPatient() {
            var response = await fetch('http://localhost:8000/test/patients/', {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.newPatient)
            });
            this.students.push(await response.json());
        }
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
    }
</style>