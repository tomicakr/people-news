<template>
  <div class="post-card">
    <a class="full-link" :href="post.url"></a>
    <div class="post-title">{{post.title}}</div>
    <div class="post-summary">{{postSummary}}</div>
    <!-- <div class="post-names">{{post.names}}</div> -->
  </div>
</template>

<script>
import { summarize } from '../util/textHelpers'

export default {
  name: 'PostCard',
  props: {
    post: Object,
  },
  data() {
    return {
      postSummary: ''
    }
  },
  created() {
    this.postSummary = summarize(this.post.text)
  }
}
</script>

<style>
.post-card {
  position: relative;
  background: lightgreen;
  border-radius: 10px;
  padding: 10px;
  transition: transform .2s;
}

.post-card:hover {
  transform: scale(1.05);
}

.post-title {
  margin-bottom: 20px;
  size: 10px;
  font-weight: 600;
  font-size: 20px;
}
.full-link {
  position: absolute;
  height: 100%;
  width: 100%;
  margin-left: -10px;
  margin-top: -10px;
}
</style>
