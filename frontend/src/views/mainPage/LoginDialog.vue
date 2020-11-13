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
<!-- alternatively   @submit.prevent="login"-->
      <div class="con-form">
        <vs-input
            class="con-form-item"
            v-model="user_email"
            label-placeholder="Email"
        >
          <template
              v-if="validEmail"
              #message-success
          >
            Valid email
          </template>

          <template
              v-if="!validEmail && user_email !== ''"
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
            v-model="user_password"
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

      <div class="form-control">
        <vs-button type="submit" class="footer-dialog">Login</vs-button>
      </div>

<!--      could not get 2 templates into a single form -->
<!--      <template #footer>-->
<!--        <div class="footer-dialog">-->
<!--          <vs-button-->
<!--              block-->
<!--              -->
<!--          >-->
<!--            Sign In-->
<!--          </vs-button>-->
<!--        </div>-->
<!--      </template>-->

         </form>
<!--    login -->
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
    user_email: '',
    user_password: '',
  }),

  computed: {
    validEmail() {
      return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.user_email)
    }
  },

  methods: {
    async loginDialogClosed() {
      if (this.userType === 'Administrator') {
        await this.$store.commit('SET_ADMIN_LOGIN');
      }

      if (this.userType === 'Doctor') {
        await this.$store.commit('SET_DOCTOR_LOGIN');
      }

      if (this.userType === 'Patient') {
        await this.$store.commit('SET_PATIENT_LOGIN');
      }

      if (this.userType === 'Healthcare worker') {
        await this.$store.commit('SET_HEALTHCARE_LOGIN');
      }
    },

    login() {
      console.log('login() ', this.user_email, this.user_password);

      this.$store.dispatch('retrieveToken', {
        username: this.user_email,
        password: this.user_password,
      })
      .then(() => {
          this.$router.push('patients')
        })
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
