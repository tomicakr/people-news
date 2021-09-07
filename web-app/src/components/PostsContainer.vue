<template>
  <div class="posts-container">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <div class="navigation">
      <div 
        v-if="activeTab !== 'posts'"
        class="left-nav">
        <button class="nav-action" @click="onActivateTab('posts')">Postovi</button>
      </div>
      <div 
        v-if="activeTab === 'posts'"
        class="left-nav"
        :style="{visibility: activeTab === 'posts' ? 'visible' : 'hidden'}">
        <button 
          :style="{visibility: current !== 0 && activeTab === 'posts' ? 'visible' : 'hidden'}" 
          class="nav-button previous" 
          @click="getPage(current-1, selectedGroup)">
          <i class="fa fa-arrow-left"></i>
        </button>
        <button 
          :style="{visibility: isEnd || activeTab !== 'posts' ? 'hidden' : 'visible'}"
          class="nav-button next" 
          @click="getPage(current+1, selectedGroup)">
          <i class="fa fa-arrow-right"></i>
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
      </div>
      <div class="right-nav">
        <div class="action-buttons">
          <button 
            class="nav-action action-right" 
            :class="{active: activeTab === 'logs'}"
            @click="onActivateTab('logs')">
            Logovi</button>
          <button 
            class="nav-action action-right"
            :class="{active: activeTab === 'analytics'}"
            @click="onActivateTab('analytics')">
            Analitika</button>
          <button 
            class="nav-action action-right" 
            :class="{active: activeTab === 'config'}"
            @click="onActivateTab('config')">
            Konfiguracija</button>
        </div>
        <div class="status">
          <button 
            class="refresh-button" 
            @click="healthCheck()">
              <span v-if="isLoadingRefreshStatus">
                <img src="../assets/spinner.svg" class="spinner" :style="{padding: '',fill: 'black', width: '20px'}">
              </span>
              <span v-else>
                <i class="fa fa-refresh"></i>
              </span>
          </button>
          <div class="status-text">
            <div
              class="status-line"
              v-for="status,index in servicesStatus" 
              :key="index"
              :style="{'background-color': status.status ? 'green' : 'red'}">
              {{status.serviceName}}: {{status.status ? 'radi' : 'ne radi'}}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="content">
      <template v-if="activeTab === 'logs'">
        <LogsContainer />
      </template>
      <template v-else-if="activeTab === 'posts'">
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
      </template>
      <template v-if="activeTab === 'analytics'">
        <AnalyticsContainer :groups="groupNames"/>
      </template>
      <template v-if="activeTab === 'config'">
        <ConfigPortalContainer />
      </template>
    </div>
    
  </div>
</template>

<script>
import PostCard from './PostCard'
import LogsContainer from './LogsContainer.vue'
import AnalyticsContainer from './AnalyticsContainer.vue'
import ConfigPortalContainer from './ConfigPortalContainer.vue'
import axios from 'axios'

export default {
  name: 'PostsContainer',
  components: {
    PostCard,
    LogsContainer,
    AnalyticsContainer,
    ConfigPortalContainer
  },
  data() {
    return {
      posts: null,
      current: 0,
      isEnd: false,
      loadingPosts: false,
      selectedGroup: 'all',
      groupNames: null,
      servicesStatus: null,
      isLoadingRefreshStatus: false,
      activeTab: 'posts'
    }
  },
  async created() {
    this.healthCheck()
    this.getGroupNames()
    this.getPage.bind(this)(0, 'all')
  },
  methods: {
    async healthCheck() {
      this.isLoadingRefreshStatus = true;
      const res = await axios.get(`http://localhost:3000/health_check`)
      if (res && res.data) {
        this.servicesStatus = res.data
      }
      this.isLoadingRefreshStatus = false;
    },
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
      this.getPage(0, event.target.value)
    },
    onActivateTab(tab) {
      this.activeTab = tab
    }
  }
}
</script>

<style>
.posts-container {
  margin: auto;
  width: 80%;
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

.content { 
  margin-top: 6em;
}

.navigation {
  margin-bottom: 10px;
  display: flex;
  position: fixed;
  z-index: 10;
  top: 0;
  left: 0;
  background-color: #4f4a41;
  padding: 5px;
  width: 100%;
  justify-content: space-between;
}

.left-nav {
  display: flex;
  align-items: center;
  margin-left: 20px;
}

.right-nav {
  display: flex;
  margin-right: 20px;
  align-items: center;
}

.status {
  display: flex;
}

.action-buttons {
  display: flex;
  flex-direction: column;
}

.status-line {
  border-radius: 5px;
  border: 1px solid black;
  margin-top: 1px;
  padding-left: 5px;
  padding-right: 5px;
}

.nav-button {
  cursor: pointer;
  text-transform: uppercase;
  margin-right: 10px;
  padding-right: 10px;
  padding-left: 10px;
  border-radius: 15%;
  font-size: 20px;
  font-weight: 700;
  height: 60%;
}

.nav-action {
  cursor: pointer;
  text-transform: uppercase;
  margin-right: 5px;
  padding-right: 10px;
  padding-left: 10px;
  border-radius: 8%;
  font-size: 12px;
  font-weight: 500;
  height: 60%;
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
  font-size: 20px;
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
  width: 15em;
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

.refresh-button {
  cursor: pointer;
  text-transform: uppercase;
  margin-right: 10px;
  border-radius: 20%;
  font-size: 20px;
  font-weight: 700;
  height: 30px;
  stroke-width: 30px;
}

.action-right:hover {
  transform: translateX(-8px);
}

.active {
  background-color: orange;
  transform: translateX(-6px);
}
</style>
