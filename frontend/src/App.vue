<template>
  <div id="app">
    <div class="hidden" v-if="this.$route.path !== '/'">
      <vs-sidebar
      absolute
      v-model="active"
      open
      >
        <template #logo>
            <img src="./assets/hospital-logo.png" alt="Hospital logo">
        </template>

        <vs-sidebar-item id="home">
            <template #icon>
              <i class='bx bx-home'></i>
            </template>
            <router-link to="/">Home</router-link>
        </vs-sidebar-item>

        <vs-sidebar-item id="market">
            <template #icon>
              <i class='bx bx-grid-alt'></i>
            </template>
            <router-link to="/patients">Patients</router-link>
        </vs-sidebar-item>

        <vs-sidebar-item id="market">
            <template #icon>
              <i class='bx bx-grid-alt'></i>
            </template>
            <router-link to="/patientAdd">Add patient</router-link>
        </vs-sidebar-item>

        <template #footer>
            <vs-row justify="space-between">  
              <vs-avatar>
                  <img src="/avatars/avatar-5.png" alt="">
              </vs-avatar>

              <vs-avatar badge-color="danger" badge-position="top-right">
                  <i class='bx bx-bell' ></i>

                  <template #badge>
                  28
                  </template>
              </vs-avatar>
            </vs-row>
        </template>
      </vs-sidebar>
    </div>

    <div>
      <router-view class="content"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',

  components: {
  },

  data:() => ({
    active: 'home',
  }),
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

html, body {
  font-family: 'Roboto', sans-serif;
  height: 100%;
}

body {
  overflow: hidden;
}

.content {
  max-height: 100vh;
}

#app {
  background-color: #fff;
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
