<script setup lang="ts">

import AppLayout from "@/Layouts/AppLayout.vue";
import DangerButton from "@/Components/DangerButton.vue";
import ConfirmationModal from "@/Components/ConfirmationModal.vue";
import {ref} from "vue";
import PrimaryButton from "@/Components/PrimaryButton.vue";
import {Link, router, useForm} from "@inertiajs/vue3";
import TextInput from "@/Components/TextInput.vue";
import InputLabel from "@/Components/InputLabel.vue";
import InputError from "@/Components/InputError.vue";
import SecondaryButton from "@/Components/SecondaryButton.vue";
import FormSection from "@/Components/FormSection.vue";
import ActionMessage from "@/Components/ActionMessage.vue";

const props = defineProps({
    device: Object
})

const deleteModalActive = ref(false);

const toggleDeleteModal = () => {
    deleteModalActive.value = !deleteModalActive.value;
}

const deleteDevice = () => {
    router.delete(route('devices.destroy', props.device.id));
    deleteModalActive.value = false;
}

const form = useForm({
    name: props.device.name,
})

const updateProfileInformation = () => {
    form.put(route('devices.update', props.device.id))
}

</script>

<template>
  <AppLayout title="device.name">
    <template #header>
      <div class="w-full flex justify-between items-center">
        <h2 v-text="device.name" class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight" />

        <DangerButton @click="toggleDeleteModal()">
          Delete
        </DangerButton>

        <confirmation-modal :show="deleteModalActive" @close="toggleDeleteModal()">
          <template #title>
            Delete Device '{{ device.name }}'?
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
      </div>
    </template>

    <div class="py-12 text-gray-800 dark:text-gray-200">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <FormSection @submitted="updateProfileInformation()">
          <template #title>
            Device Information
          </template>

          <template #description>
            Update your devices' profile information and email address.
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