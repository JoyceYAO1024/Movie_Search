<template>
  <div id="app" v-cloak>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
html,body {
  width: 100%;
  height: 100%;

}
#app {
  /* font-family: Inter,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif; */
  font: 1em Arial, Verdana, Arial, Helvetica, sans-serif;
  /* font-family: Roboto,Helvetica,Arial,sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #111;
  width: 100vw;
  height: 100vh;
}
[v-cloak] {
    display: none;
}
</style>
