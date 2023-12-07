<template>
   <div class="wrap">
    <banner ref="banner" :show-search="false" />
    <div class="form-wrap">
      <div class="form">
        <div class="title">Register</div>
        <el-form label-position="top" label-width="80px" :model="form">
          <el-form-item label="Email">
            <el-input v-model="form.email"></el-input>
          </el-form-item>
          <el-form-item label="Name">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="Password">
            <el-input v-model="form.password"></el-input>
          </el-form-item>
        </el-form>
        <div class="submit-wrap">
          <button class="submit" @click="handleRegister">Register</button>
        </div>
      </div>
    </div>
   </div>
</template>

<script>
import Banner from '@/components/Banner/index.vue'
import { register } from '@/api'
export default {
  name: 'UserRegister',
  components: {
    Banner
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
        name: ''
      }
    }
  },
  methods: {
    async handleRegister() {
      register(this.form).then((res) => {
        if (res.success === 'true') {
          localStorage.setItem('userEmail', this.form.email)
          localStorage.setItem('isLogin', true)
          this.$message({
            message: 'Register Success',
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
