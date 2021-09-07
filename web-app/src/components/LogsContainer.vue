<template>
  <div>
    <template v-if="loadingLogs">
      Učitavanje logova...
    </template>
    <template v-else>
      <button 
        @click="getLogs('scraper')"
        class="tab-button"
        :style="{'background-color': activeTab === 'scraper' ? 'white' : 'gray'}">
        Logovi scrapera
      </button>
      <button 
        @click="getLogs('ner')"
        class="tab-button"
        :style="{'background-color': activeTab === 'ner' ? 'white' : 'gray'}">
        Logovi ner-a
      </button>     
      <br>
      <textarea class="logarea" v-model="textLogs" readonly>
      </textarea>
    </template>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      logs: [],
      loadingLogs: false,
      activeTab: 'scraper'
    }
  },
  async created() {
    await this.getLogs('scraper')
  },
  methods: {
    getLogs: async function(source) {
      this.activeTab = source
      this.loadingLogs = true;
      const res = await axios.get(`http://localhost:3000/get_logs?source=${source}`)
      console.log(`got ${source} logs`)
      if (res && res.data) {
        this.logs = res.data
      }
      this.loadingLogs = false;
    },
  },
  computed: {
    textLogs: function() {
      return this.logs.join('\n')
    }
  }
}
</script>

<style>
.main {
  margin-top: 200px;
}

.logarea {
  width: 100%;
  height: 600px;
}

.tab-button {
  margin-right: 2px;
  cursor: pointer;
}

.tab-button:hover {
  transform: scale(1.12);
}
</style>