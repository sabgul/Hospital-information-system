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
                        Main Doctor
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
                        <span @click="redirectToPatientProfile(patient.id, 'patient')" class="redirect__profile">{{ patient.name }}</span>
                    </vs-td>

                    <vs-td>
                        {{ patient.date_of_birth }}
                    </vs-td>

                    <vs-td>
                        {{ patient.email_field }}
                    </vs-td>

                    <vs-td>
                      <span @click="redirectToDoctorProfile(patient.main_doctor.id, 'doctor')" class="redirect__profile">{{ patient.main_doctor.name }}</span>
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
        // this.$router.go();
    },

    redirectToDoctorProfile(userId, role) {
        this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }});
        // this.$router.go();
    },
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
