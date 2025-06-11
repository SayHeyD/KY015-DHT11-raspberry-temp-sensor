<script setup lang="ts">

import PrimaryButton from "@/Components/PrimaryButton.vue";
import DangerButton from "@/Components/DangerButton.vue";
import {ref} from "vue";
import ConfirmationModal from "@/Components/ConfirmationModal.vue";
import {router} from "@inertiajs/vue3";

defineProps({
    devices: Array
})

const deviceToDelete = ref(null);
const deleteModalActive = ref(false);

const showDeleteModal = (device) => {
    deviceToDelete.value = device;
    deleteModalActive.value = !deleteModalActive.value;
}

const deleteDevice = () => {
    router.delete(route('devices.destroy', deviceToDelete.value.id));
    deleteModalActive.value = false;
}
</script>

<template>
  <div :key="device.id" class="flex items-center justify-between p-4 w-full" v-for="device in devices">
    <p v-text="device.name" />
    <div class="flex justify-around items-center">
      <PrimaryButton class="mx-2" :href="route('devices.show', device.id)">
        Show
      </PrimaryButton>
      <DangerButton class="mx-2" @click="showDeleteModal(device)">
        Delete
      </DangerButton>
    </div>
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