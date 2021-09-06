<template>
  <PostsContainer />
</template>

<script>
import PostsContainer from './components/PostsContainer.vue'

export default {
  name: 'App',
  components: {
    PostsContainer
  },
}
</script>

<style>
*{box-sizing: border-box;}

body {
  font-family: Georgia, serif;
  background-color: #88bdbc;
}
</style>
