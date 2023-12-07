<template>
  <div class="wrap">
    <banner ref="banner" :select-val="searchType" :input-val="searchVal" @handleReSearch="handleReSearch"/>
    <div class="container search">
      <div class="search-header">
        <!-- title -->
        <div class="search-value">
          <template v-if="searchVal"> The Result of Search “{{ searchVal }}”</template>
          <template v-else>The Result of Type “{{ movieType }}” <i class="el-icon-document-copy" @click="shareUrl"></i></template>
        </div>
        <!-- sort -->
        <div class="search-sort" >
          <div
            v-for="item in sortList"
            :key="item.key"
            class="search-sort-item"
            :class="item.key === sortKey ? 'search-sort-item--active' : ''"
            @click="handleSort(item.key)"
          >
            {{ item.name }}
          </div>
        </div>
      </div>
      <div class="search-result" v-loading="loading">
        <el-empty v-show="!response.length" description="This Empty, Please Change You Search Content!"></el-empty>
        <div v-for="item in response" :key="item.index" class="search-item">
        <!-- img -->
        <div class="search-item-img">
          <el-image
            :src="item.Poster"
            style="width: 90px;height: 135px;"
            fit="contain"
            >
            <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
            </div>
          </el-image>
        </div>
        <!-- main -->
        <div class="search-item-main">
          <div class="search-item-header" @click="handleToDetail(item.id)"> <span class="search-item-title">{{ item.title }}</span> <span class="search-item-time">{{ item.release_date }}</span> </div>
          <div class="search-item-introduction">{{ item.overview }}</div>
          <div class="search-item-rate">
            <span class="search-item-rate--left">
              <!-- <span>Rating</span> -->
              <span><span class="primary">{{ getRate(item.vote_average) }}</span></span>
            </span>
            <el-rate
              :value="item.vote_average/2"
              disabled
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
              score-template="{value}"
            />
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import Banner from '@/components/Banner/index.vue'
import { search, searchByCast, searchByCrew, searchMovieByType } from '@/api/index'
export default {
  name: 'App',
  components: {
    Banner
  },
  data() {
    return {
      loading: false,
      searchType: null,
      searchVal: null,
      movieType: '',
      response: [],
      freeResponse: [],
      sortKey:1,
      sortList: [
        {name: 'Most Relevant', key: 1},
        {name: 'Top Rated', key:2},
        {name:'Most Recent', key:3}
      ]
    }
  },
  watch:{
    sortKey(cur) {
      if (cur === 1) {
        this.response = JSON.parse(JSON.stringify(this.freeResponse))
      } else if(cur === 2) {
        this.response = this.response.sort(function(a, b) { return b.vote_average - a.vote_average })
      } else if (cur === 3) {
        this.response = this.response.sort(function(a, b) { return new Date(b.release_date).getTime() - new Date(a.release_date).getTime() })
      }
    }
  },
  mounted() {
    this.searchType = this.$route.query?.searchType
    this.searchVal = this.$route.query?.searchVal
    this.movieType = this.$route.query?.movieType
    if (this.searchVal) {
      this.fetchSearchData()
    }
    if (this.movieType) {
      this.fetchSearchTypeData()
    }
  },
  methods: {
    getRate(val) {
      return (Number(val * 10) / 10).toFixed(1)
    },
    fetchSearchData() {
      this.loading = true
      if (this.searchType === 'Title') {
        search(this.searchVal).then(res => {
          this.handleData(res.data)
        })
      } else if (this.searchType === 'Cast') {
        searchByCast(this.searchVal).then(res => {
          this.handleData(res.data)
        })
      } else if (this.searchType === 'Crew') {
        searchByCrew(this.searchVal).then(res => {
          this.handleData(res.data)
        })
      }

    },
    handleData(data) {
      this.response = data
      this.freeResponse = data !== 'undefined' ? JSON.parse(JSON.stringify(data)) : []
      this.loading = false
    },
    handleSort(type) {
      this.sortKey = type
    },
    async fetchSearchTypeData() {
      this.loading = true
      const res = await searchMovieByType(this.movieType)
      this.handleData(res.data)
    },
    handleReSearch(val, type) {
      this.searchVal = val
      this.searchType = type
      this.movieType = ''
      this.$router.push(`${this.$route.path}?searchVal=${val}&searchType=${type}`)
      this.fetchSearchData()
      this.sortKey = 1
    },
    handleToDetail(id) {
      this.$router.push({
        path: '/search-detail',
        query: {
          id: id
        }
      })
    },
    shareUrl() {
      const url = window.location.href 
      var input = document.createElement('input')
      input.value = url
      document.body.appendChild(input)
      input.select() 
      document.execCommand('Copy')
      document.body.removeChild(input) 
      this.$message.success('Copy success!')
    }
  }
}
</script>

<style lang="scss" scoped>
.search {
  height: calc(100% - 90px);
  overflow: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 20px auto 0;
  &-value {
    font-weight: bold;
    font-size: 25px;
    text-align: left;
    .el-icon-document-copy {
      margin-left: 5px;
      cursor: pointer;
    }
  }
  &-result {
    flex: 1;
  }
  &-item {
    display: flex;
    gap: 20px;
    padding: 10px 0;
    border-bottom: 1px dashed rgba(0,0,0,0.15);
    &:last-child {
      border-bottom: none;
    }
    &-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 10px;
      text-align: left;
      line-height: 20px;
    }
    &-header {
      display: flex;
      align-items: baseline;
      gap: 10px;
    }
    &-title {
      font-weight: bold;
      font-size: 18px;
      line-height: 40px;
      &:hover {
        cursor: pointer;
        opacity: 0.7;
      }
    }
    &-time {
      font-size: 14px;
      color: #999;
    }
    &-introduction{
      font-style: italic;
      text-overflow: -o-ellipsis-lastline;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      -webkit-box-orient: vertical;
    }
    &-rate{
      display: flex;
      align-items: center;
      font-size: 14px;
      gap: 10px;
      &--left{
        display: flex;
        flex-direction: column;
        .primary {
          color: #000;
        }
        .soft {
          color: #666;
        }
      }
      ::v-deep .el-rate__icon{
        margin-right: 0;
      }
    }
  }
}
.search-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.search-sort {
  margin: 10px 0;
  display: flex;
  align-items: center;
  &-item{
    height: 40px;
    line-height: 40px;
    padding: 0 15px;
    color:rgba(164, 151,116, 1);    
    margin-right: 10px;
    cursor: pointer;
    &--active {
      color: #000;
      border-bottom: 2px solid rgba(164, 151,116, 1);
    }
    &:hover {
      color: #000;
    }
  }
}
::v-deep.el-image {
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
