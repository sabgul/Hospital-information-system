<template>
  <div id="app">
    <patients-overview/>
  </div>
</template>

<script>
// import TopNavBar from '@/components/TopNavBar.vue';
// import MainPage from '@/views/mainPage/MainPage.vue';
import PatientsOverview from '@/views/patientsOverview/PatientsOverview.vue';

export default {
  name: 'App',

  components: {
    PatientsOverview,
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

html, body {
  font-family: 'Roboto', sans-serif;
}

#app {
  background-color: #fafafa;
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
