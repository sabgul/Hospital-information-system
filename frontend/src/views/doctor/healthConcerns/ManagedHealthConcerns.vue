<template>
    <div>
        <div class="main__content">
            <h1 class="patients__header">
                Overview of managed health concerns
            </h1>

            <p>
                All health concerns of your patients are shown in table below.<br>
                To show more details about particular concern expand given table row.
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
                            Patient
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
                        v-for="(concern, i) in $vs.getPage($vs.getSearch(concerns, searchValue), page, max)"
                        :data="concern"
                    >
                        <vs-td>
                            {{ concern.name }}
                        </vs-td>

                        <vs-td>
                            {{ concern.patient.name }}
                        </vs-td>

                        <vs-td>
                            {{ getState(concern.state) }}
                        </vs-td>

                        <vs-td>
                            <vs-button class="buttons">
                                New examination request
                            </vs-button>

                            <vs-button
                                danger
                                class="buttons"
                            >
                                Assign to another doctor
                            </vs-button>
                        </vs-td>

                        <template #expand>
                          <p><b>Description: </b>{{ concern.description }}</p>

                          <vs-button class="right__part" border>
                                Show more details
                            </vs-button>
                        </template>

                    </vs-tr>
                </template>
                <template #footer>
                    <vs-pagination
                        v-model="page"
                        :length="$vs.getLength(concerns, max)"
                    />
                </template>
            </vs-table>
        </div>
    </div>
</template>

<script>
import HealthConcernsService from '@/services/healthConcernsService.js';

export default {
    name: 'ManagedHealthConcerns',

    data:() => ({
        page: 1,
        max: 5,
        searchValue: '',

        concerns: [],
    }),

    async created() {
        HealthConcernsService.getAll()
            .then(response => {
            this.concerns = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },

    methods: {
        getState(rawState) {
            if(rawState === 'WT') {
                return 'Waiting for first examination';
            }

            if(rawState === 'ON') {
                return 'Ongoing';
            }

            if(rawState === 'TL') {
                return 'Terminal';
            }

            if(rawState === 'ED') {
                return 'Ended';
            }

            return 'Unknown state';
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

    .actions__table {
      width: 80%;
      margin: 1em auto 0;
    }

    .buttons {
      margin: 5px 0;
    }

    .right__part {
      position: absolute;
      right: 10px;
      top: 0;
    }
</style>