<template>
  <div class="warp">
    <banner />
    <div class="container">
      <div class="home-bg">
        <el-image :src="home_bg" fit="contain">
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
      </div>
      <div>

      </div>
      <div class="main">
        <div class="main-carousel" style="width:300px;">
          <div class="main-title">Recently Hot Search</div>
          <el-carousel :interval="3000" type="card" height="300px" :initial-index="initialIndex" @change="changeIndex">
            <el-carousel-item v-for="(item) in homeImgList" :key="item.title">
              <el-image :src="item.image" fit="contain">
                <div slot="error" class="image-slot">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
            </el-carousel-item>
          </el-carousel>
        </div>
        <div class="main-type">
          <div class="main-title">Choose Type You Like！</div>
          <div class="main-type-wrap">
            <span v-for="item in typeList" :key="item.type" class="main-type-item" @click="handleSearchType(item.type)"> {{ item.type }}</span>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import Banner from '@/components/Banner/index.vue'
import { homepage, getMovieType } from '@/api/index'
export default {
  name: 'App',
  components: {
    Banner
  },
  data() {
    return {
      home_bg: require('@/assets/home_img/home_bg.png'),
      initialIndex: 0,
      homeImgList: [],
      typeList: []
    }
  },
  created() {
    this.loadHomepage()
    this.loadMovieType()
  },
  methods: {
    changeIndex(index) {
      this.initialIndex = index
    },
    async loadHomepage() {
      const res = await homepage()
      this.homeImgList = res
    },
    async loadMovieType() {
      const res = await getMovieType()
      this.typeList = res
    },
    handleSearchType(type) {
      this.$router.push({
        name: 'Search',
        query: {
          movieType: type
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>

.warp {
  .home-bg{
    min-height: 200px;
    max-height: 300px;
    margin: 20px 0;
  }
  .main {
    display: flex;
    gap:5%;
    justify-content: space-around;
    &-title {
      text-align: left;
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 20px;
    }
    &-type {
      width: 500px;
      &-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
      &-item {
        height: 32px;
        padding: 8px 15px;
        margin: 5px 0;
        font-size: 16px;
        line-height: 16px;
        border-radius: 16px;
        background: #eee;
        box-sizing: border-box;
        cursor: pointer;
        &:hover {
          transition: 0.3s;
          // font-weight: bold;
          box-shadow: rgba(99, 99, 99, 0.3) 0px 2px 8px 0px;
        }

      }
    }
  }
}
::v-deep.el-image {
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
