<script setup lang="ts">

import AppLayout from "@/Layouts/AppLayout.vue";
import DeviceList from "@/Pages/Device/Partials/DeviceList.vue";
import PrimaryButton from "@/Components/PrimaryButton.vue";

defineProps({
    devices: Array
})
</script>

<template>
  <AppLayout title="Devices">
    <template #header>
      <div class="w-full flex justify-between items-center">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
          Devices
        </h2>

        <PrimaryButton :href="route('devices.create')">
          New Device
        </PrimaryButton>
      </div>
    </template>

    <div class="py-12 text-gray-800 dark:text-gray-200">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="overflow-hidden">
          <DeviceList :devices="devices" />
        </div>
      </div>
    </div>
  </AppLayout>
</template>