<script setup lang="ts">

import AppLayout from "@/Layouts/AppLayout.vue";
import PrimaryButton from "@/Components/PrimaryButton.vue";
import {useForm} from "@inertiajs/vue3";
import TextInput from "@/Components/TextInput.vue";
import InputLabel from "@/Components/InputLabel.vue";
import InputError from "@/Components/InputError.vue";
import FormSection from "@/Components/FormSection.vue";
import ActionMessage from "@/Components/ActionMessage.vue";

const form = useForm({
    name: null,
})

const storeDevice = () => {
    form.post(route('devices.store'))
}

</script>

<template>
  <AppLayout title="device.name">
    <template #header>
      <div class="w-full flex justify-between items-center">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
          New Device
        </h2>
      </div>
    </template>

    <div class="py-12 text-gray-800 dark:text-gray-200">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <FormSection @submitted="storeDevice()">
          <template #title>
            Device Information
          </template>

          <template #description>
            Your devices' profile information.
          </template>

          <template #form>
            <!-- Name -->
            <div class="col-span-6 sm:col-span-4">
              <InputLabel for="name" value="Name" />
              <TextInput
                  id="name"
                  v-model="form.name"
                  type="text"
                  class="mt-1 block w-full"
                  required
                  autocomplete="name"
              />
              <InputError :message="form.errors.name" class="mt-2" />
            </div>
          </template>

          <template #actions>
            <ActionMessage :on="form.recentlySuccessful" class="me-3">
              Saved.
            </ActionMessage>

            <PrimaryButton :class="{ 'opacity-25': form.processing }" :disabled="form.processing">
              Save
            </PrimaryButton>
          </template>
        </FormSection>
      </div>
    </div>

  </AppLayout>
</template>