<script setup lang="ts">
import { ref, computed } from "vue";
import { z } from "zod";
import { activeWindowSchema } from "./lib/schema";
import { formatTime } from "./lib/time-formatter";
import Groups from "./components/groups.vue";

document.documentElement.setAttribute("data-theme", "dracula");

type ActiveWindow = z.infer<typeof activeWindowSchema>;
const windows = ref<ActiveWindow[]>(
  localStorage.getItem("data") ? JSON.parse(localStorage.getItem("data")!) : []
);
const groups = ref<string[]>(
  localStorage.getItem("groups")
    ? JSON.parse(localStorage.getItem("groups")!)
    : []
);

const groupedWindows = computed(() => {
  const data: { [K: string]: ActiveWindow } = {};
  windows.value.forEach((window) => {
    let isWindowGrouped = false;
    groups.value.forEach((group) => {
      const groupLE = group.toLowerCase();
      if (
        !window.title.toLowerCase().includes(groupLE) &&
        !window.app.toLowerCase().includes(groupLE)
      )
        return;
      isWindowGrouped = true;
      if (groupLE in data) {
        data[groupLE].time += window.time;
      } else {
        data[groupLE] = {
          ...window,
          title: groupLE,
        };
      }
    });
    if (!isWindowGrouped) {
      data[window.title] = window;
    }
  });

  return Object.values(data).sort((a, b) => (a.time < b.time ? 1 : -1));
});
const socket = new WebSocket("ws://localhost:8000/ws");
socket.addEventListener("message", async ({ data }: MessageEvent<string>) => {
  const parsedData = activeWindowSchema.parse(JSON.parse(data));
  const idx = windows.value.findIndex((win) => win.title === parsedData.title);
  if (idx >= 0) {
    windows.value[idx].time++;
    windows.value.sort((a, b) => (a.time < b.time ? 1 : -1));
    localStorage.setItem("data", JSON.stringify(windows.value));
  } else {
    windows.value.push(parsedData);
    localStorage.setItem("data", JSON.stringify(windows.value));
  }
});

socket.addEventListener("error", async (error) => {
  console.error(error);
});

function createGroup(name: string) {
  groups.value.push(name);
  localStorage.setItem("groups", JSON.stringify(groups.value));
}

function removeGroup(name: string) {
  groups.value = groups.value.filter((group) => group !== name);
  localStorage.setItem("groups", JSON.stringify(groups.value));
}
</script>

<template>
  <div
    class="max-w-2xl w-full rounded-lg border-neutral-700 h-96 flex flex-col text-neutral-300 mx-auto border mt-4 bg-base-300"
  >
    <div class="h-8 bg-base-100 w-full pt-1 pl-4 rounded-t-lg">ACTIVITY</div>
    <ul
      v-auto-animate
      class="w-full flex-1 bg-base-300 px-4 my-4 overflow-y-scroll"
    >
      <li
        v-for="item in groupedWindows"
        class="flex bg-base-300"
        :key="item.title"
      >
        <div class="w-24 truncate">{{ formatTime(item.time) }}</div>
        <div class="w-24 truncate">{{ item.app }}</div>
        <div class="max-w-[435px] truncate">{{ item.title }}</div>
      </li>
    </ul>
  </div>
  <Groups
    @remove-group="removeGroup"
    @create-group="createGroup"
    :groups="groups"
  />
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
