import httpService from './http.service'
import { toasterService } from './toaster.service'
import errorService from './error.service'
import type {LocationQueryValue} from "vue-router";

interface IArticle {
  parent_title: string
  id: number
}

const getAllBlogs = async () => {
  try {
    const { data } = await httpService.get(`/blog_pages`)
    const filterData = data.filter((el: IArticle) => el.parent_title === 'blog')
    console.log(filterData)
    // return data[0].blog_image
    return filterData
  } catch (err) {
    toasterService.customError('Что-то пошло не так')
    errorService(err)
  }
}

const getOneBlog = async (id: string | null | LocationQueryValue[]) => {
  try {
    const { data } = await httpService.get(`/blog_pages`)
    if (id) {
      const filterData = data.filter((el: IArticle) => el.id === +id)[0]
      console.log(filterData)
      // return data[0].blog_image
      return filterData
    }

  } catch (err) {
    toasterService.customError('Что-то пошло не так')
    errorService(err)
  }
}
export { getAllBlogs, getOneBlog }
