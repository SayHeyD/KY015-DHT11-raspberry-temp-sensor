<script setup>
import {router, usePage} from '@inertiajs/vue3'
import {computed, nextTick, onBeforeMount, onMounted, onUnmounted, ref, watch} from "vue";
import Dropdown from "@/Components/Dropdown.vue";
import DropdownLink from "@/Components/DropdownLink.vue";
import { Line } from "vue-chartjs";
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement)

const page = usePage()

const props = defineProps({
    devices: Array,
    selectedDeviceId: Number
})

const overviewChartOptions = {
    responsive: true,
    interaction: {
        mode: 'index',
        intersect: false,
    },
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Overview'
        },
    },
    scales: {
        temperature: {
            title: {
                display: true,
                text: 'Temperature (°C)'
            },
            type: 'linear',
            display: true,
            position: 'left'
        },
        humidity: {
            title: {
                display: true,
                text: 'Humidity (%)'
            },
            type: 'linear',
            display: true,
            position: 'right',
            grid: {
                drawOnChartArea: false,
            },
        }
    }
}

let refreshInterval

const selectedDevice = ref(null)

const lastTempEntryStatus = ref('bg-gray-500')

const averageTemperature = ref(0)
const averageHumidity = ref(0)
const maxTemperature = ref(0)
const maxHumidity = ref(0)
const minTemperature = ref(0)
const minHumidity = ref(0)

const overviewChartData = computed(() => {
    let labels = []
    let temperatureDataSet = {
        label: 'Temperature (°C)',
        borderColor: 'rgb(255, 99, 132)', // red
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        yAxisID: 'temperature',
        data: []
    }
    let humidityDataSet = {
        label: 'Humidity (%)',
        borderColor: 'rgb(54, 162, 235)', // blue
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        yAxisID: 'humidity',
        data: []
    }

    selectedDevice.value.temperatures.forEach((tempEntry) => {
        labels.push(new Date(tempEntry.measured_at).toLocaleString())
        temperatureDataSet.data.unshift(tempEntry.temperature)
        humidityDataSet.data.unshift(tempEntry.humidity)
    })

    return {
        labels,
        datasets: [
            temperatureDataSet,
            humidityDataSet
        ],
    }
})

const generateAverageTemperature = () => {
    let totalTemperature = 0
    selectedDevice.value.temperatures.forEach((tempEntry) => {
        totalTemperature += tempEntry.temperature
    })

    averageTemperature.value = (totalTemperature / selectedDevice.value.temperatures.length).toFixed(2)
}

const generateAverageHumidity = () => {
    let totalHumidity = 0
    selectedDevice.value.temperatures.forEach((tempEntry) => {
        totalHumidity += tempEntry.humidity
    })

    averageHumidity.value = (totalHumidity / selectedDevice.value.temperatures.length).toFixed(2)
}

const generateMaxTemperature = () => {
    let calculatedMaxTemperature
    selectedDevice.value.temperatures.forEach((tempEntry) => {
        if (calculatedMaxTemperature == null || tempEntry.temperature > calculatedMaxTemperature) {
            calculatedMaxTemperature = tempEntry.temperature
        }
    })

    maxTemperature.value = calculatedMaxTemperature
}

const generateMaxHumidity = () => {
    let calculatedMaxHumidity
    selectedDevice.value.temperatures.forEach((tempEntry) => {
        if (calculatedMaxHumidity == null || tempEntry.humidity > calculatedMaxHumidity) {
            calculatedMaxHumidity = tempEntry.humidity
        }
    })

    maxHumidity.value = calculatedMaxHumidity
}

const generateMinTemperature = () => {
    let calculatedMinTemperature
    selectedDevice.value.temperatures.forEach((tempEntry) => {
        if (calculatedMinTemperature == null || tempEntry.temperature < calculatedMinTemperature) {
            calculatedMinTemperature = tempEntry.temperature
        }
    })

    minTemperature.value = calculatedMinTemperature
}

const generateMinHumidity = () => {
    let calculatedMinHumidity
    selectedDevice.value.temperatures.forEach((tempEntry) => {
        if (calculatedMinHumidity == null || tempEntry.humidity < calculatedMinHumidity) {
            calculatedMinHumidity = tempEntry.humidity
        }
    })

    minHumidity.value = calculatedMinHumidity
}

watch(props.devices, () => {
    dataUpdate()
})

