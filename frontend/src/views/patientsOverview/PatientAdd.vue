<template>
    <div class="xxx">
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
</template>


<script>
import PatientsService from "@/services/patientsService";

export default {
    name: 'PatientAdd',    

    components: {
    },
    
    data:() => ({
        newPatient: {
            'name': '',
            'mainDoctor': '',
        },
    }),
    
    methods: {
        async createPatient() {
            var data = {
                name: this.newPatient.name,
                mainDoctor: this.newPatient.mainDoctor
            };

            PatientsService.create(data)
                .then(response => {
                    console.log(response);
                })
                .catch(e => {
                    console.log(e);
                });
        }
    },
}
</script>

<style scoped>
    .xxx {
        margin-left: 20%;
        margin-top: 2em;
    }
</style>