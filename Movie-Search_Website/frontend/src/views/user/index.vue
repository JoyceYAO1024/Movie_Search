<template>
  <div class="wrap">
    <banner  />
    <div class="container" :class="backgroundType">
      <!-- base info -->
      <div class="base-info">
        <div  :class="[{'user-avatar':true}, {'edit': isEdit}, avatarClassName]"></div>
        <div class="user-info">
          <el-form ref="form" label-width="150px">
            <el-form-item label="User Name">
              <span v-show="!isEdit">  {{ userInfo.name }}</span>
              <el-input v-show="isEdit" v-model="userInfo.name"></el-input>
            </el-form-item>
            <el-form-item label="Email">
              <span v-show="!isEdit">  {{ userInfo.email }}</span>
              <el-input v-show="isEdit" v-model="userInfo.email"></el-input>
            </el-form-item>
            <el-form-item label="Gender">
              <span v-show="!isEdit">  {{gender}}</span>
              <el-radio v-show="isEdit" v-model="gender" label="Male"></el-radio>
              <el-radio v-show="isEdit" v-model="gender" label="Female"></el-radio>
              <el-radio v-show="isEdit" v-model="gender" label="Others"></el-radio>
            </el-form-item>
            <el-form-item v-show="isEdit" label="Password">
              <el-input v-model="userInfo.password" show-password></el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <!-- wish list -->
      <div class="area-wish">
        <div class="title">{{userInfo.name}} 's Wish List</div>
        <div class="wish-list">
          <el-empty v-show="!wishlist.length" description="This Empty"></el-empty>
          <div class="wish-list-wrap" v-show="wishlist.length">
            <div v-for="item in wishlist" :key="item.title" class="card">
              <div class="card-image"> <el-image :src="item.image"  style="height: 200px;" fit="fill" /></div>
                <div class="card-description">
                  <p class="text-title"> {{ item.title }}</p>
                </div>
            </div>
          </div>
        </div>
      </div>
   </div>
  </div>

</template>

<script>
import Banner from '@/components/Banner/index.vue'
import {getPersonInfo, getPersonWishList, getBlockWishList, updateUserPicture, updateUserBackground, deleteWishlist} from '@/api/index'
export default {
  name: 'UserProfile',
  components: { Banner },
  data() {
    return {
      localStorageEmail: '',
      userInfo: {
        name: '',
        email: '',
        password: '',
        blocklist: []
      },
      gender:'Male',
      avatarClassName: 'default',
      backgroundType: 'white',
      wishlist: [],
      isEdit: false
    }
  },
  created() {
    this.localStorageEmail = this.$route.query?.email
    this.fetchData()
  },
  beforeDestroy() {
    document.querySelector('body').removeAttribute('class')
  },
  methods: {
    fetchData() {
      getPersonInfo(this.localStorageEmail).then((res) => {
        this.userInfo = res.data[0]
        this.avatarClassName = this.userInfo.picture === 0 ? 'default' : (this.userInfo.picture === 1 ? 'male' : 'female')
        this.saveBackGround(this.userInfo.background === 0 ? 'white' : 'black')
        console.log(this.userInfo)
      }).finally(_ => {
        this.fetchWishListData()
      })
    },
    fetchWishListData() {
      getPersonWishList(this.localStorageEmail).then((res) => {
        this.wishlist = res.data
      })
    },
    saveBackGround(type) {
      if (type === 'black') {
        document.querySelector('body').setAttribute('style', 'background-color:#f0f3f5;')
      } else {
        document.querySelector('body').setAttribute('style', 'background-color:#fff;')
      }
      this.backgroundType = type
    }
  }
}
</script>

<style lang='scss' scoped>
.container {
  text-align: center;
}
.container.black {
  .profile-header {
    color: #333;
  }
  ::v-deep .el-form-item__label {
    color: #333;
  }
}
.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  font-size: 18px;
  &-set {
    display:flex;
    align-items: center;
    gap: 30px;
  }
  .el-icon-setting,
  .el-icon-finished {
    font-size: 25px;
  }
  svg.icon {
    border-bottom: 3px solid #515151;
    cursor: pointer;
  }
}
.base-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
  gap: 50px;
  .user-avatar {
    width: 200px;
    height: 200px;
    border-radius: 50%;
  }
  .default {
      background: url('@/assets/home_img/default.png')  no-repeat center center  /210px;
    }
    .female {
      background: url('@/assets/home_img/default_female.png')  no-repeat center center  /210px;
    }
    .male {
      background: url('@/assets/home_img/default_male.png')  no-repeat center center  /210px;
    }
  .user-info {
    flex: 1;
    ::v-deep .el-form-item {
      margin-bottom: 10px;
    }
    ::v-deep .el-form-item__content{
      border-radius: 10px;
      padding: 0 20px;
      width: 260px;
      text-align: left;
    }
  }
}
.title {
  width: 250px;
  padding: 10px 0;
  margin: 40px 0;
  border-radius: 10px;
  background: #A49774;
  color:#fff;
}
.wish-list-wrap {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
}
::v-deep .el-image {
  margin-top: 30px;
}
.card {
 height: 280px;
 width: 200px;
 position: relative;
 transition: all 0.4s cubic-bezier(0.645, 0.045, 0.355, 1);
 border-radius: 1em;
 box-shadow: 0 0 20px 8px #d0d0d0;
 .el-icon-delete {
  visibility: hidden;
  cursor: pointer;
 }
 &:hover {
  .el-icon-delete {
   visibility: visible;
  }
 }
}
 /*Image*/
.card-image {
 height: 100%;
 width: 100%;
 position: absolute;
 transition: all 1s cubic-bezier(0.645, 0.045, 0.355, 1);
//  background: #0a3394;
//  background: linear-gradient(to top, #0a3394, #4286f4);
}
/*Description */
.card-description {
 display: flex;
 position: absolute;
 gap: 1em;
 flex-direction: column;
//  background-color: #f5f5f5;
 width: 85%;
 height:50px;
 bottom: 0;
 border-radius: 1em 1em 0 0;
 transition: all 1s cubic-bezier(0.645, 0.045, 0.355, 1);
 padding: 1rem;
}
/*Text*/
.text-title {
 font-size: 1.4em;
 font-weight: 700;
}
.text-body {
 font-size: 1em;
 line-height: 150%;
}
</style>
