<template>
  <div style="height: 88vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">过程依赖图</span>
          </div>
          <p id="intro_text">
            过程依赖图（Procedure Dependence Graph, PDG）是一个有向图G = (V ,
            E)，V为节点集合,是语句和谓词表达式（或运算符和操作数），E为边集合表示依赖关系，依赖关系包括数据依赖和控制依赖。
            PDG明确了程序中每个操作的数据和控制依赖关系，可以帮助分析程序中语句之间的依赖关系、可达性分析和数据流分析等。通过分析PDG，可以帮助开发人员更好地理解代码的结构，提高代码的可读性和可维护性。
          </p>
        </el-card></el-col
      >
    </el-row>
    <el-row style="height: 1%; width: 100%"> </el-row>
    <el-row style="height: 80%; width: 100%">
      <el-col :span="6" style="height: 100%">
        <!--模块树-->
        <el-tree
          :data="fileTreeData"
          :props="fileProps"
          node-key="id"
          max-depth="1"
          highlight-current
          ref="tree"
          class="tree"
          accordion
          @node-click="fileNodeClick"
        >
        </el-tree>
      </el-col>
      <el-col :span="12" style="height: 100%">
        <div style="width: 98%; height: 100%">
          <!-- <webview :src="g_url+url" style="width:99%;height: 99%;"></webview> -->
          <iframe
            ref="htmlwebview"
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
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">节点语句：</div>
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
      url: "/cfg_graph.html",
      fileProps: {
        id: "id",
        children: "children",
        label: "name",
        name: "label",
        path: "path",
      },
      fileTreeData: null,
    };
  },
  methods: {
    fileNodeClick(item, data) {
      if (data.data.type == "func") {
        console.log(data.data.path);
        let _this = this;
        utils.axiosMethod({
          method: "GET",
          url:
            window.ipConfig.baseUrl +
            "/GRAPH_SHOW/" +
            _this.$store.state.current_project.name,
          params: {
            graph_type: "pdg",
            file_path: data.data.path,
            function_name: data.data.label,
          },
          callback: (res) => {
            // console.log(res)
          },
        });
        this.$refs.htmlwebview.contentWindow.postMessage(
          { path: data.data.path, flag: "update" },
          "*"
        );
        console.log("向iframe发送信息", { path: data.data.path, flag: "update" });
      }
    },
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url: window.ipConfig.baseUrl + "/PDG/" + _this.$store.state.current_project.name,
      callback: (res) => {
        //  console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/cfg_graph.html";
      },
    });

    let params = this.$route.meta.params;
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      if (e.data.flag == "graph") {
        this.$refs.number_of_nodes.innerHTML = "节点个数：" + e.data.data["节点个数："];
        this.$refs.number_of_edges.innerHTML = "边个数：" + e.data.data["边个数："];
        this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："];
        this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："];
      }
      if (e.data.flag == "node") {
        this.$refs.node_name.innerHTML = "节点语句：" + e.data.data["节点语句："];
        this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："];
        this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："];
      }
    });
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
