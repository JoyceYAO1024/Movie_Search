const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api/*': {
        target: 'http://127.0.0.1:5000/', // dev post
        changeOrigin: true, // 跨域
        pathRewrite: {
          '^/api': '' // rewrite url
        }
      }
    }
  }
})
