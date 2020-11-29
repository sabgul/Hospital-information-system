<template>
  <div>
    <vs-table striped class="patients__table">
            <template #header>
                <vs-input v-model="searchValue" border placeholder="Search" />
            </template>

            <template #thead>
                <vs-tr>
                    <vs-th>
                        Name
                    </vs-th>

                    <vs-th>
                        Date of birth
                    </vs-th>

                    <vs-th>
                        Email contact
                    </vs-th>

                    <vs-th>
                        Gender
                    </vs-th>
                </vs-tr>
            </template>

            <template #tbody>
                <vs-tr
                    :key="i"
                    v-for="(patient, i) in $vs.getPage($vs.getSearch(patients, searchValue), page, max)"
                    :data="patient"
                >
                    <vs-td>
                      <span @click="redirectToPatientProfile(patient.user.id, 'patient')" class="redirect__profile"><b>{{ patient.user.first_name }} {{ patient.user.last_name }}</b></span>
                    </vs-td>

                    <vs-td>
                        {{ getDate(patient.user.date_of_birth) }}
                    </vs-td>

                    <vs-td>
                        {{ patient.user.email }}
                    </vs-td>

                    <vs-td>
                        {{ getGender(patient.user.gender) }}
                    </vs-td>
                </vs-tr>
            </template>

            <template #footer>
                <vs-pagination v-model="page" :length="$vs.getLength(patients, max)" />
            </template>
        </vs-table>
  </div>
</template>

<script>
import DateUtils from "@/utils/dateUtils";

export default {
  name: "PatientsTable",

  props: {
    patients: {}
  },

  data:() => ({
        page: 1,
        max: 10,
        searchValue: '',
  }),

  methods: {
    redirectToPatientProfile(userId, role) {
        this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }});
        if(this.$route.path !== '/patients')
          this.$router.go();
    },

    getDate(date) {
      return DateUtils.getDateForFrontend(date);
    },

    getGender(rawGender) {
      if(rawGender === 'M') {
        return 'Male';
      }

      if(rawGender === 'F') {
        return 'Female';
      }

      if(rawGender === 'O') {
        return 'Other';
      }
    }
  },
}
</script>

<style scoped>
    .patients__table {
      width: 70%;
      margin: 1em auto 0;
    }

    .redirect__profile:hover {
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }
</style>
