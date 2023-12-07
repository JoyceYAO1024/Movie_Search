<template>
  <div class="wrap" >
   <banner ref="banner" :show-search="false" />
   <div class="form-wrap">
    <div class="form">
      <div class="title">Login</div>
      <el-form label-position="top" label-width="80px" :model="form">
        <el-form-item label="Email">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
      </el-form>
      <div class="submit-wrap">
        <button class="submit" @click="handleLogin">Login</button>
      </div>
    </div>
   </div>
  </div>
</template>

<script>
import Banner from '@/components/Banner/index.vue'
import { login } from '@/api'
export default {
  name: 'UserLogin',
  components: {
    Banner
  },
  data() {
    return {
      form: {
        email: '',
        password: '' 
      }
    }
  },
  methods: {
    async handleLogin() {
      login(this.form).then((res) => {
        if (res.success === 'true') {
          localStorage.setItem('userEmail', this.form.email)
          localStorage.setItem('isLogin', true)
          this.$message({
            message: 'Login Success',
            type: 'success'
          })
          this.$router.push({
            path: '/'
          })
        } else {
          return this.$message({
            message: res.message,
            type: 'error'
          })
        }
      })

    }
  }
}
</script>

<style lang='scss' scoped>
@import '@/views/user/style/index.scss'
</style>
