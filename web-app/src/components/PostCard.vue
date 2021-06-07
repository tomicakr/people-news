<template>
  <div class="post-card">
    <a class="full-link" :href="post.url"></a>
    <div class="post-title">{{post.title}}</div>
    <div class="post-summary">{{postSummary}}</div>
    <div class="post-date"><strong>Date:</strong> {{post.dateAdded}}</div>
    <div v-if="postNames.length" class="post-names"><strong>Mentions:</strong> {{postNames}}</div>
  </div>
</template>

<script>
import { summarize, concat } from '../util/textHelpers'

export default {
  name: 'PostCard',
  props: {
    post: Object,
  },
  data() {
    return {
      postSummary: '',
      postNames: ''
    }
  },
  created() {
    this.postSummary = summarize(this.post.text)
    this.postNames = concat(this.post.names)
  }
}
</script>

<style>
.post-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
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

.post-summary {
  margin-bottom: 10px;
}

.full-link {
  position: absolute;
  height: 100%;
  width: 100%;
  margin-left: -10px;
  margin-top: -10px;
}

.post-date {
  margin-bottom: 10px;
}
</style>
