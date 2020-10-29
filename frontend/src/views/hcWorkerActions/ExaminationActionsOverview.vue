<template>
    <div>
        <div class="main__content">
            <h1>Examination actions overview</h1>

            <p>
                You can see all examinations related to this hospital.<br>
                You are able to edit name of each examinations and its pricing.
            </p>
        </div>

        <div class="main__content">
            <h4>Filter results</h4>

            <div class="wrapper">
                <div class="left__filter__row">
                    <vs-select 
                        v-model="filter.action_manager"
                        label="Action manager"
                        color="primary"
                    >   
                        <vs-option v-for="worker in availableWorkers" :key="worker.id" label="worker.name" :value="worker.id">
                            {{ worker.name }}
                        </vs-option>
                    </vs-select>
                </div>

                <div class="right__filter__row">
                    <vs-select 
                        v-model="filter.is_action_paid"
                        label="Action pricing"
                        color="primary"
                    >   
                        <vs-option value="true" label="Paid">
                            Paid only
                        </vs-option>

                        <vs-option value="false" label="Free">
                            Free only
                        </vs-option>
                    </vs-select>
                </div>

                <div class="filter__submit">
                    <vs-button  @click="clearFilter()" style="padding: 3px 25px;" border>
                        Clear filter
                    </vs-button>

                    <vs-button  @click="getFiltered()" style="padding: 3px 42px;">
                        Filter
                    </vs-button>
                </div>
            </div>
        </div>

        <div class="main__content">
            <vs-table striped class="actions__table">
                <template #header>
                    <vs-input v-model="searchValue" border placeholder="Search" />
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
                            {{ action.action_manager.name }}
                        </vs-td>

                        <vs-td>
                            <vs-button @click="editAction(action.name, action.is_action_paid)">
                                Edit
                            </vs-button>
                            <vs-button danger @click="deleteAction(action.name)">
                                Delete
                            </vs-button>
                        </vs-td>
                    </vs-tr>
                </template>

                <template #footer>
                    <vs-pagination v-model="page" :length="$vs.getLength(actions, max)" />
                </template>
            </vs-table>
        </div>

        <vs-dialog width="300px" v-model="activeDelete">
            <template #header>
            <h5>
                Are you sure you want to remove <b>{{ toDelete }}</b> from database?
            </h5>
            </template>

            <template #footer>
            <div class="center">
                <vs-button @click="finalDeletion()" danger>
                Yep, delete it
                </vs-button>

                <vs-button @click="cancelDeletion()" transparent>
                Abort mission
                </vs-button>
            </div>
            </template>
        </vs-dialog>

        <vs-dialog width="500px" v-model="activeEdit">
            <template #header>
                <h5>
                    Editing action <b>{{ newNameConst }}</b>
                </h5>
            </template>

            <vs-input v-model="toEdit.name" label="Name"/>

            <vs-switch v-model="toEdit.is_action_paid" class="switch">
                <template #off>
                    Free
                </template>

                <template #on>
                    Paid
                </template>
            </vs-switch>
            
            <template #footer>
                <div class="center">
                    <vs-button @click="finalEdit()" success>
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

export default {
    name: 'ExaminationActionsOverview',    

    components: {
    },
    
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
            action_manager: 1,
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
            .catch(e => {
                console.log(e);
            });

        HealthcareWorkersService.getAll()
            .then(response => {
                this.availableWorkers = response.data;
            })
            .catch(e => {
                console.log(e);
            });
    },
    
    methods: {
        getPricingInfo(value) {
            return value ? 'PAID' : 'FREE';
        },

        getFiltered() {
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
            .catch(e => {
                console.log(e);
            });
        },

        deleteAction(name) {
            this.activeDelete = true;
            this.toDelete = name;
        },

        cancelDeletion() {
            this.activeDelete = false;
            this.toDelete = '';
        },

        finalDeletion() {
            const position = 'top-right';
            const progress = 'auto';
            const duration = '6000';

            ExaminationActionsService.delete(this.toDelete)
            .then(response => {
                var color = '';
                response ? color = 'success' : color = 'success';

                const noti = this.$vs.notification({
                    duration,
                    progress,
                    color,
                    position,
                    title: 'Hooray!🎉',
                    text: 'Examination action successfuly deleted.'
                });
                console.log(noti);

                ExaminationActionsService.getAll()
                .then(response => {
                    this.actions = response.data;
                })
                .catch(e => {
                    var color = '';
                    e ? color = 'success' : color = 'success';

                    const noti = this.$vs.notification({
                        duration,
                        progress,
                        color,
                        position,
                        title: 'Whoops!😓: ' + e.message,
                        text: 'Action was not deleted. Try again later or contact support.'
                    });
                    console.log(noti);
                });
            })
            .catch(e => {
                console.log(e);
            });         
            this.activeDelete = false;
        },

        editAction(name, pricing) {
            this.activeEdit = true;
            this.toEdit.name = name;
            this.newNameConst = name;
            this.toEdit.is_action_paid = pricing;
        },

        finalEdit() {
            ExaminationActionsService.update(this.newNameConst, this.toEdit)
            .then(response => {
                console.log(response); 
            })
            .catch(e => {
                console.log(e);
            });  

            if(this.newNameConst !== this.toEdit.name) {
                ExaminationActionsService.delete(this.newNameConst)
                .then(response => {
                    console.log(response);

                    ExaminationActionsService.getAll()
                    .then(response => {
                        this.actions = response.data;
                    })
                    .catch(e => {
                        console.log(e);
                    });
                })
                .catch(e => {
                    console.log(e);
                });
            }        

            ExaminationActionsService.getAll()
            .then(response => {
                this.actions = response.data;
            })
            .catch(e => {
                console.log(e);
            });

            this.activeEdit = false;
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
        margin-top: 20px;
        margin-left: 25%;
        margin-right: 15%;
        background-color: #ffffff;
        box-shadow:
            0 1.3px 20.1px rgba(0, 0, 0, 0.003),
            0 4.2px 44.8px rgba(0, 0, 0, 0.003),
            0 19px 76px rgba(0, 0, 0, 0.06);
        border-radius: 10px;
    }

    .background__img {
        width: 30%;
        position: absolute;
        right: 50px;
        bottom: 50px;
        z-index: -1;
    }

    .actions__table {
        margin: 0 auto;
        width: 80%;
        margin-top: 1em;
    }

    .center {
        float: right;
        padding-bottom: 10px;
    }

    .switch {
        width: 100px;
        margin-left: 6px;
        margin-top: 16px;
    }

    .wrapper {
        display: flex;
        padding-top: 2em;
    }

    .left__filter__row {
        width: 200px;
    }

    .right__filter__row {
        padding-left: 2em;
        flex-grow: 1;
    }

    .filter__submit {
        margin-left: auto;
        order: 3;
    }
</style>