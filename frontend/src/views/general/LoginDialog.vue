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

    <form action="#" v-on:submit.prevent="login">
      <div class="con-form">
        <vs-input
            class="con-form-item"
            v-model="email"
            label-placeholder="Email"
            ref="email_field"
        >

          <template #icon>
           <box-icon name="user"></box-icon>
          </template>
        </vs-input>

        <vs-input
            class="con-form-item"
            type="password"
            :visiblePassword="hasVisiblePassword"
            v-model="password"
            label-placeholder="Password"
            @click-icon="hasVisiblePassword = !hasVisiblePassword">
          >
          <template #icon>
            <box-icon v-if="!hasVisiblePassword" name="hide"></box-icon>
            <box-icon v-else name="show"></box-icon>
          </template>
        </vs-input>
      </div>

      <!-- could not get 2 templates into a single form -->
      <!--       <template #footer>-->
      <div class="footer-dialog">
        <vs-button
            type="submit"
            block

        >
          Sign In
        </vs-button>
      </div>
      <!--      <span v-if="credentials_invalid">Wrong credentials</span>-->
      <span v-if="response_code"><br>
        Response code: {{ this.response_code || null }} <br>
        Response detail: {{ this.response_string || null }}
      </span>
      <!--       </template>-->

    </form>
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
    email: '',
    password: '',
    credentials_invalid: false,
    response_code: null,
    response_string: null,
  }),

  computed: {
    validEmail() {
      return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.xxx)
    }
  },

  methods: {
    async loginDialogClosed() {
      if (this.userType === 'Administrator') {
        await this.$store.commit('SET_ADMIN_LOGIN_WINDOW');
      }

      if (this.userType === 'Doctor') {
        await this.$store.commit('SET_DOCTOR_LOGIN_WINDOW');
      }

      if (this.userType === 'Patient') {
        await this.$store.commit('SET_PATIENT_LOGIN_WINDOW');
      }

      if (this.userType === 'Healthcare worker') {
        await this.$store.commit('SET_HEALTHCARE_LOGIN_WINDOW');
      }
    },

    login() {
      if (!this.email.length || !this.password.length) {
        return;
      }

      let login_role;
      if (this.$store.state.patientLoginWindowActive)
        login_role = 'patient';
      else if (this.$store.state.doctorLoginWindowActive)
        login_role = 'doctor';
      else if (this.$store.state.healthcareLoginWindowActive)
        login_role = 'healthcare-worker';
      else if (this.$store.state.adminLoginWindowActive)
        login_role = 'admin';
      else {
        console.log('invalid login role');
        return;
      }

      this.$store.dispatch('loginUser', {
        email: this.email,
        password: this.password,
        role: login_role,
      })
          .then(() => {
            this.credentials_invalid = false;

            if(login_role === 'patient') {
              this.$router.push('my-health-report-card');
            }
            if(login_role === 'doctor') {
              this.$router.push('health-concerns');
            }
            if(login_role === 'healthcare-worker') {
              this.$router.push('examination-actions-overview');
            }
            if(login_role === 'admin') {
              this.$router.push('users-overview');
            }

            this.loginDialogClosed();
          })
          .catch(err => {
            console.log(err);
            this.credentials_invalid = true;

            // no response if BE is not running
            if (err.response) {
              if (err.response.data) {
                this.response_string = err.response.data.detail;
              }
              this.response_code = err.response.status;
            } else {
              this.response_string = 'No response from server';
              this.response_code = '-';
            }
          })
    },
    register() {
      this.$store.dispatch('registerUser', {
        name: this.name,
        email: this.email,
        password: this.password,
        // confirm: this.confirm  // manually verify matching passwords?
      })
    },

  },
}
</script>

<style scoped>
    .con-form-item {
      padding-bottom: 24px;
      padding-left: 20%;
    }
</style>
