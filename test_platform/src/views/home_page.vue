<template style="height:100%;">
  <div style="height:100%;">
    <el-container style="height:100%; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu router :default-active=$route.path>
          <el-submenu index="1">
            <template #title><i class="el-icon-message"></i>奇享盒模拟</template>
            <el-menu-item-group>
              <el-menu-item index="/home_page/creat_box">单个盒子模拟</el-menu-item>
              <el-menu-item index="/home_page/box_list">盒子模拟列表</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="1-4">
              <template #title>选项4</template>
            </el-submenu>
          </el-submenu>
          <el-submenu index="2">
            <template #title><i class="el-icon-menu"></i>导航二</template>
            <el-menu-item-group>
              <template #title>分组一</template>
              <el-menu-item index="2-1">选项1</el-menu-item>
              <el-menu-item index="2-2">选项2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="分组2">
              <el-menu-item index="2-3">选项3</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="2-4">
              <template #title>选项4</template>
              <el-menu-item index="2-4-1">选项4-1</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-submenu index="3">
            <template #title><i class="el-icon-setting"></i>导航三</template>
            <el-menu-item-group>
              <template #title>分组一</template>
              <el-menu-item index="3-1">选项1</el-menu-item>
              <el-menu-item index="3-2">选项2</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="分组2">
              <el-menu-item index="3-3">选项3</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="3-4">
              <template #title>选项4</template>
              <el-menu-item index="3-4-1">选项4-1</el-menu-item>
            </el-submenu>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item  @click="quit">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <span>奇享科技</span>
        </el-header>

        <el-main>
          <RouterView></RouterView>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  methods: {
     quit() {
        this.$confirm('吃否确认退出', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '退出成功!'
          });
          this.$router.push({name: 'login'})
          localStorage['token'] = ''
        })
      }
  },
  data() {
    return {}
  },
  mounted() {
    window.console.log(this.$route.path.split('/').reverse())
  },
  computed: {
    defaultActive() {
      return '/' + this.$route.path.split('/').reverse()[0];
    }
  },
 
};
</script>

<style scoped>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>