const generateLastTempEntryStatus = () => {

    if (selectedDevice.value != null && selectedDevice.value.temperatures.length > 0) {
        let createdAt = new Date(selectedDevice.value.temperatures[0].created_at)
        let timeDifferenceInSeconds = (Date.now() - createdAt) / 1000

        if (timeDifferenceInSeconds <= 90) {
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

const setSelectedDevice = () => {
    if (props.devices.length === 0)
    {
        return
    }

    if (props.selectedDeviceId != null) {
        for (let i = 0; i++; i < props.devices.length) {
            if (props.devices[i].id == props.selectedDeviceId) {
                selectedDevice.value = props.devices[i]
            }
        }
    } else {
        selectedDevice.value = props.devices[0]
    }
}

const refreshTempEntries = () => {
    router.reload({
        only: ['devices'],
        data: {
            device: selectedDevice.value.id
        }
    })
    nextTick(() => {
        dataUpdate()
        console.log(props.devices[0].temperatures)
    })
}

const dataUpdate = () => {
    setSelectedDevice()
    generateLastTempEntryStatus()
    generateAverageTemperature()
    generateAverageHumidity()
    generateMaxTemperature()
    generateMaxHumidity()
    generateMinTemperature()
    generateMinHumidity()
}

onBeforeMount(() => {
    dataUpdate()
})

onMounted(() => {
    refreshInterval = setInterval(refreshTempEntries, 15000)
})

onUnmounted(() => {
    clearInterval(refreshInterval)
})
</script>

<template>
  <div class=" bg-white dark:bg-gray-800">
    <div class="flex justify-end items-center">
      <p class="text-gray-800 dark:text-gray-200">Device selection: </p>
      <Dropdown class="m-4"
                content-classes="py-1 bg-white dark:bg-gray-700 overflow-y-scroll max-h-96">
        <template #trigger>
          <span class="inline-flex rounded-md">
            <button type="button" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 hover:text-gray-700 dark:hover:text-gray-300 focus:outline-none focus:bg-gray-50 dark:focus:bg-gray-700 active:bg-gray-50 dark:active:bg-gray-700 transition ease-in-out duration-150">
              <span v-if="selectedDevice">{{ selectedDevice.name }}</span>
              <span v-else>No Device</span>

              <svg class="ms-2 -me-0.5 size-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
          </span>
        </template>

        <template #content>
          <div class="block px-4 py-2 text-xs text-gray-400">
            Choose the device of which you want to see the data
          </div>

          <DropdownLink v-if="devices.length > 0" v-for="dev in devices" @click="selectedDevice = dev">
            {{ dev.name }} <span v-if="selectedDevice.id === dev.id">(SELECTED)</span>
          </DropdownLink>
          <DropdownLink href="" v-else>
            <span>Create new device</span>
          </DropdownLink>
        </template>
      </Dropdown>
    </div>

    <div class="p-6">
      <h1 class="text-2xl font-medium text-gray-900 dark:text-white">
        <span v-if="selectedDevice">Data from {{ selectedDevice.name }}</span>
        <span v-else>No Data</span>
      </h1>

      <div v-if="selectedDevice" class="mt-4 text-gray-400">
          <div v-if="selectedDevice.temperatures.length > 0">
              <Line
                  :id="`${selectedDevice.id}-${selectedDevice.name}-overview-chart`"
                  :options="overviewChartOptions"
                  :data="overviewChartData"
              />
          </div>
          <div v-else>
              No data has been recorded from this device yet.
          </div>
      </div>
      <p v-else class="mt-6 text-gray-500 dark:text-gray-400 leading-relaxed">
        You have not selected a device. Please select a device or add a new device to
        the application to be able to see your data here.
      </p>
    </div>

    <div class="bg-gray-200 dark:bg-gray-800 bg-opacity-25 grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8 p-6 lg:p-8">
      <div>
        <div class="flex items-center">
          <div class="min-h-4 min-w-4 rounded-full animate-pulse"
                :class="lastTempEntryStatus"
          />
          <h2 class="ms-3 text-xl font-semibold text-gray-900 dark:text-white">
            Device Status
          </h2>
        </div>

        <div class="mt-4 text-gray-500 dark:text-gray-400 text-sm leading-relaxed">
            <div v-if="selectedDevice && selectedDevice.temperatures.length > 0">
                <p>Last temperature: <span v-text="selectedDevice.temperatures[0].temperature"/> °C</p>
                <p>Last humidity: <span v-text="selectedDevice.temperatures[0].humidity" /> %</p>
                <p>Last reading: <span v-text="new Date(selectedDevice.temperatures[0].created_at).toLocaleString()" /></p>
            </div>
            <div v-else>
                <p>No data found.</p>
            </div>
        </div>
      </div>

      <div>
        <div class="flex items-center">
          <svg class="size-6 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" fill="currentColor">
            <!--!Font Awesome Free 6.7.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
            <path d="M160 80c0-26.5 21.5-48 48-48l32 0c26.5 0 48 21.5 48 48l0 352c0 26.5-21.5 48-48 48l-32 0c-26.5 0-48-21.5-48-48l0-352zM0 272c0-26.5 21.5-48 48-48l32 0c26.5 0 48 21.5 48 48l0 160c0 26.5-21.5 48-48 48l-32 0c-26.5 0-48-21.5-48-48L0 272zM368 96l32 0c26.5 0 48 21.5 48 48l0 288c0 26.5-21.5 48-48 48l-32 0c-26.5 0-48-21.5-48-48l0-288c0-26.5 21.5-48 48-48z"/>
          </svg>
          <h2 class="ms-3 text-xl font-semibold text-gray-900 dark:text-white">
            Stats
          </h2>
        </div>

        <div class="mt-4 text-gray-500 dark:text-gray-400 text-sm leading-relaxed">
          <p>Average: <span v-text="averageTemperature"/> °C / <span v-text="averageHumidity"/> %</p>
          <p>Max: <span v-text="maxTemperature"/> °C / <span v-text="maxHumidity"/> %</p>
          <p>Min: <span v-text="minTemperature"/> °C / <span v-text="minHumidity"/> %</p>
        </div>
      </div>
    </div>
  </div>
</template>
