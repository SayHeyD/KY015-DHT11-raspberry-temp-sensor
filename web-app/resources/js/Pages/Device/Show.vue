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
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl sm:rounded-lg p-4">
          <div class="w-1/2">
            <InputLabel class="w-full">
              Name
            </InputLabel>
            <TextInput class="w-full" v-model="form.name" />
            <InputError class="w-full" :message="form.errors.name" />
          </div>

          <PrimaryButton>
            Save
          </PrimaryButton>

          <FormSection @submitted="updateProfileInformation">
            <template #title>
              Device Information
            </template>

            <template #description>
              Update your devices' profile information and email address.
            </template>

            <template #form>
              <!-- Profile Photo -->
              <div v-if="$page.props.jetstream.managesProfilePhotos" class="col-span-6 sm:col-span-4">
                <!-- Profile Photo File Input -->
                <input
                    id="photo"
                    ref="photoInput"
                    type="file"
                    class="hidden"
                    @change="updatePhotoPreview"
                >

                <InputLabel for="photo" value="Photo" />

                <!-- Current Profile Photo -->
                <div v-show="! photoPreview" class="mt-2">
                  <img :src="user.profile_photo_url" :alt="user.name" class="rounded-full size-20 object-cover">
                </div>

                <!-- New Profile Photo Preview -->
                <div v-show="photoPreview" class="mt-2">
                    <span
                        class="block rounded-full size-20 bg-cover bg-no-repeat bg-center"
                        :style="'background-image: url(\'' + photoPreview + '\');'"
                    />
                </div>

                <SecondaryButton class="mt-2 me-2" type="button" @click.prevent="selectNewPhoto">
                  Select A New Photo
                </SecondaryButton>

                <SecondaryButton
                    v-if="user.profile_photo_path"
                    type="button"
                    class="mt-2"
                    @click.prevent="deletePhoto"
                >
                  Remove Photo
                </SecondaryButton>

                <InputError :message="form.errors.photo" class="mt-2" />
              </div>

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

              <!-- Email -->
              <div class="col-span-6 sm:col-span-4">
                <InputLabel for="email" value="Email" />
                <TextInput
                    id="email"
                    v-model="form.email"
                    type="email"
                    class="mt-1 block w-full"
                    required
                    autocomplete="username"
                />
                <InputError :message="form.errors.email" class="mt-2" />

                <div v-if="$page.props.jetstream.hasEmailVerification && user.email_verified_at === null">
                  <p class="text-sm mt-2 dark:text-white">
                    Your email address is unverified.

                    <Link
                        :href="route('verification.send')"
                        method="post"
                        as="button"
                        class="underline text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800"
                        @click.prevent="sendEmailVerification"
                    >
                      Click here to re-send the verification email.
                    </Link>
                  </p>

                  <div v-show="verificationLinkSent" class="mt-2 font-medium text-sm text-green-600 dark:text-green-400">
                    A new verification link has been sent to your email address.
                  </div>
                </div>
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
    </div>

  </AppLayout>
</template>