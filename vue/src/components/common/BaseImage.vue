<template>
  <img :src="baseUrl + image" alt="img" />
</template>

<script lang="ts" setup>
const props = defineProps<{ image: string }>()
const baseUrl = import.meta.env.VITE_BASE_URL
</script>

<style scoped></style>
