<template>
  <div class="wrap">
    <banner :show-collect="true" :wish-title="details.title " />
    <div class="detail container">
      <div class="detail-left">
        <div class="detail-top">
          <div class="detail-top-left">
            <el-image
              :src="temImg"
              style="width: 150px;height: 300px;"
              fit="contain"
              >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </div>
          <div class="detail-top-right">
            <div class="title">
              <span>{{ details.title }}</span>
              <span class="time"> ({{ details.release_date }})</span>
              <i class="el-icon-document-copy" @click="shareUrl"></i>
            </div>
            <div class="overview">{{ details.overview }}</div>
            <div class="rate">
              <span class="rate-text">Rating</span>
              <div class="rate-bg">
                <el-rate
                  :value="details.vote_average/ 2"
                  disabled
                  :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                  score-template="{value}"
                />
                <span>{{ getRate(details.vote_average) }}</span>
              </div>
            </div>
            <div class="header-collect"  v-if="isLogin" @click="addWish">
              <i class="el-icon-star-on"></i>
              <span>Collect</span>
            </div>
          </div>
        </div>
        
        <div class="detail-item">
          <div class="detail-title"><i></i><span>Top Cast</span></div>
          <div class="detail-cast-list">
            <div v-for="item in cast" :key="item.id" class="detail-cast-item">
              <i class="iconfont icon-person" />
              <span class="right">
                <span class="right-name">{{ item.name }}</span>
                <span class="right-character">{{ item.character }}</span>
              </span>
            </div>
          </div>
        </div>
        <div class="detail-item">
          <div class="detail-title"><i></i><span>Review</span></div>
          <div class="detail-score-add" v-if="isLogin">
            <el-rate
              v-model="score"
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
            </el-rate>
            <el-link @click="handleAddScore" type="primary">Add Score</el-link>
          </div>
          <div class="detail-review-add"  v-if="isLogin">
            <el-input
              type="textarea"
              :rows="2"
              placeholder="Input Your Review"
              v-model="review">
            </el-input>
            <el-button @click="handleAddReview" type="primary">Add Review</el-button>
          </div>
          <div v-show="reviewList.length" class="detail-review-list">
            <div v-for="item in reviewList" :key="item.time" class="card">
              <i v-if="item.email !==localStorageEmail && isLogin" class="el-icon-error" @click="handleBlockUser(item.email)"></i>
              <i class="el-icon-document-copy" @click="copyValue(item.review)"></i>
              <div class="header">
                <div class="image" :class="`image-${item.picture === 0 ? 'default' : (item.picture === 1 ? 'male' : 'female')}`" @click="handleToUserPage(item.email)"></div>
                <div>
                  <p class="name" @click="handleToUserPage(item.email)"> {{ item.name }}</p>
                  <p class="time"> {{ item.time }}</p>
                </div>
              </div>
              <p class="message">{{ item.review }}</p>
            </div>
          </div>
          <el-empty v-show="!reviewList.length" description="This Empty, Go To Add Review!"></el-empty>
        </div>
      </div>
      <div class="detail-right">
        <div class="recommend-title">You May Like...</div>
        <div class="recommend-list">
          <div v-for="(item) in recommendList" :key="item.id" class="recommend-item" @click="handleToDetail(item.id)">
              <el-image :src="item.Poster" fit="contain" style="width: 50px; height: 75px" >
                <div slot="error" class="image-slot">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
              <div class="recommend-item-content">
                <span class="main">{{ item.title }}</span>
                <span> <i class="el-icon-star-on"></i> <span > {{ item.vote_average }}</span></span>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Banner from '@/components/Banner/index.vue'
