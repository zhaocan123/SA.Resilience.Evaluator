<template>
  <div style="height: 85vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">调用返回风格架构图</span>
          </div>
          <p id="intro_text">
            调用返回风格顾名思义，就是指在系统中采用了调用与返回机制。利用调用返回实际上是一种分而治之的策略，其主要思想是将一个复杂的大系统分解为一些子系统，以便降低复杂度，并且增加可修改性。图中每个节点都是一个组件，组件是由一组功能相似的函数组成，节点之间的边表示组件之间的调用关系。
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
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%; overflow-y: scroll;" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">组件内函数：</div>
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
      url: "/callback.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl +
        "/CALLBACK_SHOW/" +
        _this.$store.state.current_project.name,
      callback: (res) => {
        //   console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/callback.html";
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
          this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = e.data.data["节点名称："];
          this.$refs.node_func_num.innerHTML =
            "包含函数个数：" + e.data.data["包含函数个数："];
          this.$refs.node_type.innerHTML = "节点类型：" + e.data.data["节点类型："];
          this.$refs.node_call_num.innerHTML = "出度：" + e.data.data["出度："];
          this.$refs.node_called_num.innerHTML = "入度：" + e.data.data["入度："];
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
