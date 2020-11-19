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
            v-model="username"
            label-placeholder="Username"
        >

          <template #icon>
            <box-icon name='user'></box-icon>
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
      <span v-if="invalid_credentials">Wrong credentials.</span>
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
    username: '',
    password: '',
    invalid_credentials: false,
  }),

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
      console.log(`login() "${this.username}" "${this.password}"`);
      if (!this.username.length || !this.password.length) {
        console.log('empty');
        return;
      }

      this.$store.dispatch('loginUser', {
        username: this.username,
        password: this.password
      })
          .then(() => {
            console.log('success')
            this.invalid_credentials = false
            this.$router.push('patients')
          })
          .catch(err => {
            console.log(err)
            this.invalid_credentials = true
          })
    },
    register() {
      this.$store.dispatch('registerUser', {
        name: this.name,
        email: this.email,
        username: this.username,
        password: this.password,
        confirm: this.confirm
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
