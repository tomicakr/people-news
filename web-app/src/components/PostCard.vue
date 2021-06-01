<template>
  <div class="post-card">
    <div class="post-title">{{post.title}}</div>
    <div class="post-summary">{{post.text[0]}}</div>
    <div class="post-names">{{post.names}}</div>
  </div>
</template>

<script>
export default {
  name: 'PostCard',
  props: {
    post: Object,
  }
}
</script>

<style scoped>
.post-card {
  background-color: red;
  margin-bottom: 10px;
  border-radius: 10%;
}
</style>
