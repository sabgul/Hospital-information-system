<template>
    <div class="main__page">
        <top-nav-bar/>

        <div class="row">
            <div class="column left__part">
                <h1 class="headline">
                    HospitalIS - the best solution for your hospital
                </h1>

                <div class="button__area">
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
                        :userLoginActive="this.$store.state.doctorLoginWindowActive"
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
                        :userLoginActive="this.$store.state.patientLoginWindowActive"
                    />

                    <vs-button
                        floating
                        large
                        class="btn"
                        gradient
                        @click="setHealthcareLoginActive()"
                    >
                        Insurance worker login
                    </vs-button>

                    <login-dialog
                        :userType="'Healthcare worker'"
                        :userLoginActive="this.$store.state.healthcareLoginWindowActive"
                    />
                </div>
            </div>

            <div class="column">
                <img
                    class="home__illustration"
                    src="@/assets/home-page.svg"
                    alt=""
                >
            </div>
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
            await this.$store.commit('SET_DOCTOR_LOGIN_WINDOW');
        },

        async setPatientLoginActive() {
            await this.$store.commit('SET_PATIENT_LOGIN_WINDOW');
        },

        async setHealthcareLoginActive() {
            await this.$store.commit('SET_HEALTHCARE_LOGIN_WINDOWm  ');
        },
    }
}
</script>

<style scoped>
    .main__page {
        overflow: hidden;
        background-image: url("../../assets/wave.svg");
        background-repeat: no-repeat;
        background-position: bottom;
        height: 100vh;
    }

    .button__area {
        display: grid;
        margin: 0 auto;
    }

    .button__area .btn {
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

    .left__part {
        display: grid;
        margin-top: 10em;
        align-content: center;
        text-align: center;
        padding-left: 6em;
    }

    .home__illustration {
        align-content: center;
        margin-top: 10em;
        width: 90%;
    }

    .row {
        /*display: flex;*/
    }

    .column {
        flex: 50%;
    }

    .home__wave {
        position: absolute;
        top: 70%;
        left: 0;
    }

    @media only screen and (max-width: 1100px) {
        .home__illustration {
            display: none;
        }

        .home__wave {
            display: none;
        }

        .left__part {
            margin: 20% 20% 20% 10%;
        }
    }
</style>
