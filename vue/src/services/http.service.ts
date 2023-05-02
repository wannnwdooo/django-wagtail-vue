import type { AxiosRequestHeaders } from 'axios'
import axios from 'axios'
import { toasterService } from './toaster.service'
import cookieService from './cookie.service'

// const http = axios.create({ baseURL: `/api/v2` })
const http = axios.create({ baseURL: import.meta.env.VITE_BACK_URL })

http.interceptors.request.use(
  async (config) => {
    // Тут можем описывать уходящий запрос
    // Приделывать к нему хедеры и обрабатывать данные для отправки
    const token = cookieService.get('auth_token')

    if (token)
      config.headers = {
        ...config.headers,
        Authorization: `token ${token}`
      } as AxiosRequestHeaders
    return config
  },
  (error) => Promise.reject(error)
)

http.interceptors.response.use(
  (res) => {
    // Тут мы можем обрабатывать входящие запросы с бэка
    // Трансформировать данные в нужный формат и тд.
    return res
  },

  (error) => {
    const expectedErrors =
      error.response && error.response.status >= 400 && error.response.status < 500

    if (!expectedErrors) {
      toasterService.customError('Ой, что-то сломалось')
    }

    return Promise.reject(error)
  }
)

const httpService = {
  get: http.get,
  post: http.post,
  put: http.put,
  delete: http.delete,
  patch: http.patch
}

export default httpService
