<template>
  <div id="app">
    <top-nav-bar/>
    <main-page/>
  </div>
</template>

<script>
import TopNavBar from '@/components/TopNavBar.vue';
import MainPage from '@/views/mainPage/MainPage.vue';

export default {
  name: 'App',

  components: {
    TopNavBar,
    MainPage,
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
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
