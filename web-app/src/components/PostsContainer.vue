<template>
  <div class="posts-container">
    <div class="navigation-area">
      <button 
        :style="{visibility: current !== 0 ? 'visible' : 'hidden'}" 
        class="nav-button previous" 
        @click="getPage(current-1, selectedGroup)">
          nazad
      </button>
      <button 
        :style="{visibility: isEnd ? 'hidden' : 'visible'}"
        class="nav-button next" 
        @click="getPage(current+1, selectedGroup)">
          naprijed
      </button>
      <span 
        :style="{visibility: loadingPosts ? 'visible' : 'hidden'}"
        class="loader">
        <img src="../assets/spinner.svg" class="spinner">
      </span>
      <div class="select">
        <select v-model="selectedGroup" @change="onSelectChange($event)">
            <option value="all" selected>Svi postovi</option>
            <option v-for="name in groupNames" :key="name.groupName" :value="name.groupName">{{name.groupFullName}}</option>
        </select>
      </div>
      <div class="status">
        <span v-for="status,index in servicesStatus" :key="index">
          {{index+1}}.{{status.serviceName}}: {{status.status}}
        </span>
      </div>
    </div>
    
    <div v-if="posts.length" class="posts-grid">
      <PostCard 
        v-for="post in posts" 
        :key="post.hash" 
        :post="post">
      </PostCard>
    </div>
    <div class="nopost" v-else>
      Ne postoje postovi s tom grupom ljudi
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
      selectedGroup: 'all',
      groupNames: null,
      servicesStatus: null
    }
  },
  async created() {
    const res = await axios.get(`http://localhost:3000/health_check`)
    if (res && res.data) {
      this.servicesStatus = res.data
    }
    this.getGroupNames()
    this.getPage.bind(this)(0, 'all')
  },
  methods: {
    async getPage(page, group) {
      this.current = page
      this.loadingPosts = true
      const res = await axios.get(`http://localhost:3000/posts?start=${page*10}&count=10&group=${group}`)
      if (res && res.data) {
        this.posts = res.data
      }
      if (this.posts.length < 10) {
        this.isEnd = true
      } else {
        this.isEnd = false
      }
      this.loadingPosts = false
    },
    async getGroupNames() {
      const res = await axios.get(`http://localhost:3000/groupnames`)
      console.log(res.data)
      if (res && res.data) {
        this.groupNames = res.data
      }
    },
    onSelectChange(event) {
      this.getPage(0, event.target.value);
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
  background-color: #4f4a41;
  padding: 10px;
  width: 100%;
  justify-content: center;
}

.nav-button {
  cursor: pointer;
  text-transform: uppercase;
  margin-right: 10px;
  padding-right: 10px;
  padding-left: 10px;
  border-radius: 8%;
  font-size: 20px;
  font-weight: 700;
}

.loader {
  margin-right: 10px;
}

.spinner {
  width: 50px;
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

.selector {
  font-size: 30px;
  font-weight: 700;
}

/* Reset Select */
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  -ms-appearance: none;
  appearance: none;
  outline: 0;
  box-shadow: none;
  border: 0 !important;
  background: #31475d;
  background-image: none;
  font-size: 30px;
  font-weight: 600;
}
/* Remove IE arrow */
select::-ms-expand {
  display: none;
}
/* Custom Select */
.select {
  position: relative;
  display: flex;
  width: 20em;
  height: 3em;
  line-height: 3;
  background: #2c3e50;
  overflow: hidden;
  border-radius: .25em;
}
select {
  flex: 1;
  padding: 0 .5em;
  color: #fff;
  cursor: pointer;
}
/* Arrow */
.select::after {
  content: '\25BC';
  position: absolute;
  top: 0;
  right: 0;
  padding: 0 1em;
  background: #34495e;
  cursor: pointer;
  pointer-events: none;
  -webkit-transition: .25s all ease;
  -o-transition: .25s all ease;
  transition: .25s all ease;
  border-radius: 29%;
}
/* Transition */
.select:hover::after {
  color: #f39c12;
}

.nopost {
  padding-top: 30%;
  padding-left: 10%;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  font-size: 30px;
}

.status {
  margin-left: 20px;
  margin-top: 5px;
}
</style>
