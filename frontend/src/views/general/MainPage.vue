<template>
    <div>
        <top-nav-bar/>
        <div class="row">
            <div class="column left--part">
                <h1 class="headline">
                    HospIS - best solution for your hospital
                </h1>
                <div class="button--area">
                    <vs-button
                        floating
                        large
                        class="btn"
                        gradient
                        @click="setDoctorLoginActive()"
                    >
                        Doctor login
                    </vs-button>

                    <login-dialog
                        :userType="'Doctor'"
                        :userLoginActive="this.$store.state.doctorLoginActive"
                    />

                    <vs-button
                        floating
                        large
                        class="btn"
                        gradient
                        @click="setPatientLoginActive()"
                    >
                        Patient login
                    </vs-button>

                    <login-dialog
                        :userType="'Patient'"
                        :userLoginActive="this.$store.state.patientLoginActive"
                    />

                    <vs-button
                        floating
                        large
                        class="btn"
                        gradient
                        @click="setHealthcareLoginActive()"
                    >
                        Healthcare worker login
                    </vs-button>

                    <login-dialog
                        :userType="'Healthcare worker'"
                        :userLoginActive="this.$store.state.healthcareLoginActive"
                    />
                </div>
            </div>

            <div class="column">
                <img
                    class="home--illustration"
                    src="@/assets/home-page.svg"
                    alt=""
                >
            </div>
        </div>

        <div class="row">
            <img
                class="home--wave"
                src="@/assets/wave.svg"
                alt=""
            >
        </div>
    </div>
</template>

<script>
import LoginDialog from './LoginDialog.vue';
import TopNavBar from '@/components/TopNavBar.vue';

export default {
    name: 'MainPage',
    
    components: {
        LoginDialog,
        TopNavBar,
    },

    methods: {
        async setDoctorLoginActive() {
            await this.$store.commit('SET_DOCTOR_LOGIN');
        },

        async setPatientLoginActive() {
            await this.$store.commit('SET_PATIENT_LOGIN');
        },

        async setHealthcareLoginActive() {
            await this.$store.commit('SET_HEALTHCARE_LOGIN');
        },
    }
}
</script>

<style scoped>
    .button--area {
        display: grid;
        margin: 0 auto;
    }

    .button--area .btn {
        margin-top: 1em;
        padding: 4px 16px;
        font-size: 14px;
        font-weight: 600;
    }

    .headline {
        margin: 0 auto;
        color:#272727;
        font-weight: bolder;
        font-size: 2em;
        padding-bottom: 1em;
    }

    .left--part {
        display: grid;
        margin-top: 10em;
        align-content: center;
        padding-left: 6em;
    }

    .home--illustration {
        align-content: center;
        margin-top: 10em;
        width: 90%;
    }

    .row {
        display: flex;
    }

    .column {
        flex: 50%;
    }

    .home--wave {
        position: absolute;
        top: 600px;
        left: 0;
    }

    @media only screen and (max-width: 1100px) {
        .home--illustration {
            display: none;
        }
    }
</style>
