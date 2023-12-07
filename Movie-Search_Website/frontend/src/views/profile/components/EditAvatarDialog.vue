<template>
  <el-dialog
    title="Choose Your Avatar"
    width="700px"
    :visible.sync="visible"
    :show-fullscreen="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :before-close="beforeClose"
  >
    <div class="avatar_wrap">
      <div class="default" @click="saveAvatar('default')"></div>
      <div class="default default-female" @click="saveAvatar('female')"></div>
      <div class="default default-male" @click="saveAvatar('male')"></div>
    </div>
  </el-dialog>
</template>
<script>
export default {
  name: 'EditAvatarDialog',
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
    saveAvatar(type) {
      this.close()
      this.$emit('saveAvatar', type)
    }
  }
}
</script>

<style lang='scss' scoped>
.avatar_wrap {
  display: flex;
  justify-content: space-between;
}
.default {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: url('@/assets/home_img/default.png')  no-repeat center center  /200px;
  &-female {
    background: url('@/assets/home_img/default_female.png')  no-repeat center center  /200px;
  }
  &-male {
    background: url('@/assets/home_img/default_male.png')  no-repeat center center  /200px;
  }
}
</style>
