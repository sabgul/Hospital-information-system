<template>
  <div class="center examplex">
    <vs-navbar 
      center-collapsed
      class="top--navbar"
    >
      <template #left>
        <img 
          src="/logo2.png" 
          alt=""
        />
      </template>

      <template #right>
        <vs-button 
          floating 
          gradient
          @click="setAdminLoginActive()"
        >
          Administrator login
        </vs-button>
      </template>
    </vs-navbar>

    <login-dialog 
      :userType="'Administrator'"
      :userLoginActive="this.$store.state.adminLoginActive"    
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
      await this.$store.commit('SET_ADMIN_LOGIN');
    }
  },
}
</script>

<style scoped>
    .top--navbar {
        padding: 2em;
    }
</style>