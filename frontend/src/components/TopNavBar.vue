<template>
  <div>
    <vs-navbar
      center-collapsed
      class="top__navbar"
    >
      <template #right>
        <vs-button 
          floating 
          @click="setAdminLoginActive()"
        >
          Administrator login
        </vs-button>
      </template>
    </vs-navbar>

    <login-dialog 
      :userType="'Administrator'"
      :userLoginActive="this.$store.state.adminLoginWindowActive"
    />
  </div>
</template>

<script>
import LoginDialog from '@/views/general/LoginDialog.vue';

export default {
  name: 'TopNavBar',    

  components: {
    LoginDialog,
  },

  methods: {
    async setAdminLoginActive() {
      await this.$store.commit('SET_ADMIN_LOGIN_WINDOW');
    }
  },
}
</script>

<style scoped>
    .top__navbar {
        padding: 2em;
        background-color: #fbfbfb;
    }
</style>