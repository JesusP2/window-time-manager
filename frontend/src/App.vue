<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { z } from "zod";
import { sessionSchema, windowSchema } from "./lib/schema";
import type { STATE } from "./lib/schema";
import { formatTime } from "./lib/time-formatter";
import Groups from "./components/groups.vue";

document.documentElement.setAttribute("data-theme", "dracula");

const state = ref<STATE>("Inactive");

type ActiveWindow = z.infer<typeof windowSchema>;
type Session = z.infer<typeof sessionSchema>;
const session = ref<Session>({
  id: "0",
  name: "",
  start: 0,
  end: 0,
  duration: 0,
  windows: [],
});

const groups = ref<string[]>(
  localStorage.getItem("groups")
    ? JSON.parse(localStorage.getItem("groups")!)
    : []
);

const groupedWindows = computed(() => {
  const data: { [K: string]: ActiveWindow } = {};
  session.value.windows.forEach((window) => {
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
const timeout = ref<any>(null);
const socket = new WebSocket("ws://localhost:8000/ws");

socket.addEventListener("message", async ({ data }: MessageEvent<string>) => {
  const parsedData = JSON.parse(data);
  switch (parsedData.STATE) {
    case "START SESSION":
      session.value = parsedData.payload;
      break;
    case "FINISH SESSION":
      session.value.windows = [];
      break;
    case "DATA":
      const idx = session.value.windows.findIndex(
        (win) => win.title === parsedData.payload.title
      );
      if (idx >= 0) {
        session.value.windows[idx].time++;
        session.value.windows.sort((a, b) => (a.time < b.time ? 1 : -1));
      } else {
        session.value.windows.push(parsedData.payload);
      }
      break;
  }
});
socket.addEventListener("error", async (error) => {
  console.error(error);
});

function createGroup(name: string) {
  groups.value.push(name);
}

function removeGroup(name: string) {
  groups.value = groups.value.filter((group) => group !== name);
}

function changeState() {
  switch (state.value) {
    case "Active":
      if (timeout.value !== null) {
        clearInterval(timeout.value);
      }
      socket.send("FINISH SESSION");
      state.value = "Inactive";
      break;
    case "Inactive":
      timeout.value = setInterval(() => {
        socket.send("DATA");
      }, 1000);
      socket.send("START SESSION");
      state.value = "Active";
      break;
  }
}

function pauseState() {
  socket.send("PAUSED")
  state.value = "Paused"
}
</script>

<template>
  <button class="btn" @click="changeState">
    {{ state === "Active" ? "Finish session" : "Start session" }}
  </button>
  <!-- <button -->
  <!--   class="btn" -->
  <!--   v-if="state === 'Active'" -->
  <!--   @click="pauseState" -->
  <!-- > -->
  <!--   Pause -->
  <!-- </button> -->
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
