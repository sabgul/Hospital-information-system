<template>
  <div>
    <h3>Specific details for Health insurance worker role</h3>
    <br>
    <h5><b>Works for:</b> {{ worker.works_for_company.length === 0 ? 'not stated' : worker.works_for_company }}</h5>

    <br>

    <h5><b>Supervised examination actions:</b></h5>

    <vs-table striped>
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
            </vs-tr>
        </template>

        <template #tbody>
            <vs-tr
                :key="i"
                v-for="(action, i) in $vs.getPage($vs.getSearch(supervised_actions, searchValue), page, max)"
                :data="action"
            >
                <vs-td>
                    {{ action.name }}
                </vs-td>

                <vs-td>
                    <b>{{ getPricingInfo(action.is_action_paid) }}</b>
                </vs-td>
            </vs-tr>
        </template>

        <template #footer>
            <vs-pagination
                v-model="page"
                :length="$vs.getLength(supervised_actions, max)"
            />
        </template>
    </vs-table>
  </div>
</template>

<script>
import ExaminationActionsService from "@/services/examinationActionsService";

export default {
  name: "UserProfileHcWorker",

  components: {
  },

  data:() => ({
        supervised_actions: [],
        page: 1,
        max: 5,
        searchValue: '',
  }),

  props: {
    worker: {},
  },

  async created() {
      ExaminationActionsService.getAllByWorker(this.worker.id)
        .then(response => {
            this.supervised_actions = response.data;
        })
  },

  methods: {
    getPricingInfo(value) {
        return value ? 'PAID' : 'FREE';
    },
  }
}
</script>

<style scoped>

</style>