import { searchMovieByType, searchDetail, searchDetailReview, addReview, addScore, addWishlist, addBlockUser } from '@/api/index'
export default {
  name: 'App',
  components: {
    Banner
  },
  data() {
    return {
      movie_id: '',
      cast: [],
      crew: [],
      details: {
        title: ''
      },
      recommendList: [],
      reviewList: [],
      temImg: require('@/assets/temp.png'),
      review: '',
      iconClasses: ['icon-rate-face-1', 'icon-rate-face-2', 'icon-rate-face-3'],
      score: null,
      isLogin: false,
      localStorageEmail: ''
    }
  },
  created() {
    this.movie_id = this.$route.query?.id
    this.isLogin = localStorage.getItem('isLogin') || false
    this.localStorageEmail = localStorage.getItem('userEmail')
  },
  watch:{
    movie_id(cur) {
      this.fetchData()
    }
  },
  methods: {
    handleToDetail(id) {
      this.movie_id = id
      this.$router.push(`${this.$route.path}?id=${id}`)
    },
    getRate(val) {
      return (Number(val * 10) / 10).toFixed(1)
    },
    fetchData() {
      searchDetail(this.movie_id).then(res => {
        const data = res.data[0]
        this.details = data
        this.cast = JSON.parse(data.cast).slice(0, 6)
        this.temImg = data.poster
        const type = JSON.parse(data.genres)[0];
        (type?.name) && this.fetchRecommend(type.name) 
      })
      this.fetchReview()
    },
    fetchRecommend(type) {
      searchMovieByType(type).then(res => {
        const list = this.uniqueArr(res.data).sort(function(a, b) { return b.vote_average - a.vote_average })
        this.recommendList = list.slice(0, 5)
        console.log(this.recommendList)
      })
    },
    uniqueArr(arr) {
      let result = [] 
      arr.forEach((item) => {
        if (!result.some(m => m.id === item.id) && item.id !== Number(this.movie_id)) {
          result.push(item)
        }
      })
      return result
    },
    fetchReview() {
      searchDetailReview(this.movie_id).then(res => {
        this.reviewList = res.data
      })
    },
    addWish() {
      addWishlist(this.localStorageEmail, this.movie_id).then(res => {
        if (res.status === 'successful') {
          this.$message({
            message: 'Add wish movie success!',
            type: 'success'
          })
        }
      })
    },
    handleAddReview() {
      const data = {
        email:  this.localStorageEmail,
        movie_id: this.details.id,
        review: this.review
      }
      addReview(data).then((res) => {
        this.fetchReview()
      })
    },
    handleAddScore() {
      addScore(this.details.id, this.score).then((res) => {
        console.log(res)
        if (res.success === 'true') {
          this.$message({
            message: 'Score success!',
            type: 'success'
          })
          this.score = null
        }
      })
    },
    copyValue(value, isReview = true) {
      var input = document.createElement('input')
      input.value = isReview ? `${this.details.title} —— ${value}` : value
      document.body.appendChild(input)
      input.select() 
      document.execCommand('Copy')
      document.body.removeChild(input) 
      this.$message.success('Copy success!')
    },
    shareUrl() {
      this.copyValue(window.location.href, false)
    },
    handleBlockUser(block_email) {
      addBlockUser(this.localStorageEmail, block_email).then(res => {
        if (res.success === 'true') {
          this.$message({
            message: 'Block success!',
            type: 'success'
          })
          this.fetchReview()
        }
      })
    },
    handleToUserPage(email) {
      if (email === this.localStorageEmail) {
        this.$router.push({
          path: '/profile'
        })
      } else {
        this.$router.push({
          path: '/user',
          query: {
            email: email
          }
        })
      }
      console.log(email)
    }
  }
}
</script>

  <style lang="scss" scoped>
  .container {
    height: calc(100% - 110px);
    margin: 20px auto ;
    overflow: auto;
    text-align: left;
    // width: 1000px;
  }
  .detail {
    display: flex;
    gap: 50px;
    &-left {
      flex: 1;
    }
    &-right {
      width: 200px;
      padding-top: 30px;
      .recommend {
        &-title {
          font-size: 20px;
          font-style: italic;
          margin-bottom: 10px;
        }
        &-list {
          display: flex;
          flex-direction: column;
        }
        &-item {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 10px 0;
          border-bottom: 1px dashed #eee;
          &-content {
            display: flex;
            flex-direction: column;
            flex: 1;
            span.main {
              color:#000;
              line-height: 20px;
              margin-bottom: 5px;
              cursor: pointer;
              &:hover {
                text-decoration: underline;
              }
            }
          }
          .el-icon-star-on{
            color: rgb(247, 186, 42);
          }
        }

      }
    }
    &-top {
      display: flex;
      gap: 30px;
      align-items: center;
      &-right {
        .title {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 15px;
          font-size: 20px;
          color: #000;
          font-weight: bold;
          background: #A59773;
          border-radius: 3px 3px 0 0;
          .el-icon-document-copy {
            margin-left: auto;
            cursor: pointer;
          }
        }
        .time {
          margin-left: 5px;
          font-size: 14px;
          color: #eee;
          font-weight: normal;
        }
        .overview{
          padding: 10px 20px;
          font-style: italic;
          background: #eee;
          border-radius:  0 0 3px 3px;
        }
        .rate {
          margin-top: 10px;
          display: flex;
          &-text{
            padding: 10px;
            background: #A59773;
            border-radius: 3px 0 0 3px;
          }
          .rate-bg {
            display: flex;
            background: #eee;
            align-items: center;
            flex: 1;
            padding: 10px;
            border-radius: 0 3px 3px 0;
          }
        }
      }
    }
    &-cast{
      &-list {
        display: grid;
        align-items: center;
        justify-content: center;
        grid-template-columns: repeat(3, 250px);
        grid-column-gap:60px;
        grid-row-gap:20px;
      }
      &-item {
        display: flex;
        align-items: center;
        padding: 10px 10px 10px 30px;
        gap: 20px;
        border:1px solid #eee;
        width: 250px;
        border-radius: 5px;
        &:hover {
          box-shadow: 0px 0px 6px 0px rgba(29,120,255,0.2);
        }
        .iconfont {
          font-size: 40px;
        }
        span.right {
          display: flex;
          flex: 1;
          text-align: center;
          flex-direction: column;
          align-items: center;
          &-name {
            color: #202d40;
            font-weight: bold;
            &:hover {
              text-decoration: underline;
            }
          }
          &-character {
            color: rgba(0,0,0,.55);
            &:hover {
              opacity: 0.8;
            }
          }
        }
        &:hover {
          cursor: pointer;
        }
      }
    }
    &-title{
      display: flex;
      gap: 10px;
      align-items: center;
      font-size: 20px;
      line-height: 20px;
      color: #000;
      border-radius: 3px;
      margin: 20px 0;
      i {
        display: inline-block;
        width: 3px;
        height: 18px;
        background: #A59773;
      }
    }
    .detail-review-list {
      margin-top: 20px;
      display: grid;
      align-items: center;
      justify-content: center;
      grid-template-columns: repeat(3,1fr);
      grid-column-gap:20px;
      grid-row-gap:20px;
      justify-content: space-between;
    }
  }
  .detail-score-add {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-bottom: 10px;
  }
  .detail-review-add {
    display: flex;
    align-items: center;
    gap: 10px;
  }
