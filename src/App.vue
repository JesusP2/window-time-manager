<script setup lang="ts">
import { reactive } from "vue";
import { z } from "zod";
import { activeWindowSchema } from "./lib/schema";

type ActiveWindow = z.infer<typeof activeWindowSchema>;
const windows = reactive<ActiveWindow[]>([]);

const socket = new WebSocket("ws://localhost:8080");
socket.addEventListener("message", async ({ data }: MessageEvent<string>) => {
  const parsedData = activeWindowSchema.parse(JSON.parse(data));
  const idx = windows.findIndex((window) => window.app === parsedData.app);
  if (idx >= 0) {
    windows[idx].time += parsedData.time;
  } else {
    windows.push(parsedData);
  }
});
socket.addEventListener("error", async (error) => {
  console.error(error);
});
</script>

<template>
  <div
    class="max-w-lg w-full rounded-lg border-neutral-800 h-96 flex flex-col text-neutral-300 mx-auto border mt-4"
  >
    <div class="h-8 bg-neutral-800 w-full pt-1 pl-4">ACTIVITY</div>
    <div class="w-full flex-1 bg-neutral-900">
      <table>
        <tr v-for="item of windows">
          <td>{{ item.time }}</td>
          <td>{{ item.app }}</td>
          <td>{{ item.title }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>
