<script setup>

import {onMounted, ref, watch} from "vue";

const props = defineProps({
    device: {
        type: Object,
        default: null,
    },
    size: {
        type: Number,
        default: 2
    }
})

watch(
  () => props.device?.temperatures,
  () => {
    generateLastTempEntryStatus()
  },
  { deep: true }
);

const lastTempEntryStatus = ref('bg-gray-500')

const generateLastTempEntryStatus = () => {

  if (props.device == null) {
      return
  }

  if (props.device != null && props.device.temperatures.length > 0) {
    let createdAt = new Date(props.device.temperatures[0].created_at)
    let timeDifferenceInSeconds = (Date.now() - createdAt) / 1000

    if (timeDifferenceInSeconds <= 120) {
      lastTempEntryStatus.value = 'bg-green-500'
    } else if (timeDifferenceInSeconds <= 300) {
      lastTempEntryStatus.value = 'bg-yellow-500'
    } else if (timeDifferenceInSeconds >= 300) {
      lastTempEntryStatus.value = 'bg-red-500'
    }
  } else {
    lastTempEntryStatus.value = 'bg-gray-500'
  }
}

onMounted(() => {
    generateLastTempEntryStatus()
})

</script>

<template>
  <div
      :class="`min-h-${size} min-w-${size} ${lastTempEntryStatus}`"
      class="rounded-full animate-pulse"
  />
</template>

<style scoped>

</style>