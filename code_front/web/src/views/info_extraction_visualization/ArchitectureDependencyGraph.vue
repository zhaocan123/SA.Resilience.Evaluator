<template>
  <div style="height: 85vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">系统架构依赖图</span>
          </div>
          <p id="intro_text">
            系统架构图是在系统依赖图的基础上恢复的，图中的节点是系统中的组件，组件是由一组紧密关联的函数组成，边表示组件之间的依赖关系。它提供了系统组件架构的简明描述，以协助组件与组件之间的关系和系统的运作。系统架构图是软件架构的一个可视化表示，可以清晰地表示系统中不同组件之间的关系，以便系统设计者和软件工程师更好地了解系统的架构。
          </p>
        </el-card></el-col
      >
    </el-row>
    <el-row style="height: 1%; width: 100%"> </el-row>
    <el-row style="height: 80%; width: 100%">
      <el-col :span="18" style="height: 100%">
        <div style="width: 98%; height: 100%">
          <!-- <webview :src="g_url+url" style="width:99%;height: 99%;"></webview> -->
          <iframe
            :src="g_url + url"
            style="width: 100%; height: 100%; border: none"
          ></iframe>
        </div>
      </el-col>
      <el-col :span="6" style="height: 100%">
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>图信息</span>
            </div>
          </template>
          <div ref="number_of_comps" class="text item">组件个数：</div>
          <div ref="number_of_funcs" class="text item">总函数个数：</div>
          <div ref="max_in_degree" class="text item">最大入度：</div>
          <div ref="max_out_degree" class="text item">最大出度：</div>
          <div ref="total_data_depends" class="text item">数据依赖总数：</div>
          <div ref="total_control_depends" class="text item">控制依赖总数：</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">节点名称：</div>
          <div ref="node_type" class="text item">节点类型：</div>
          <div ref="node_call_num" class="text item">出度：</div>
          <div ref="node_called_num" class="text item">入度：</div>
          <div ref="node_func_num" class="text item">包含函数个数：</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import utils from "@/utils/utils";
import config from "@/config";
export default {
  name: "GraphView",
  data() {
    return {
      g_url: window.ipConfig.baseUrl,
      url: "/comp.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl + "/COMP_SHOW/" + _this.$store.state.current_project.name,
      callback: (res) => {
        // console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/comp.html";
      },
    });
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_comps) {
          this.$refs.number_of_comps.innerHTML = "组件个数：" + e.data.data["组件个数："];
          this.$refs.number_of_funcs.innerHTML =
            "总函数个数：" + e.data.data["总函数个数："];
          this.$refs.total_control_depends.innerHTML =
            "控制依赖总数：" + e.data.data["控制依赖总数："];
          this.$refs.total_data_depends.innerHTML =
            "数据依赖总数：" + e.data.data["数据依赖总数："];
          this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "节点名称：" + e.data.data["节点名称："];
          this.$refs.node_func_num.innerHTML = e.data.data["包含函数个数："];
          this.$refs.node_type.innerHTML = "节点类型：" + e.data.data["节点类型："];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："];
        }
      }
    });
    // this.url = "/comp.html";
  },
};
</script>

<style scoped>
/*标题样式*/
.fileLevelTitle {
  /*二级标题*/
  font-size: 20px;
  font-weight: 600;
}
.textitem {
  font-size: 20px;
  font-weight: 600;
}
</style>
