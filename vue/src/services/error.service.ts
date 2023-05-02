import axios from 'axios'

const errorService = (error: unknown) => {
  if (axios.isAxiosError(error) && error.response) {
    const err = error.response.data.message
    throw new Error(err)
  }
}
export default errorService
