<template>
    <div>
        <div class="main__content">
            <h1>My health report card</h1>

            <br>

            <p>This is your health report card. By clicking on name of a health concern or by clicking on 'Show more details',
              <br>
              you can see all examinations and doctor reports related to given concern.
            </p>
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
    }),

    computed: {
        ...mapState([
            'user',
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
           this.$router.push({ name: 'healthConcernDetail', params: {id: concernId }});
        },
    },
}
</script>

<style scoped>

</style>