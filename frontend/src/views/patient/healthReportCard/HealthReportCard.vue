<template>
    <div>
        <div class="main__content">
            <h1>My health report card</h1>

            <br>

            <p>This is your health report card. By clicking on the name of a health concern or by clicking on 'Show more details',
              <br>
              you can see all the examinations and doctor reports related to a given concern.
            </p>
        </div>

        <div class="main__content">
            <h4>
                Filter your health concerns
            </h4>

          <form action="#" v-on:submit.prevent="getFiltered">
            <div class="wrapper">
                <div class="first__row">
                    <vs-select
                        v-model="filter.state"
                        label="State"
                        color="primary"
                    >
                        <vs-option
                            value="WT"
                            label="Waiting"
                        >
                            Waiting
                        </vs-option>

                        <vs-option
                            value="ON"
                            label="Ongoing"
                        >
                            Ongoing
                        </vs-option>

                        <vs-option
                            value="ED"
                            label="Ended"
                        >
                            Ended
                        </vs-option>
                    </vs-select>
                </div>

                <div class="submit__row" style="margin-top: 2em; margin-bottom: 4em;">
                    <vs-button
                        @click="clearFilter()"
                        style="padding: 3px 25px;"
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
                            Name of health concern
                        </vs-th>

                        <vs-th>
                            Description
                        </vs-th>

                        <vs-th>
                            State
                        </vs-th>

                        <vs-th>
                            Actions
                        </vs-th>
                    </vs-tr>
                </template>

                <template #tbody>
                    <vs-tr
                        :key="i"
                        v-for="(concern, i) in $vs.getPage($vs.getSearch(healthConcerns, searchValue), page, max)"
                        :data="concern"
                    >
                        <vs-td>
                            <span @click="redirectToConcernDetail(concern.id)" class="concern__name">
                                <b>{{ concern.name }}</b>
                            </span>
                        </vs-td>

                        <vs-td>
                            {{ concern.description.length ? concern.description : '-' }}
                        </vs-td>

                        <vs-td>
                            {{ getState(concern.state) }}
                        </vs-td>

                        <vs-td>
                            <vs-button
                              class="right__part"
                              border
                              @click="redirectToConcernDetail(concern.id)"
                            >
                                Show more details
                            </vs-button>
                        </vs-td>
                    </vs-tr>
                </template>

                <template #footer>
                    <vs-pagination
                        v-model="page"
                        :length="$vs.getLength(healthConcerns, max)"
                    />
                </template>
            </vs-table>
        </div>
    </div>
</template>

<script>
import HealthConcernsService from "@/services/healthConcernsService";

import StateUtils from "@/utils/stateUtils";

import { mapState } from "vuex";

export default {
    name: "HealthReportCard",

    data:() => ({
        page: 1,
        max: 5,
        searchValue: '',

        healthConcerns: [],

        filter: {
            state: -1,
        }
    }),

    computed: {
        ...mapState([
            'user',
            'userRole'
        ])
    },

    async created() {
        HealthConcernsService.getAllByPatient(this.user.id)
            .then(response => {
                this.healthConcerns = response.data;
            })
    },

    methods: {
        getState(rawState) {
            return StateUtils.getExaminationState(rawState);
        },

        redirectToConcernDetail(concernId) {
          console.log(concernId)
           this.$router.push({ name: 'healthConcernDetail', params: {id: concernId }});
        },

        async clearFilter() {
            this.filter.state = -1;

             HealthConcernsService.getAllByPatient(this.user.id)
                 .then(response => {
                    this.healthConcerns = response.data;
                 })
        },

        async getFiltered() {
            HealthConcernsService.getFilteredByPatient(this.user.id, this.filter)
                .then(response => {
                    this.healthConcerns = response.data;
                })
        }
    },
}
</script>

<style scoped>
    .actions__table {
        width: 80%;
        margin: 1em auto 0;
    }
</style>
