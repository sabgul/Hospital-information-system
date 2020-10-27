<template>
    <div class="main__content">
        <h1>Add new examination action</h1>
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
            primary
        >
            <template #message-warn v-if="newAction.name.length === 0">
                Required
            </template>
        </vs-input>

        <vs-select 
            v-model="newAction.action_manager_id"
            class="input__items"
            label="Action manager"
            color="primary"
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

        <vs-button 
            @click="addNewExamination()"
            :disabled="newAction.name.length === 0 || newAction.action_manager_id === -1"
        >
            Submit
        </vs-button>

        <img class="background__img" src="@/assets/add-action.svg" alt="">
    </div>
</template>


<script>
import ExaminationActionsService from "@/services/examinationActionsService";
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
        async addNewExamination() {
            const position = 'top-right';
            const progress = 'auto';
            const duration = '6000';

            var data = {
                name: this.newAction.name,
                is_action_paid: this.newAction.is_action_paid,
                action_manager: this.newAction.action_manager_id,
            };

            ExaminationActionsService.create(data)
                .then(response => {
                    var color = '';
                    
                    if(response) {
                        color = 'success';
                    }
                    color = 'success';

                    const noti = this.$vs.notification({
                        duration,
                        progress,
                        color,
                        position,
                        title: 'Hooray!🎉',
                        text: 'Examination action added to database.'
                    });
                    console.log(noti);
                })
                .catch(e => {
                    var color = '';
                    
                    if(e) {
                        color = 'danger';
                    }
                    color = 'danger';

                    const noti = this.$vs.notification({
                        duration,
                        progress,
                        color,
                        position,
                        title: 'Whoops!😓: ' + e.message,
                        text: 'Examination with name `' + this.newAction.name + '` already exists in database.',
                    });
                    console.log(noti);
                });
        }
    },
}
</script>

<style scoped>
    h1 {
        margin-top: 0.5em;
        margin-bottom: 1em;
    }

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
        z-index: -1;
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