<template>
    <div class="main__content">
        <h1>Add new patient</h1>
        <p>
            Create new patient in the database of patients.<br>
            Some of the basic patient information are necessary to state, but patient can manage his profile later.
        </p>

        <br>

        <vs-input
            v-model="newPatient.name"
            label="Name of patient"
            placeholder="Type name of new patient"
            class="input__items"
            primary
        >
            <template #message-warn v-if="newPatient.name.length === 0">
                Required
            </template>
        </vs-input>

        <vs-select
            v-model="newPatient.main_doctor_id"
            class="input__items"
            label="Main doctor"
            color="primary"
        >
            <template #message-warn v-if="newPatient.main_doctor_id === -1">
                Required
            </template>

            <vs-option v-for="doctor in availableDoctors" :key="doctor.id" :label="doctor.name" :value="doctor.id">
                {{ doctor.name }}
            </vs-option>
        </vs-select>

        <vs-input
            type="date"
            v-model="newPatient.date_of_birth"
            label="Date of birth"
            class="input__items"
        >
          <template #message-warn v-if="!validDateOfBirth">
                Required
           </template>
        </vs-input>

        <vs-input
            v-model="newPatient.email_field"
            label="Email address"
            class="input__items"
        >
            <template v-if="validEmail" #message-success>
                Valid email
            </template>

            <template v-if="!validEmail && newPatient.email_field !== ''" #message-danger>
                Invalid email
            </template>

            <template #message-warn v-if="newPatient.email_field.length === 0">
                Required
            </template>
        </vs-input>

        <vs-input
          v-model="newPatient.phone_number"
          label="Phone number"
          class="input__items"
        >
          <template v-if="validNumber" #message-success>
              Valid phone number
          </template>

          <template v-if="!validNumber && newPatient.phone_number !== ''" #message-danger>
              Invalid phone number
          </template>
        </vs-input>

        <vs-button
            @click="createPatient()"
            :disabled=" newPatient.name.length === 0 ||
                        newPatient.main_doctor_id === -1 ||
                        !validDateOfBirth ||
                        (!validEmail && newPatient.email_field.length !== 0) ||
                        (!validNumber && newPatient.phone_number.length !== 0)"
        >
            Submit
        </vs-button>
    </div>
</template>


<script>
import PatientsService from "@/services/patientsService";
import DoctorsService from "@/services/doctorsService";

export default {
    name: 'PatientAdd',    

    components: {
    },
    
    data:() => ({
        newPatient: {
            'name': '',
            'main_doctor_id': -1,
            'date_of_birth': '',
            'email_field': '',
            'phone_number': '',
        },

        availableDoctors: [],
    }),

    computed: {
        validEmail() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.newPatient.email_field);
        },

        validNumber() {
          return /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im.test(this.newPatient.phone_number);
        },

        validDateOfBirth() {
          return this.newPatient.date_of_birth.length !== 0;
        }
    },

    async created() {
        DoctorsService.getAll()
            .then(response => {
            this.availableDoctors = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },

    methods: {
        async createPatient() {
            const position = 'top-right';
            const progress = 'auto';
            const duration = '6000';

            var data = {
                name: this.newPatient.name,
                mainDoctor: this.newPatient.main_doctor_id,
                date_of_birth: this.formatDate(this.newPatient.date_of_birth),
                email_field: this.newPatient.email_field,
                phone_number: this.newPatient.phone_number
            };

            if(data.date_of_birth === '') {
              data.date_of_birth = null;
            }

            PatientsService.create(data)
                .then(response => {
                    var color = '';

                    if(response) {
                        color = 'success';
                    }
                    color = 'success';

                    const noti = this.$vs.notification({
                        duration,
                        progress,
                        color,
                        position,
                        title: 'Hooray!🎉',
                        text: 'New patient was added to the database.'
                    });
                    console.log(noti);
                })
                .catch(e => {
                    var color = '';

                    if(e) {
                        color = 'danger';
                    }
                    color = 'danger';

                    const noti = this.$vs.notification({
                        duration,
                        progress,
                        color,
                        position,
                        title: 'Whoops!😓: ' + e.message,
                        text: 'Something went wrong. Please try again later or contact support.',
                    });
                    console.log(noti);
                });
        },

        formatDate(date) {
            const day = date.slice(8, 10);
            const month = date.slice(5, 7);
            const year = date.slice(0, 4);

            return year + '-' + month + '-' + day
        },
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

    .switch {
        width: 80px;
        margin-left: 6px;
        margin-top: 16px;
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