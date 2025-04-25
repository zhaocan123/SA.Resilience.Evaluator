<template>
  <div style="height: 88vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">系统依赖图</span>
          </div>
          <p id="intro_text">
            系统依赖图（System Dependence Graph, SDG）是对过程依赖图（PDG）的扩展，
            SDG是一个有向图G=(N,E)，其中，N中的每个节点表示程序代码中的语句，而E中的每条边表示的式节点中的依赖关系。在SDG中，边分为两种类型：控制依赖边和数据依赖边。
            SDG
            可以用于表示和分析系统中各组件之间依赖关系，包括数据依赖、控制依赖等，可以帮助开发人员更好地理解系统结构和优化系统性能，提高系统的可靠性、可维护性和可扩展性。
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
          <div ref="number_of_nodes" class="text item">节点个数：</div>
          <div ref="number_of_edges" class="text item">边个数：</div>
          <div ref="max_in_degree" class="text item">最大入度：</div>
          <div ref="max_out_degree" class="text item">最大出度：</div>
          <!-- <div ref="total_data_depends" class="text item">数据依赖总数：</div>
                    <div ref="total_control_depends" class="text item">控制依赖总数：</div> -->
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">节点名称：</div>
          <div ref="node_call_num" class="text item">出度：</div>
          <div ref="node_called_num" class="text item">入度：</div>
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
      url: "/sdg.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl + "/SDG_SHOW/" + _this.$store.state.current_project.name,
      callback: (res) => {
        // console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/sdg.html";
      },
    });
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_nodes) {
          this.$refs.number_of_nodes.innerHTML = "节点个数：" + e.data.data["节点个数："];
          this.$refs.number_of_edges.innerHTML = "边个数：" + e.data.data["边个数："];
          // this.$refs.total_control_depends.innerHTML = "控制依赖总数：" + e.data.data["控制依赖总数："]
          // this.$refs.total_data_depends.innerHTML = "数据依赖总数：" + e.data.data["数据依赖总数："]
          this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "节点名称：" + e.data.data["节点名称："];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："];
        }
      }
    });

    // let params = this.$route.meta.params
    // this.url = "/graphs/sdg.html"
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
