<template>
  <div class="posts-grid">
    <PostCard 
      v-for="post in posts" 
      :key="post.hash" 
      :post="post">
    </PostCard>
  </div>
</template>

<script>
import PostCard from './PostCard'
import axios from 'axios'

export default {
  name: 'PostsContainer',
  components: {
    PostCard,
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
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  grid-auto-rows: minmax(100px, auto);
  gap: 20px;
  margin: auto;
  width: 70%;
  padding: 10px;
}

@media (max-width: 600px) {
  .posts-grid {
    width: 100%;
  }
}
</style>
