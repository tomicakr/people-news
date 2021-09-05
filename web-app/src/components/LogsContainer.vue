<template>
  <div>
    <div v-for="log, index in logs" :key="index">
      <div>
        {{ log }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      logs: []
    }
  },
  async created() {
    const res = await axios.get(`http://localhost:3000/get_logs`)
    if (res && res.data) {
      this.logs = res.data
    }
  }
}
</script>

<style>

</style>