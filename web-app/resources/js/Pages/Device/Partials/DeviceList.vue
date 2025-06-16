<script setup lang="ts">

import PrimaryButton from "@/Components/PrimaryButton.vue";
import DangerButton from "@/Components/DangerButton.vue";
import {onMounted, onUnmounted, ref} from "vue";
import ConfirmationModal from "@/Components/ConfirmationModal.vue";
import {router} from "@inertiajs/vue3";
import DeviceStatus from "@/Components/DeviceStatus.vue";

defineProps({
    devices: Array
})

const deviceToDelete = ref(null);
const deleteModalActive = ref(false);

let refreshInterval

const showDeleteModal = (device) => {
    deviceToDelete.value = device;
    deleteModalActive.value = !deleteModalActive.value;
}

const deleteDevice = () => {
    router.delete(route('devices.destroy', deviceToDelete.value.id));
    deleteModalActive.value = false;
}

onMounted(() => {
    refreshInterval = setInterval(() => {
        router.reload({
            only: [
                'devices'
            ]
        })
    }, 1000 * 30)
})

onUnmounted(() => {
    clearInterval(refreshInterval)
})
</script>

<template>
  <div v-if="devices.length > 0" :key="device.id" v-for="device in devices" class="bg-white dark:bg-gray-800 flex items-center justify-between p-4 w-full my-4 shadow-xl sm:rounded-lg">
    <div class="flex justify-start items-center">
      <DeviceStatus :device="device" :size="2" class="mr-4" />
      <p v-text="device.name" />
    </div>
    <div class="flex justify-around items-center">
      <PrimaryButton class="mx-2" :href="route('devices.show', device.id)">
        Show
      </PrimaryButton>
      <DangerButton class="mx-2" @click="showDeleteModal(device)">
        Delete
      </DangerButton>
    </div>
  </div>
  <div v-else>
    <p>No devices found</p>
  </div>

  <confirmation-modal :show="deleteModalActive" @close="deleteModalActive = false">
    <template #title>
      Delete Device '{{ deviceToDelete.name }}'?
    </template>

    <template #content>
      If you delete the device all data belonging to it will be lost permanently and the API keys will stop working!
    </template>

    <template #footer>
      <PrimaryButton class="mx-2" @click="deleteModalActive = false">
        Cancel
      </PrimaryButton>
      <DangerButton class="mx-2" @click="deleteDevice()">
        Delete Permanently
      </DangerButton>
    </template>
  </confirmation-modal>
</template>