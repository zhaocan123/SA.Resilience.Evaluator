<template>
  <div style="height: 88vh">
    <el-tabs type="card" v-model="activeName">
      <el-tab-pane label="函数调用图" name="funcLevel">
        <funcLevelGraph></funcLevelGraph>
      </el-tab-pane>
      <el-tab-pane label="文件调用图" name="fileLevel">
        <fileLevelGraph></fileLevelGraph>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import funcLevelGraph from "./graphs/funcLevelGraph.vue";
import fileLevelGraph from "./graphs/fileLevelGraph.vue";
export default {
  name: "GraphView",
  components: {
    funcLevelGraph,
    fileLevelGraph,
  },
  data() {
    return {
      activeName: "funcLevel",
    };
  },
  mounted() {},
};
</script>

<style scoped></style>
