<template>
  <div id="app">
    {{posts}}
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  components: {
  },
  data() {
    return {
      posts: null
    }
  },
  async created() {
    const res = await axios.get('http://localhost:5000/posts?count=10')
    if (res && res.data) {
      this.posts = res.data
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
