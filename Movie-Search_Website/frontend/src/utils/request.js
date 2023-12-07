import axios from 'axios'
import { Message } from 'element-ui'

// Determine the development environment
let baseURL
// window.console.log(process.env.BASE_API, 'process.env.BASE_API')
if (process.env.NODE_ENV === 'development') {
  // dev
  baseURL = process.env.BASE_API
} else {
  // prod
}
const service = axios.create({
  baseURL: baseURL, // baseURL
  timeout: 10000 // request timeout
})
// response interceptor
service.interceptors.response.use(
  response => {
    if (response.headers['content-type'] === 'application/json') {
      const res = response.data
      if (res.status === 20002) {
        window.location.href = '/'
      }
      if (res.ok === false) {
        Message({
          message: res.msg || 'Error',
          type: 'error',
          duration: 5 * 1000
        })
        return Promise.reject(new Error(res.data || res.msg || 'Error'))
      }
      return res
    }
    return response
  },
  error => {
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)
export default service
