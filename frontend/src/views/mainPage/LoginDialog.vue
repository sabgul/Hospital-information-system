<template>
    <vs-dialog 
        v-model="userLoginActive"
        @close="loginDialogClosed()"
    >
        <template #header>
            <h4 class="not-margin">
                Login as <b>{{ userType }}</b> 
            </h4>
        </template>

        <div class="con-form">
            <vs-input 
                class="con-form-item" 
                v-model="xxx" 
                label-placeholder="Email"
            >
                <template
                    v-if="validEmail"
                    #message-success
                >
                    Valid email
                </template>

                <template
                    v-if="!validEmail && xxx !== ''"
                    #message-danger
                >
                    Invalid email
                </template>

                <template #icon>
                    @
                </template>
            </vs-input>

            <vs-input 
                class="con-form-item" 
                type="password" 
                :visiblePassword="hasVisiblePassword"
                v-model="xxx2" 
                label-placeholder="Password"
                @click-icon="hasVisiblePassword = !hasVisiblePassword">
            >   
                <template #icon>
                    <i 
                        v-if="!hasVisiblePassword"
                        class="material-icons"
                    >
                        search
                    </i>

                    <i 
                        v-else
                        class="material-icons"
                    >
                        remove_red_eye
                    </i>
                </template>
            </vs-input>
        </div>

        <template #footer>
            <div class="footer-dialog">
                <vs-button
                    block
                    @click="testt"
                >
                    Sign In
                </vs-button>
            </div>
        </template>
    </vs-dialog>
</template>

<script>
export default {
    name: 'LoginDialog',    

    props: {
        userType: String,
        userLoginActive: Boolean,
    },

    data: () => ({
        hasVisiblePassword: false,
        xxx: '',
        xxx2: '',
    }),

    computed: {
        validEmail() {
          return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.xxx)
        }
    },

    methods: {
        async loginDialogClosed() {
            if(this.userType === 'Administrator') {
                await this.$store.commit('SET_ADMIN_LOGIN');
            }

            if(this.userType === 'Doctor') {
                await this.$store.commit('SET_DOCTOR_LOGIN');
            }

            if(this.userType === 'Patient') {
                await this.$store.commit('SET_PATIENT_LOGIN');
            }

            if(this.userType === 'Healthcare worker') {
                await this.$store.commit('SET_HEALTHCARE_LOGIN');
            }
        },

        testt() {
            this.$router.push('patients');
        }
    }
}
</script>
<style scoped>
    .con-form-item {
        padding-bottom: 24px;
        padding-left: 20%;
    }
</style>