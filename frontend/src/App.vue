<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { z } from "zod";
import { activeWindowSchema } from "./lib/schema";
import { formatTime } from "./lib/time-formatter";

type ActiveWindow = z.infer<typeof activeWindowSchema>;
const windows = ref<ActiveWindow[]>(
  localStorage.getItem("data") ? JSON.parse(localStorage.getItem("data")!) : []
);
// const windowsSorted = computed(() =>
//   [...windows.value].sort((a, b) => (a.time < b.time ? 1 : -1))
// );

const socket = new WebSocket("ws://localhost:8080");
socket.addEventListener("message", async ({ data }: MessageEvent<string>) => {
  const parsedData = activeWindowSchema.parse(JSON.parse(data));
  const idx = windows.value.findIndex((win) => win.title === parsedData.title);
  if (idx >= 0) {
    for (let i = 0; i < parsedData.time; i++) {
      windows.value[idx].time++;
      windows.value.sort((a, b) => (a.time < b.time ? 1 : -1))
      localStorage.setItem("data", JSON.stringify(windows));
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  } else {
    windows.value.push(parsedData);
    localStorage.setItem("data", JSON.stringify(windows));
  }
});
socket.addEventListener("error", async (error) => {
  console.error(error);
});
</script>

<template>
  <div
    class="max-w-2xl w-full rounded-lg border-neutral-800 h-96 flex flex-col text-neutral-300 mx-auto border mt-4"
  >
    <div class="h-8 bg-neutral-800 w-full pt-1 pl-4">ACTIVITY</div>
    <ul v-auto-animate class="w-full flex-1 bg-neutral-900 px-4 my-4 overflow-y-scroll">
      <li v-for="item of windows" class="flex" :key="item.title">
        <div class="w-24 truncate">{{ formatTime(item.time) }}</div>
        <div class="w-24 truncate">{{ item.app }}</div>
        <div class="max-w-[435px] truncate">{{ item.title }}</div>
      </li>
    </ul>
  </div>
</template>

<style>
#customers {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#customers td,
#customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#customers tr:nth-child(even) {
  background-color: #f2f2f2;
}

#customers tr:hover {
  background-color: #ddd;
}

#customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04aa6d;
  color: white;
}
</style>
