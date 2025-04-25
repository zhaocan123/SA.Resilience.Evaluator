<template>
  <div style="height: 80vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">类图</span>
          </div>
          <p id="intro_text">
            类图(Class
            diagram)是显示了模型的静态结构，特别是模型中存在的类、类的内部结构以及它们与其他类的关系等。类图不显示暂时性的信息。类图是面向对象建模的主要组成部分。它既用于应用程序的系统分类的一般概念建模，也用于详细建模，将模型转换成编程代码。类图也可用于数据建模。
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
          <div ref="Class_count" class="text item">Class个数:</div>
          <div ref="Struct_count" class="text item">Struct个数:</div>
          <div ref="Union_count" class="text item">Union个数:</div>
        </el-card>
        <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>当前节点信息</span>
            </div>
          </template>
          <div ref="node_name" class="text item">节点名称：</div>
          <div ref="node_type" class="text item">节点类型：</div>
          <div ref="mem_var" class="text item">成员变量：</div>
          <div ref="mem_method" class="text item">成员函数：</div>
          <div ref="base" class="text item">基类：</div>
          <div ref="file" class="text item">文件路径：</div>
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
      url: "/Class.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl +
        "/CLASS_SHOW/" +
        _this.$store.state.current_project.name,
      callback: (res) => {
        //   console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/Class.html";
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
          this.$refs.Class_count.innerHTML = "Class个数: " + e.data.data["Class个数"];
          this.$refs.Struct_count.innerHTML = "Struct个数: " + e.data.data["Struct个数"];
          this.$refs.Union_count.innerHTML = "Union个数: " + e.data.data["Union个数"];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.node_name) {
          this.$refs.node_name.innerHTML = "文件名称：" + e.data.data["节点名称"];
          this.$refs.node_type.innerHTML = "节点类型：" + e.data.data["节点类型"];
          this.$refs.mem_var.innerHTML = "成员变量：" + e.data.data["成员变量"];
          this.$refs.mem_method.innerHTML = "成员函数：" + e.data.data["成员函数"];
          this.$refs.base.innerHTML = "基类：" + e.data.data["基类"];
          this.$refs.file.innerHTML = "文件路径：" + e.data.data["位置"];
        }
      }
    });

    let params = this.$route.meta.params;
    // this.url = "/Class.html";
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
