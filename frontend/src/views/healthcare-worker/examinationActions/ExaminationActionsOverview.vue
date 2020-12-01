<template>
    <div>
        <div class="main__content">
            <h1>
                Examination actions overview
            </h1>

            <p>
                In this module, you can find the overview of all actions that can be performed during the examinations. <br>
                The names and character in terms of pricing can be edited.
            </p>
        </div>

        <div class="main__content">
            <h5>
                Filter results
            </h5>

          <form action="#" v-on:submit.prevent="getFiltered">
            <div class="wrapper">
                <div class="first__row">
                    <vs-select 
                        v-model="filter.action_manager"
                        label="Action manager"
                        color="primary"
                        :key="availableWorkers.length"
                    >   
                        <vs-option
                            v-for="worker in availableWorkers"
                            :key="worker.user.id"
                            :label="getFullName(worker.user)"
                            :value="worker.user.id"
                        >
                            {{ worker.user.first_name }} {{ worker.user.last_name }}
                        </vs-option>
                    </vs-select>
                </div>

                <div class="second__row">
                    <vs-select 
                        v-model="filter.is_action_paid"
                        label="Action pricing"
                        color="primary"
                    >   
                        <vs-option
                            value="true"
                            label="Paid"
                        >
                            Paid only
                        </vs-option>

                        <vs-option
                            value="false"
                            label="Free"
                        >
                            Free only
                        </vs-option>
                    </vs-select>
                </div>

                <div class="submit__row" style="margin-top: 2em; margin-bottom: 4em;">
                    <vs-button
                        @click="clearFilter()"
                        style="padding: 3px 42px;"
                        border
                    >
                        Clear filter
                    </vs-button>

                    <vs-button
                        style="padding: 3px 42px;"
                    >
                        Apply filter
                    </vs-button>
                </div>
            </div>
          </form>
        </div>

        <div class="main__content">
            <h5>
                Results
            </h5>

            <br>

            <vs-table
                striped
                class="actions__table"
            >
                <template #header>
                    <vs-input
                        v-model="searchValue"
                        border
                        placeholder="Search"
                    />
                </template>

                <template #thead>
                    <vs-tr>
                        <vs-th>
                            Name of action
                        </vs-th>

                        <vs-th>
                            Pricing
                        </vs-th>

                        <vs-th>
                            Action manager
                        </vs-th>

                        <vs-th>
                            Actions
                        </vs-th>
                        
                    </vs-tr>
                </template>

                <template #tbody>
                    <vs-tr
                        :key="i"
                        v-for="(action, i) in $vs.getPage($vs.getSearch(actions, searchValue), page, max)"
                        :data="action"
                    >
                        <vs-td>
                            {{ action.name }}
                        </vs-td>

                        <vs-td>
                            <b>{{ getPricingInfo(action.is_action_paid) }}</b>
                        </vs-td>

                        <vs-td>
                            {{ action.action_manager.user ? action.action_manager.user.first_name + ' ' + action.action_manager.user.last_name : 'No manager' }}
                        </vs-td>

                        <vs-td>
                            <vs-button
                                v-if="action.action_manager.user"
                                @click="editAction(action.name, action.is_action_paid, action.action_manager.user.id)"
                            >
                                Edit
                            </vs-button>

                            <vs-button
                                danger
                                @click="deleteAction(action.name)"
                            >
                                Delete
                            </vs-button>
                        </vs-td>
                    </vs-tr>
                </template>

                <template #footer>
                    <vs-pagination
                        v-model="page"
                        :length="$vs.getLength(actions, max)"
                    />
                </template>
            </vs-table>
        </div>

        <vs-dialog
            width="300px"
            v-model="activeDelete"
        >
            <template #header>
            <h5>
                Are you sure you want to remove <b>{{ toDelete }}</b> from database?
            </h5>
            </template>

            <template #footer>
                <div class="center">
                    <vs-button
                        @click="finalDeletion()"
                        danger
                    >
                        Yes, delete it
                    </vs-button>

                    <vs-button
                        @click="cancelDeletion()"
                        transparent
                    >
                        Abort mission
                    </vs-button>
                </div>
            </template>
        </vs-dialog>

        <vs-dialog
            width="500px"
            v-model="activeEdit"
        >
            <template #header>
                <h5>
                    Editing action <b>{{ newNameConst }}</b>
                </h5>
            </template>

            <vs-input
                v-model="toEdit.name"
                label="Name"
                class="popup__center"
            />

            <vs-switch
                v-model="toEdit.is_action_paid"
                class="switch"

            >
                <template #off>
                    Free
                </template>

                <template #on>
                    Paid
                </template>
            </vs-switch>

            <template #footer>
                <div class="center">
                    <vs-button
                        @click="finalEdit()"
                        success
                    >
                        Save
                    </vs-button>
                </div>
            </template>
        </vs-dialog>
    </div>
