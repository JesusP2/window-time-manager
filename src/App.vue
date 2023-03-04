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
  <div class="max-w-lg w-full rounded-lg border-neutral-800 h-96 flex flex-col text-neutral-300 mx-auto border mt-4">
    <div class="h-8 bg-neutral-800 w-full pt-1 pl-4">ACTIVITY</div>
    <div class="w-full flex-1 bg-neutral-900"></div>
  </div>
</template>
