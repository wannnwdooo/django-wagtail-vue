import { useToast } from 'vue-toastification'
interface ErrorData {
  [key: string]: string[]
}

interface ErrorMessages {
  [key: string]: string
}

const toast = useToast()

const okMessages = (data: string) => {
  toast.success(data)
}
const warnMessage = (data: string) => {
  toast.warning(data)
}

const customErrorMessage = (data: string) => {
  toast.error(data)
}
const errorMessages = (data: ErrorData) => {
  const errorMessages: ErrorMessages = {
    email: 'Почта',
    username: 'Логин',
    current_password: 'Пароль',
    password: 'Пароль',
    phone_number: 'Телефон',
    avatar: 'Изображение профиля',
    apartment: 'Квартира',
    building: 'Проект',
    client: 'ФИО',
    date: 'Дата',
    time: 'Время',
    message: 'Комментарий',
    tariff: 'Тариф'
  }
  const errorList: string[] = []

  for (const prop in data) {
    let key = ''
    errorMessages[prop] ? (key += errorMessages[prop] + ': ') : (key += '')

    if (Object.prototype.hasOwnProperty.call(data, prop)) {
      data[prop].forEach((el) => errorList.push(`${key} ${el}`))
    }
  }

  errorList.forEach((el) => toast.error(el))
}
const toasterService = {
  ok: okMessages,
  handleError: errorMessages,
  customError: customErrorMessage,
  warn: warnMessage
}
export { toasterService }
