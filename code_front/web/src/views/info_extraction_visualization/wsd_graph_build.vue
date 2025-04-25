<template>
    <div style="height: 85vh">
      <!-- <div>
              <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
            </div> -->
      <el-row style="height: 20%; width: 100%">
        <el-col :span="24"><el-card class="box-card" style="height: 100%">
            <div slot="header" class="clearfix">
              <span class="fileLevelTitle">UML架构视图</span>
            </div>
            <p id="intro_text">
              可视化显示系统架构UML图信息
            </p>
          </el-card></el-col>
      </el-row>
      <el-row style="height: 1%; width: 100%"> </el-row>
      <el-row style="height: 80%; width: 100%">
        <el-col :span="12" style="height: 100%">
          <div style="width: 98%; height: 100%">
            <iframe
              :src="g_url + url_activity"
              style="width: 100%; height: 100%; border: none"></iframe>
          </div>
        </el-col>
        <!-- <el-col :span="3" style="height: 100%">
          <el-card class="box-card" style="width: 99%; height: 99%" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>活动图信息概况</span>
              </div>
            </template>
            <div ref="number_of_activity_nodes" class="text item">系统节点个数：</div>
          </el-card>
        </el-col> -->
        <el-col :span="12" style="height: 100%">
          <div style="width: 98%; height: 100%">
            <iframe
              :src="g_url + url_comp"
              style="width: 100%; height: 100%; border: none"></iframe>
          </div>
        </el-col>
        <!-- <el-col :span="3" style="height: 100%">
          <el-card class="box-card" style="width: 99%; height: 99%" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>组件图信息概况</span>
              </div>
            </template>
            <div ref="number_of_compnodes" class="text item">组件节点个数：</div>
            <div ref="number_of_dependencies" class="text item">依赖边个数：</div>
            <div ref="number_of_interface" class="text item">接口个数：</div>
          </el-card>
        </el-col> -->
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
        url_activity: "/activity_uml.html",
        url_comp: "/comp_uml.html",
      };
    },
    mounted() {
      let _this = this;
      utils.axiosMethod({
        method: "GET",
        url:
          window.ipConfig.baseUrl + "/UML_SHOW/" + _this.$store.state.current_project.name,
        callback: (res) => {
          // console.log(res)
          // _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
          _this.url_activity = "/activity_uml.html";
          _this.url_comp = "/comp_uml.html";
        },
      });
      // 接受iframe组件传过来的数据
      window.addEventListener("message", (e) => {
        console.log("接受html页面的数据", e.data);
        if (e.data.flag == "activity") {
          if (this.$refs.number_of_comps) {
            this.$refs.number_of_activity_nodes.innerHTML = "系统节点个数：" + e.data.data["number_of_activity_nodes"]
          }
        }
        if (e.data.flag == "comp") {
          if (this.$refs.number_of_comps) {
            this.$refs.number_of_compnodes.innerHTML = "组件节点个数：" + e.data.data["number_of_compnodes"]
            this.$refs.number_of_dependencies.innerHTML = "依赖边个数：" + e.data.data["number_of_dependencies"]
            this.$refs.number_of_interface.innerHTML = "接口个数：" + e.data.data["number_of_interface"]
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
  