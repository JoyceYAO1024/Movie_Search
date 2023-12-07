<template>
  <div class="wrap">
    <banner :show-log-out="true" :show-search="false" />
    <div class="container" :class="backgroundType">
      <!-- base info -->
      <div class="base-info">
        <div  :class="[{'user-avatar':true}, {'edit': isEdit}, avatarClassName]" @click="handleChangeAvatar"></div>
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
        <div v-show="isEdit" class="change_bg" @click="handleChangeBackground"></div>
        <div class="profile-header" @click="handleEditOrSave">
          <template v-if="!isEdit">
            <div class="profile-header-set"><i class="el-icon-setting" ></i><span >Edit your home page</span></div>
          </template>
          <template v-else>
            <div class="profile-header-set"><i class="el-icon-finished"></i><span>Click To Finish</span></div>
          </template>
        </div>
      </div>
      <!-- wish list -->
      <div class="area-wish">
        <div class="title">Wish List</div>
        <div class="wish-list">
          <el-empty v-show="!wishlist.length" description="This Empty, Go To Collect Your Favorite!"></el-empty>
          <div class="wish-list-wrap" v-show="wishlist.length">
            <div v-for="item in wishlist" :key="item.title" class="card">
              <div class="card-image"> <el-image :src="item.image"  style="height: 200px;" fit="fill" /></div>
                <div class="card-description">
                  <p class="text-title">
                    <span>{{ item.title }}</span>
                    <template>
                      <el-popconfirm
                        confirm-button-text='confirm'
                        cancel-button-text='cancel'
                        :title="`Are you sure to delete this wish ?`"
                        @confirm="deleteWishlist(item.id)"
                      >
                        <i  slot="reference" class="el-icon-delete"></i>
                      </el-popconfirm>
                    </template>
                  </p>
                </div>
            </div>
          </div>
        </div>
      </div>
      <!-- black list -->
      <div class="area-black" v-show="blockList.length">
        <div class="title">Block List</div>
        <div class="black-list">
          <div class="header" v-for="item in blockList" :key="item.block_user">
            <div class="image" :class="`image-${item.picture === 0 ? 'default' : (item.picture === 1 ? 'male' : 'female')}`"></div>
            <div>
              <p class="name"> {{ item.name }}</p>
            </div>
          </div>
        </div>
      </div>
      <!-- Dialog -->
      <EditAvatarDialog 
        ref="EditAvatarDialog"
        @saveAvatar="saveAvatar"
      />
      <EditBackgroundDialog 
        ref="EditBackgroundDialog"
        @saveBackGround="saveBackGround"
      />
   </div>
  </div>

</template>

<script>
import Banner from '@/components/Banner/index.vue'
import {getPersonInfo, getPersonWishList, getBlockWishList, updateUserPicture, updateUserBackground, deleteWishlist} from '@/api/index'
import EditAvatarDialog from './components/EditAvatarDialog.vue'
import EditBackgroundDialog from './components/EditBackgroundDialog.vue'
export default {
  name: 'UserProfile',
  components: { Banner, EditAvatarDialog, EditBackgroundDialog },
  data() {
    return {
      localStorageEmail: '',
      userInfo: {
        name: '',
        email: '',
        password: ''
      },
      gender:'Male',
      avatarClassName: 'default',
      backgroundType: 'white',
      wishlist: [],
      blockList: [],
      isEdit: false
    }
  },
  created() {
    this.localStorageEmail = localStorage.getItem('userEmail')
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
        console.log(this.userInfo.background)
        this.saveBackGround(this.userInfo.background)
      }).finally(_ => {
        this.fetchWishListData()
        this.fetchBlockListData()
      })
    },
    fetchWishListData() {
      getPersonWishList(this.localStorageEmail).then((res) => {
        this.wishlist = res.data
      })
    },
    fetchBlockListData() {
      getBlockWishList(this.localStorageEmail).then((res) => {
        this.blockList = res.data
      })
    },
    deleteWishlist(id) {
      deleteWishlist(localStorage.getItem('userEmail'), id).then(_ => {}).finally(_ => {
        this.fetchWishListData()
      })
    },
    handleEditOrSave() {
      if (this.isEdit) {
        // confirm edit
        if (this.userInfo.email.match(/^\w+@\w+\.\w+$/i)) {
          // update picture
          const AVATAR_DATA = {
            default: 0,
            male: 1,
            female: 2
          }
          updateUserPicture(this.localStorageEmail, AVATAR_DATA[this.avatarClassName]).then((res) => {
            if (res.success === 'true') {
              this.$message({
                message: 'Edit info success!',
                type: 'success'
              })
            }
          })
          // update background
          updateUserBackground(this.localStorageEmail, this.backgroundType)
        } else {
          return this.$message({
            message: 'Please enter correct email',
            type: 'error'
          })
        }
      }
      this.isEdit = !this.isEdit
    },
    handleChangeAvatar() {
      if (this.isEdit) {
        this.$refs.EditAvatarDialog.open()
      }
    },
    saveAvatar(type) {
      this.avatarClassName = type
    },
    handleChangeBackground() {
      if (this.isEdit) {
        this.$refs.EditBackgroundDialog.open()
      }
    },
    saveBackGround(type) {
      document.querySelector('body').setAttribute('class', `bg-theme${type}`)
      this.backgroundType = type
    }
  }
}
</script>

<style lang='scss' scoped>
.container {
  text-align: center;
  height: calc(100% - 70px);
  overflow: auto;
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
    span {
      cursor: pointer;
    }
  }
  .el-icon-setting,
  .el-icon-finished {
    font-size: 25px;
    cursor: pointer;
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
  .user-avatar.edit {
    cursor: pointer;
  }
  .user-info {
    // flex: 1;
    ::v-deep .el-form-item {
      margin-bottom: 10px;
    }
    ::v-deep .el-form-item__content{
      border-radius: 10px;
      padding: 0 20px;
      width: 260px;
      text-align: left;
    }
    ::v-deep .el-input__inner {
      background: #A49774;
      color: #FFF;
      border: none;
      padding: 0 10px;
    }
  }
  .change_bg {
    width: 80px;
    height: 80px;
    background: url('@/assets/home_img/bg_icon.png')  no-repeat center center  /80px;
    cursor: pointer;
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
.black-list {
  display: flex;
  gap: 55px;
  .iconfont {
    font-size: 50px;
    color: #999;
  }
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
}
/*Description */
.card-description {
 display: flex;
 position: absolute;
 gap: 1em;
 flex-direction: column;
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
/* Hover states */
// .card:hover .card-description {
//  transform: translateY(100%);
// }

.black-list {
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
</style>
