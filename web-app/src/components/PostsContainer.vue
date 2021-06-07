<template>
  <div class="posts-container">
    <div class="navigation-area">
      <button 
        :style="{visibility: current !== 0 ? 'visible' : 'hidden'}" 
        class="nav-button previous" 
        @click="getPage(current-1)">
          prev
      </button>
      <button 
        :style="{visibility: isEnd ? 'hidden' : 'visible'}"
        class="nav-button next" 
        @click="getPage(current+1)">
          next
      </button>
      <span 
        :style="{visibility: loadingPosts ? 'visible' : 'hidden'}">
          Loading posts...
      </span>
    </div>

    <div class="posts-grid">
      <PostCard 
        v-for="post in posts" 
        :key="post.hash" 
        :post="post">
      </PostCard>
    </div>
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
      posts: null,
      current: 0,
      isEnd: false,
      loadingPosts: false,
    }
  },
  async created() {
    this.getPage.bind(this)(0)
  },
  methods: {
    async getPage(page) {
      this.current = page
      this.loadingPosts = true
      const res = await axios.get(`http://localhost:3000/posts?start=${page*10}&count=10`)
      if (res && res.data) {
        this.posts = res.data
      }
      if (this.posts.length < 10) {
        this.isEnd = true
      } else {
        this.isEnd = false
      }
      this.loadingPosts = false
    }
  }
}
</script>

<style>
.posts-container {
  margin: auto;
  width: 70%;
  padding: 10px;
  margin: auto;
  width: 70%;
  padding: 10px;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  grid-auto-rows: minmax(100px, auto);
  gap: 20px;
  margin-top: 80px;
}

@media (max-width: 600px) {
  .posts-container {
    width: 95%;
  }
}

.navigation-area {
  margin-bottom: 10px;
  display: flex;
  position: fixed;
  z-index: 10;
  top: 0;
  left: 0;
  background-color: green;
  padding: 20px;
  width: 100%;
  justify-content: center;
}

.nav-button {
  cursor: pointer;
  text-transform: uppercase;
  margin-right: 10px;
  padding-right: 10px;
  padding-left: 10px;
  border-radius: 11%;
}

.nav-button:hover {
  background-color: green;
}

.previous:hover {
  transform: translateX(-2px);
}

.next:hover {
  transform: translateX(2px);
}
</style>
