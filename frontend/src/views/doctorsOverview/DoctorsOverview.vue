<template>
  <div>
    <div class="main__content">
        <h1 class="doctors__header">
          All Doctors
        </h1>

        <vs-table
            striped
            class="doctors__table"
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
                        Name
                    </vs-th>

                    <vs-th>
                        Date of birth
                    </vs-th>

                    <vs-th>
                        Email contact
                    </vs-th>
                </vs-tr>
            </template>

            <template #tbody>
                <vs-tr
                    :key="i"
                    v-for="(doctor, i) in $vs.getPage($vs.getSearch(doctors, searchValue), page, max)"
                    :data="doctor"
                >
                    <vs-td>
                        {{ doctor.name }}
                    </vs-td>

                    <vs-td>
                        {{ doctor.date_of_birth }}
                    </vs-td>

                    <vs-td>
                        {{ doctor.email_field }}
                    </vs-td>

                </vs-tr>
            </template>

            <template #footer>
                <vs-pagination
                    v-model="page"
                    :length="$vs.getLength(doctors, max)"
                />
            </template>
        </vs-table>
    </div>
  </div>
</template>

<script>
import DoctorsService from "@/services/doctorsService";

export default {

    name: 'DoctorsOverview',

    data:() => ({
        doctors: [],
        page: 1,
        max: 10,
        searchValue: '',
    }),

    async created() {
        DoctorsService.getAll()
            .then(response => {
            this.doctors = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },
}
</script>

<style scoped>
    .main__content {
        padding: 20px 20px 20px 280px;
    }

    .doctors__header {
        margin-left: 15%;
    }

    .doctors__table {
      width: 70%;
      margin: 1em auto 0;
    }
</style>
