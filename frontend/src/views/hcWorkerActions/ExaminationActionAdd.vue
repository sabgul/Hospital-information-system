<template>
    <div>
        <div class="main__content">
            <h1>
              Add new examination action
            </h1>

            <p>
                By adding new examination action, doctors can use them when examining their patients. <br>
                Thanks to that, you will be able to track unpaid examinations of patients.
            </p>

            <br>

            <div class="wrapper">
                <div class="first__row">
                    <vs-input
                        v-model="newAction.name"
                        label="Name of action"
                        placeholder="Type name of new action"
                        class="input__items"
                        primary
                    >
                        <template
                            #message-warn
                            v-if="newAction.name.length === 0"
                        >
                            Required
                        </template>
                    </vs-input>
                </div>

                <div class="second__row">
                    <vs-select
                        v-model="newAction.action_manager_id"
                        class="input__items"
                        label="Action manager"
                        color="primary"
                    >
                        <template
                            #message-warn
                            v-if="newAction.action_manager_id === -1"
                        >
                            Required
                        </template>

                        <vs-option
                            v-for="worker in availableWorkers"
                            :key="worker.id"
                            :label="worker.name"
                            :value="worker.id"
                        >
                            {{ worker.name }}
                        </vs-option>
                    </vs-select>
                </div>

                <div class="third__row">
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
                </div>

                <div class="submit__row">
                     <vs-button
                         @click="addNewExamination()"
                         :disabled="newAction.name.length === 0 || newAction.action_manager_id === -1"
                     >
                         Submit
                     </vs-button>
                </div>
            </div>
        </div>

<!--        <div>-->
<!--            <img-->
<!--                class="background__img"-->
<!--                src="@/assets/add-action.svg"-->
<!--                alt=""-->
<!--            >-->
<!--        </div>-->
    </div>
</template>


<script>
import ExaminationActionsService from "@/services/examinationActionsService";
import HealthcareWorkersService from "@/services/healthcareWorkersService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'ExaminationActionAdd',    

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
            const data = {
                name: this.newAction.name,
                is_action_paid: this.newAction.is_action_paid,
                action_manager: this.newAction.action_manager_id,
            };

            ExaminationActionsService.create(data)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Examination action added to database.', this.$vs);
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
        }
    },
}
</script>

<style scoped>
    .background__img {
        width: 30%;
        position: absolute;
        right: 50px;
        bottom: 50px;
        z-index: 0;
    }

    .switch {
        width: 80px;
        margin-left: 6px;
        margin-bottom: 2em;
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