.card {
  position: relative;
  background-color: rgba(243, 244, 246, 1);
  padding: 20px;
  max-width: 320px;
  border-radius: 10px;
  box-shadow: 0 20px 30px -20px rgba(5, 5, 5, 0.24);
  .header {
    display: flex;
    align-items: center;
    grid-gap: 1rem;
    gap: 1rem;
  }
  .header .image {
    height: 4rem;
    width: 4rem;
    border-radius: 9999px;
    object-fit: cover;
    cursor: pointer;
  }
  .image-default {
    background: url('@/assets/home_img/default.png')  no-repeat center center  /4rem;
  }
  .image-female {
    background: url('@/assets/home_img/default_female.png')  no-repeat center center  /4rem;
  }
  .image-male {
    background: url('@/assets/home_img/default_male.png')  no-repeat center center  /4rem;
  }

.stars {
  display: flex;
  justify-content: center;
  grid-gap: 0.125rem;
  gap: 0.125rem;
  color: rgba(34, 197, 94, 1);
}

.stars svg {
  height: 1rem;
  width: 1rem;
}

.name {
  margin-top: 0.25rem;
  font-size: 1.125rem;
  line-height: 1.75rem;
  font-weight: 600;
  --tw-text-opacity: 1;
  color: rgba(55, 65, 81, 1);
  cursor: pointer;
}
// .time {
//   font-size: 0.8rem;
// }

.message {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    margin-top: 1rem;
    color: rgba(107, 114, 128, 1);
  }
  .el-icon-document-copy {
    display: none;
    position: absolute;
    right: 50px;
    font-size: 20px;
    cursor: pointer;
  }
  .el-icon-error {
    display: none;
    position: absolute;
    right: 20px;
    font-size: 20px;
    cursor: pointer;
    color: #f56c6c;
  }
  &:hover {
    .name {
      text-decoration: underline;
    }
    .el-icon-document-copy {
      display: block;
    }
    .el-icon-error {
      display: block;
    }
  }
}
.header-collect{
  margin-top: 10px;
  line-height: 20px;
  text-align: right;
  i {
    font-size: 20px;
    cursor: pointer;
  }
  span {
    font-size: 20px;
    cursor: pointer;
  }
}
::v-deep.el-image {
  display: flex;
  align-items: center;
  justify-content: center;
}
::v-deep .el-empty {
  padding: 20px 0;
}
  </style>

