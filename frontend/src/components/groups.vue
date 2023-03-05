<script setup lang="ts">
import { ref } from "vue";
const emit = defineEmits(["createGroup", "removeGroup"]);
const props = defineProps<{ groups: string[] }>();
const groupName = ref("");

function createGroup() {
  emit("createGroup", groupName.value);
  groupName.value = "";
}
</script>

<template>
  <input type="checkbox" id="my-modal" class="modal-toggle" />
  <div class="modal">
    <div class="modal-box max-w-xs">
      <h3 class="font-bold text-lg">Create new group</h3>
      <input
        type="text"
        class="input rounded-sm input-info w-full max-w-xs input-sm mt-4"
        v-model="groupName"
      />
      <div class="modal-action">
        <label for="my-modal" class="btn btn-sm btn-error btn-outline"
          >Close</label
        >
        <label @click="createGroup" for="my-modal" class="btn btn-sm btn-info"
          >Create</label
        >
      </div>
    </div>
  </div>

  <div
    class="max-w-xs w-full rounded-lg border-neutral-700 h-96 flex flex-col text-neutral-300 mx-auto border mt-4 bg-base-300"
  >
    <div class="h-8 bg-base-100 w-full pt-1 pl-4 rounded-t-lg">GROUPS</div>
    <ul
      v-auto-animate
      class="w-full flex-1 bg-base-300 px-4 my-4 overflow-y-scroll"
    >
      <li
        class="flex w-full justify-between hover:bg-base-100 px-4 py-1 rounded-full text-sm"
        v-for="group of props.groups"
        :key="group"
      >
        <p>{{ group }}</p>
        <button
          class="hover:text-red-500 text-red-900"
          @click="$emit('removeGroup', group)"
        >
          x
        </button>
      </li>
    </ul>
    <label for="my-modal" class="btn mx-auto">NEW GROUP</label>
  </div>
</template>
