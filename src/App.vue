<script setup lang="ts">
const socket = new WebSocket("ws://localhost:8080");
socket.addEventListener("message", async ({ data }: MessageEvent<string>) => {
  console.log(data);
});
socket.addEventListener("error", async (error) => {
  console.error(error);
});
</script>
<template>
  <div>hello</div>
</template>
