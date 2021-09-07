<template>
  <div>
    <template v-if="loading">
      Učitavanje analitike...
    </template>
    <template v-else>
      <input v-model.number="days" type="number">
      <button @click="getAnalytics(days)">Posljednjih {{days}} dana</button>
      <Bar :labels="labels" :counts="counts"/>
    </template>
  </div>
</template>

<script>
import axios from 'axios';
import Bar from './Bar.vue'

export default {
  components: {
    Bar
  },
  props: {
    groups: Array,
  },
  data() {
    return {
      logs: [],
      labels: [],
      counts: [],
      loading: false,
      days: 7
    }
  },
  async created() {
    await this.getAnalytics(7)
  },
  methods: {
    getAnalytics: async function(days) {
      this.loading = true
      this.logs = []
      this.labels = []
      this.counts = []
      for (const group of this.groups) {
        const groupName = group.groupName
        const res = await axios.get(`http://localhost:3000/analytics?group=${groupName}&days=${days}`)
        console.log(`got ${groupName} analytics`)
        if (res && res.data) {
          this.logs.push(res.data)
        }
      }
      for (const log of this.logs) {
        const name = log.groupName
        const count = log.fromGroupCount
        this.labels.push(name)
        this.counts.push(count)
      }
      this.loading = false
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