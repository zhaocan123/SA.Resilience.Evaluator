<template>
  <div id="app" class="app">
    <NaviBar class="navi-bar"></NaviBar>
    <keep-alive>
      <router-view class="router-view"  v-if="$route.meta.keepAlive" />
    </keep-alive>
    <router-view class="router-view" v-if="!$route.meta.keepAlive" />
  </div>
</template>

<script>
  import NaviBar from "./components/NaviBar";

  export default {
    name: 'CQualityEvaluatorWeb',
    components: {
      NaviBar
    },
  }
</script>

<style scoped>
html, body, #app{
  /* height: 100vh;
  width: 100vw; */
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  border:0;
  display: flex;
  flex-direction: column;
}

.navi-bar{
  height: 2%;
  width: 100%;
  padding-left: 2%;
  margin-top: 1%;
}

.router-view{
  height: 97%;
  width: 100%;
}
</style>
<style>
/*通过全局CSS来修改el-tree的内部样式*/
.el-tree>.el-tree-node> .el-tree-node__content {
    font-weight: bold;
    font-size: large;
    color: #000000;
    margin-bottom: 1%;
}
.el-tree>.el-tree-node>.el-tree-node__children>.el-tree-node>.el-tree-node__content{
    font-weight: bold;
    font-size: medium;
    color: #666666;
    margin-bottom: 1%;
}
.el-tree>.el-tree-node>.el-tree-node__children>.el-tree-node>.el-tree-node__children>.el-tree-node>.el-tree-node__content{
    font-size: medium;
    margin-bottom: 1%;
}
</style>
