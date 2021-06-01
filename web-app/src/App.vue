<template>
  <div id="app">
    <PostCard 
      v-for="post in posts" 
      :key="post.hash" 
      :post="post">
    </PostCard>
  </div>
</template>

<script>
import PostCard from './components/PostCard'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    PostCard
  },
  data() {
    return {
      posts: null
    }
  },
  async created() {
    const res = await axios.get('http://localhost:3000/posts?count=10')
    if (res && res.data) {
      this.posts = res.data
    }
  }
}
</script>

<style>
</style>
