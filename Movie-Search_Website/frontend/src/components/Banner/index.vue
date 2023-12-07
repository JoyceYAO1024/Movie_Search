<template>
  <div class="header">
    <div class="header-wrap">
      <div class="header-logo"  @click="toHome">
        APEX MOVIE
      </div>
      <div class="header-input" v-show="showSearch">
        <el-select class="left" v-model="searchType">
          <el-option value="Title">Title</el-option>
          <el-option value="Cast">Cast</el-option>
          <el-option value="Crew">Crew</el-option>
        </el-select>
        <el-input
          v-model="searchVal"
          placeholder="Search movies, actors, more..."
          class="right"
          @focus="showIcon=true"
          @blur="showIcon=false"
        >
          <i slot="suffix" class="iconfont icon-search" @click="toSearch" />
        </el-input>
      </div>
      <div class="header-person" v-show="isLogin && !showLogOut" @click="toPerson">
        <i class="iconfont icon-person" />
      </div>
      <div class="header-user" v-show="!isLogin">
        <span @click="toLogin">Log In</span>
        <span class="gap"></span>
        <span @click="toRegister">Register</span>
      </div>
      <div class="header-user" v-show="showLogOut">
        <span @click="toLogOut">Log Out <i class="el-icon-switch-button"></i> </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BannerIndex',
  props: {
    showHomeIcon:{
      type: Boolean,
      default: true
    },
    selectVal: {
      type: String,
      default: ''
    },
    inputVal: {
      type: String,
      default: ''
    },
    showSearch: {
      type: Boolean,
      default: true
    },
    showLogOut: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchType: 'Title',
      searchVal: '',
      showIcon: false,
      isLogin: undefined
    }
  },
  watch: {
    selectVal: {
      handler(val) {
        if (val) {
          this.searchType = val
        }
      },
      immediate: true
    },
    inputVal: {
      handler(val) {
        this.searchVal = val
      },
      immediate: true
    }
  },
  created() {
    this.isLogin = localStorage.getItem('isLogin') || false
  },
  methods: {
    toHome() {
      if (this.$route.path !== '/') {
        this.$router.push({
          path: '/'
        })
      }
    },
    toSearch() {
      if (!this.searchVal) {
        return
      }
      if (this.$route.path === '/search') {
        this.$emit('handleReSearch', this.searchVal, this.searchType)
      } else {
        this.$router.push({
          name: 'Search',
          query: {
            searchVal: this.searchVal,
            searchType:this.searchType
          }
        })
      }
    },
    toPerson() {
      this.$router.push({
        path: '/profile'
      })
    },
    toLogin() {
      this.$router.push({
        path: '/login'
      })
    },
    toRegister() {
      this.$router.push({
        path: '/register'
      })
    },
    toLogOut() {
      localStorage.removeItem('isLogin')
      localStorage.removeItem('userEmail')
      document.querySelector('body').setAttribute('style', 'background-color:#fff;')
      this.toHome()
    }

  }
}
</script>

<style lang="scss" scoped>
.header {
  background: #A49774;
  box-shadow: 0 2px 10px 0 rgba(0,0,0,.1);
}
.header-wrap {
  width: 80%;
  max-width: 1280px;
  height: 70px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10%;
  // padding: 0 5%;
}
.header-logo {
  font-size: 30px;
  font-weight: bold;
  color: #fff;
  cursor: pointer;
}
.header-input  {
  ::v-deep .el-select>.el-input {
    width: 80px;
  }
  ::v-deep .el-select .el-input.is-focus .el-input__inner{
    border-color: transparent;
  }
  ::v-deep .el-input__inner {
    border-radius: 0;
    border:1px solid transparent;
    color: #333;
    background: rgba(255,255,255,.9);
  }
  ::v-deep .el-input__suffix {
    :hover {
      cursor: pointer;
    }
  }
  .left {
    ::v-deep .el-input__inner {
      border-radius: 5px 0 0 5px;
    }
  }
  .right {
    width: 300px;
    ::v-deep .el-input__inner {
      border-radius: 0 5px 5px 0;
    }
  }
}
.header-person{
  flex: 1;
  text-align: right;
  :hover {
    cursor: pointer;
  }
}
.header-user{
  flex: 1;
  text-align: right;
  font-size: 18px;
  line-height: 25px;
  font-weight: bold;
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: end;
  color: #fff;
  span {
    &:hover {
      opacity: 0.7;
      cursor: pointer;
    }
    &.gap {
      display: inline-block;
      width: 1px;
      height: 15px;
      background:#eee
    }
  }
 
}
/* icon class */
.icon-search {
  font-size: 20px;
  line-height: 40px;
  color: #c0c4cc;
  padding-right: 10px;

}
.icon-person {
  font-size: 30px;
  line-height: 30px;
  color: rgba(255,255,255,.6);
}
</style>
