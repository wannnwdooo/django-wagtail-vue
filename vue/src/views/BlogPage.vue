<template>
  <template v-if="nonNestedPage">
    <h1 class="blog-title">Страница блога</h1>
    <button v-for="item in result" @click="pushLink(item.title, item.id)">{{ item.title }}</button>
  </template>
  <router-view />
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { getAllBlogs } from '@/services/blog.service'
import { useRouter } from 'vue-router'
import { checkNonNestedPage } from '@/helpers/route'

const router = useRouter()

const nonNestedPage = checkNonNestedPage('/blog/')

const result = ref([])

const pushLink = (route: string, id: number) =>
  router.push({ path: `/blog/${route}`, query: { id } })

onMounted(async () => {
  result.value = []
  result.value = await getAllBlogs()
})
</script>

<style scoped>
.blog-title {
  color: #34cc01;
}
</style>
