<script setup>
import AppLayout from '@/Layouts/AppLayout.vue';
import DeviceData from "@/Pages/Dashboard/Partials/DeviceData.vue";
import {watch} from "vue";

const props = defineProps({
    devices: Array,
  selectedDeviceId: Number,
})

watch(
  () => props.devices[0]?.temperatures,
  (newTemps, oldTemps) => {
    console.log('Temperatures changed:', newTemps);
  },
  { deep: true }
);
</script>

<template>
  <AppLayout title="Dashboard">
    <template #header>
      <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
        Dashboard
      </h2>
    </template>

    <div class="py-12">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-gray-800 shadow-xl sm:rounded-lg">
          <DeviceData :devices="devices" :selected-device-id="selectedDeviceId" />
        </div>
      </div>
    </div>
  </AppLayout>
</template>
