<template>
  <div class="main">
    <template v-if="loadingLogs">
      Loading logs...
    </template>
    <template v-else>
      <button @click="getLogs">refresh</button>
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
      loadingLogs: false
    }
  },
  async created() {
    await this.getLogs()
  },
  methods: {
    getLogs: async function() {
      this.loadingLogs = true;
      const res = await axios.get(`http://localhost:3000/get_logs`)
      console.log('got logs')
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
</style>