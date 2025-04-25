<template>
  <div style="height: 85vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">分层架构图</span>
          </div>
          <p id="intro_text">
            分层架构模式是一种分解系统结构的技术，其将整个系统分解为一组子任务，每组子任务基于特定的抽象层次，利用分层模式可将高等级的职责分解为较细粒度的职责。换句话说，分层模式设计的系统架构是一个有组织的分层结构，其中任一层次内软件实体负责向上层软件实体提供服务并使用下层实体的服务实现自身功能。
          </p>
        </el-card></el-col
      >
    </el-row>
    <el-row style="height: 1%; width: 100%"> </el-row>
    <el-row style="height: 69%; width: 100%">
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
          <div ref="number_of_layers" class="text item">层数：</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%; overflow-y: scroll;" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">组件id:</div>
          <div ref="function_nums" class="text item">包含函数个数：</div>
          <div ref="node_functions" class="text item">包含函数：</div>
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
      url: "/level.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl +
        "/LEVEL_SHOW/" +
        _this.$store.state.current_project.name,
      callback: (res) => {
        //   console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/level.html";
      },
    });
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      console.log(e.data.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_nodes) {
          this.$refs.number_of_nodes.innerHTML = "节点个数：" + e.data.data["节点个数"];
          this.$refs.number_of_edges.innerHTML = "边个数：" + e.data.data["边个数"];
          this.$refs.number_of_layers.innerHTML = "层数：" + e.data.data["层数"];
        }
      }
      if (e.data.flag == "node") {
        if (e.data.data["type"] == "comp") {
          if (this.$refs.node_name) {
            this.$refs.node_name.innerHTML = "组件id: " + e.data.data["组件id"];
            this.$refs.function_nums.innerHTML =
              "包含函数个数：" + e.data.data["函数个数"];
            this.$refs.node_functions.innerHTML = "包含函数：" + e.data.data["包含函数"];
          }
        } else {
          if (this.$refs.node_name) {
            this.$refs.node_name.innerHTML = "当前层次：" + e.data.data["当前层次"];
            this.$refs.function_nums.innerHTML = "组件个数：" + e.data.data["组件个数"];
            this.$refs.node_functions.innerHTML = "";
          }
        }
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