</template>

<script>
import ExaminationActionsService from "@/services/examinationActionsService";
import HealthcareWorkersService from "@/services/healthcareWorkersService";

import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'ExaminationActionsOverview',

    data:() => ({
        page: 1,
        max: 5,
        searchValue: '',

        actions: [],
        availableWorkers: [],

        activeDelete: false,
        activeEdit: false,
        toDelete: '',
        toEdit: {
            name: '',
            is_action_paid: false,
            action_manager: -1,
        },
        newNameConst: '',

        filter: {
            is_action_paid: -1,
            action_manager: -1,
        }
    }),
    
    async created() {
        ExaminationActionsService.getAll()
            .then(response => {
                this.actions = response.data;
            })

        HealthcareWorkersService.getAll()
            .then(response => {
                this.availableWorkers = response.data;
            })
    },
    
    methods: {
        getPricingInfo(value) {
            return value ? 'PAID' : 'FREE';
        },

        async getFiltered() {
            ExaminationActionsService.getFiltered(this.filter)
                .then(response => {
                    this.actions = response.data;
                })
        },

        async clearFilter() {
            this.filter.is_action_paid = -1;
            this.filter.action_manager = -1;

            ExaminationActionsService.getAll()
            .then(response => {
                this.actions = response.data;
            })
        },

        deleteAction(name) {
            this.activeDelete = true;
            this.toDelete = name;
        },

        cancelDeletion() {
            this.activeDelete = false;
            this.toDelete = '';
        },

        getFullName(usr) {
          return usr.first_name + ' ' + usr.last_name;
        },

        async finalDeletion() {
            ExaminationActionsService.delete(this.toDelete)
            .then(response => {
                console.log(response);
                NotificationsUtils.successPopup('Examination action successfully deleted.', this.$vs);

                ExaminationActionsService.getAll()
                .then(response => {
                    this.actions = response.data;
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e);
                });
            })
            .catch(e => {
                NotificationsUtils.failPopup(e);
            });         
            this.activeDelete = false;
        },

        editAction(name, pricing, managerId) {
            this.activeEdit = true;
            this.toEdit.name = name;
            this.newNameConst = name;
            this.toEdit.is_action_paid = pricing;
            this.toEdit.action_manager = managerId;
        },

        async finalEdit() {
            ExaminationActionsService.update(this.newNameConst, this.toEdit)
            .then(response => {
                console.log(response);
            })

            if(this.newNameConst !== this.toEdit.name) {
                ExaminationActionsService.delete(this.newNameConst)
                .then(response => {
                    console.log(response);

                    ExaminationActionsService.getAll()
                    .then(response => {
                        this.actions = response.data;
                    })
                })
                .catch(e => {
                    console.log(e);
                });
            } else {
              ExaminationActionsService.getAll()
              .then(response => {
                  this.actions = response.data;
                  this.activeEdit = false;
              })
            }
            this.activeEdit = false;
        }
    },
}
</script>

<style scoped>
    .actions__table {
      width: 80%;
      margin: 1em auto 0;
    }

    .center {
        float: right;
        padding-bottom: 0;
        padding-top: 2em !important;
    }

    .switch {
        width: 100px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
