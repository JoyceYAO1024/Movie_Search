import request from '@/utils/request.js'

// homepage
export function homepage() {
  return request({
    url: '/api/homepage'
  })
}
// register
export function register(data) {
  return request({
    url: '/api/user/register',
    method: 'POST',
    data
  })
}
// login
export function login(data) {
  return request({
    url: '/api/user/login',
    method: 'POST',
    data
  })
}
// search page
export function search(name) {
  return request({
    url: `/api/search/moviename/${name}`
  })
}
export function searchByCast(name) {
  return request({
    url: `/api/search/cast/${name}`
  })
}
export function searchByCrew(name) {
  return request({
    url: `/api/search/crew/${name}`
  })
}
export function searchDetail(id) {
  return request({
    url: `/api/movie/${id}`
  })
}
export function searchDetailReview(id) {
  return request({
    url: `/api/review/${id}`
  })
}
export function addReview(data) {
  return request({
    url: `/api/addreview`,
    method: 'POST',
    data
  })
}
export function addScore(movie_id, score) {
  return request({
    url: `/api/score/${movie_id}/${score}`
  })
}
// movie type
export function getMovieType() {
  return request({
    url: `/api/search/movieType`
  })
}
export function searchMovieByType(type) {
  return request({
    url: `/api/search/movieByType/${type}`
  })
}
// get person info  
export function getPersonInfo(email) {
  return request({
    url: `/api/personpage/${email}`
  })
}
// person update picture
export function updateUserPicture(email, pid) {
  return request({
    url: `/api/user/update_picture/${email}/${pid}`
  })
}
// person update background  
export function updateUserBackground(email, bid) {
  return request({
    url: `/api/user/update_background/${email}/${bid}`
  })
}
// get person wish list  
export function getPersonWishList(email) {
  return request({
    url: `/api/getwishlist/${email}`
  })
}
// get person block list  
export function getBlockWishList(email) {
  return request({
    url: `/api/getblocklist/${email}`
  })
}
// add person block user  
export function addBlockUser(email, block_email) {
  return request({
    url: `/api/block/${email}/${block_email}`
  })
}
// add wish list item
export function addWishlist(email, id) {
  return request({
    url: `/api/addwishlist/${email}/${id}`
  })
}
// delete wish list item
export function deleteWishlist(email, id) {
  return request({
    url: `/api/deletewishlist/${email}/${id}`
  })
}