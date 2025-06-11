<script setup lang="ts">

import AppLayout from "@/Layouts/AppLayout.vue";
import DeviceList from "@/Pages/Device/Partials/DeviceList.vue";

defineProps({
    devices: Array
})
</script>

<template>
  <AppLayout title="Devices">
    <template #header>
      <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
        Devices
      </h2>
    </template>

    <div class="py-12 text-gray-800 dark:text-gray-200">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl sm:rounded-lg">
          <DeviceList :devices="devices" />
        </div>
      </div>
    </div>
  </AppLayout>
</template>