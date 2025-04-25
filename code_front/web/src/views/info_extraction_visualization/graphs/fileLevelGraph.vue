<template>
  <div style="height: 80vh">
    <!-- <div>
          <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
        </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">文件级调用图</span>
          </div>
          <p id="intro_text">
            文件级调用图(FLCG)中，每个节点表示C语言项目中的一个文件，边表示两个文件之间存在的调用关系
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
            style="height: 100%; width: 100%; border: none"
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
          <div ref="header_node_count" class="text item">头文件个数：</div>
          <div ref="C_node_count" class="text item">C语言文件个数：</div>
          <div ref="Cpp_node_count" class="text item">C++文件个数：</div>
          <div ref="max_in_degree" class="text item">最大入度：</div>
          <div ref="max_out_degree" class="text item">最大出度：</div>
          <div ref="max_call_depth" class="text item">最大调用深度：</div>
          <div ref="min_call_depth" class="text item">最小调用深度：</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">文件名称：</div>
          <div ref="node_call_num" class="text item">出度：</div>
          <div ref="node_called_num" class="text item">入度：</div>
          <div ref="node_path" class="text item">文件路径：</div>
          <div ref="func_num" class="text item">包含函数个数：</div>
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
      url: "/FLCG.dot.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl +
        "/FILE_CG_SHOW/" +
        _this.$store.state.current_project.name,
      params: {
        graph_type: "cg",
        //file_path: data.data.path,
      },
      callback: (res) => {
        // console.log(res)
      },
    });
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      console.log(e.data.data);
      if (e.data.flag == "file_graph") {
        if (this.$refs.number_of_nodes) {
          this.$refs.number_of_nodes.innerHTML = "节点个数：" + e.data.data["节点个数"];
          this.$refs.number_of_edges.innerHTML = "边个数：" + e.data.data["边个数"];
          this.$refs.header_node_count.innerHTML =
            "头文件个数：" + e.data.data["头文件个数"];
          this.$refs.C_node_count.innerHTML =
            "C语言文件个数：" + e.data.data["C语言文件个数"];
          this.$refs.Cpp_node_count.innerHTML =
            "C++文件个数：" + e.data.data["C++文件个数"];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度文件"];
          this.$refs.max_out_degree.innerHTML =
            "最大出度：" + e.data.data["最大出度文件"];
          this.$refs.max_call_depth.innerHTML =
            "最大调用深度：" + e.data.data["最大调用深度"];
          this.$refs.min_call_depth.innerHTML =
            "最小调用深度：" + e.data.data["最小调用深度"];
        }
      }
      if (e.data.flag == "file_node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "文件名称：" + e.data.data["节点名称"];
          this.$refs.node_path.innerHTML = "文件路径：" + e.data.data["节点文件路径"];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度"];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度"];
          this.$refs.func_num.innerHTML = "包含函数个数：" + e.data.data["包含函数个数"];
        }
      }
    });

    let params = this.$route.meta.params;
    // this.url = "/FLCG.dot.html";
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
