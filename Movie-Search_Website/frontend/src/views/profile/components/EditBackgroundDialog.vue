<template>
  <el-dialog
    title="Choose Your Home Page Background"
    width="700px"
    :visible.sync="visible"
    :show-fullscreen="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :before-close="beforeClose"
  >
  <div class="bg_wrap">
      <div class="default bg-theme1" @click="saveBackGround('1')"></div>
      <div class="default bg-theme2" @click="saveBackGround('2')"></div>
      <div class="default bg-theme3" @click="saveBackGround('3')"></div>
    </div>
  </el-dialog>
</template>
<script>
export default {
  name: 'EditBackgroundDialog',
  data() {
    return {
      visible:false,
      type: ''
    }
  },
  methods: {
    open(type) {
      this.visible = true
      this.type = type
    },
    close() {
      this.visible = false
      this.type = ''
    },
    beforeClose() {
      this.close()
    },
    saveBackGround(type) {
      this.close()
      this.$emit('saveBackGround', type)
    }
  }
}
</script>

<style lang='scss' scoped>
.bg_wrap {
  display: flex;
  justify-content: space-around;
}
.default {
  width: 200px;
  height: 150px;
  border-radius: 10px;
  border: 1px solid #eee;
  cursor: pointer;
}
</style>
