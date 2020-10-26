<template>
    <div class="main__content">
        <h2>Add new examination action</h2>
        <p>
            By adding new examination action, doctors can use them when examinating their patients. <br>
            Thanks to that, you will be able to track unpaid examinations of patients.
        </p>

        <br>

        <vs-input 
            v-model="newAction.name" 
            label="Name of action"
            placeholder="Type name of new action"
            class="input__items"
        >
            <template #message-warn v-if="newAction.name.length === 0">
                Required
            </template>
        </vs-input>

        <vs-select 
            v-model="newAction.action_manager_id"
            class="input__items"
            label="Action manager"
        >   
            <template #message-warn v-if="newAction.action_manager_id === -1">
                Required
            </template>
            <vs-option v-for="worker in availableWorkers" :key="worker.id" :label="worker.name" :value="worker.id">
                {{ worker.name }}
            </vs-option>
        </vs-select>

        <vs-switch 
            v-model="newAction.is_action_paid" 
            class="switch"
        >
            <template #off>
                Free
            </template>

            <template #on>
                Paid
            </template>
        </vs-switch>

        <vs-button>
            Submit
        </vs-button>

        <img class="background__img" src="@/assets/add-action.svg" alt="">
    </div>
</template>


<script>
import HealthcareWorkersService from "@/services/healthcareWorkersService";

export default {
    name: 'ExaminationActionAdd',    

    components: {
    },
    
    data:() => ({
        newAction: {
            name: '',
            is_action_paid: false,
            action_manager_id: -1,
        },

        availableWorkers: [],
    }),
    
    async created() {
        HealthcareWorkersService.getAll()
            .then(response => {
            this.availableWorkers = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },
    
    methods: {
        // async createPatient() {
        //     var data = {
        //         name: this.newPatient.name,
        //         mainDoctor: this.newPatient.mainDoctor
        //     };

        //     PatientsService.create(data)
        //         .then(response => {
        //             console.log(response);
        //         })
        //         .catch(e => {
        //             console.log(e);
        //         });
        // }
    },
}
</script>

<style scoped>
    .main__content {
        padding: 20px 20px 20px 25px;
        margin-left: 25%;
        margin-right: 15%;
        background-color: #fafafa;
        border-radius: 10px;
    }

    .background__img {
        width: 30%;
        position: absolute;
        right: 50px;
        bottom: 50px;
    }

    .switch {
        width: 80px;
        margin-left: 6px;
        margin-top: 16px;
    }

    .input__items {
        padding: 16px 0;
        margin-left: 6px;
    }

    .vs-button {
        float: right;
        padding: 5px 30px;
    }
</style>