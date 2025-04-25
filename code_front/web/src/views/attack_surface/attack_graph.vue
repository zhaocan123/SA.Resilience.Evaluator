<template>
    <div style="height: 85vh">
      <!-- <div>
              <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
            </div> -->
      <el-row style="height: 20%; width: 100%">
        <el-col :span="24"
          ><el-card class="box-card" style="height: 100%">
            <div slot="header" class="clearfix">
              <span class="fileLevelTitle">攻击面可视化</span>
            </div>
            <p id="intro_text">
              可视化显示系统架构攻击面以及潜在攻击集合信息
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
                <span>信息概况</span>
              </div>
            </template>
            <div ref="number_of_nodes" class="text item">系统节点个数：</div>
            <div ref="number_of_attack_nodes" class="text item">攻击面节点个数：</div>
            <div ref="number_of_category_attacks" class="text item">潜在攻击种类：</div>
            <div ref="number_of_attacks" class="text item">潜在攻击总数：</div>
          </el-card>
          <el-card class="box-card" style="width: 99%; height: 50%" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>当前节点信息</span>
              </div>
            </template>
            <div ref="node_name" class="text item">节点名称：</div>
            <div ref="node_type" class="text item">节点类型：</div>
            <div ref="node_attack_num" class="text item">潜在攻击数：</div>
            <div ref="node_attack_prob" class="text item">被攻击概率：</div>
            <div ref="node_resilience" class="text item">节点韧性：</div>
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
        url: "/attack.html",
      };
    },
    mounted() {
      let _this = this;
      utils.axiosMethod({
        method: "GET",
        url:
          window.ipConfig.baseUrl + "/ATTACK_SHOW/" + _this.$store.state.current_project.name,
        callback: (res) => {
          // console.log(res)
          _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
          _this.url = "/attack.html";
        },
      });
      // 接受iframe组件传过来的数据
      window.addEventListener("message", (e) => {
        console.log("接受html页面的数据", e.data);
        console.log(e.data.flag)
        if (e.data.flag == "graph") {
          if (this.$refs.number_of_nodes) {
            console.log(e.data.data)
            this.$refs.number_of_nodes.innerHTML = "系统节点个数：" + e.data.data["number_of_nodes"]
            this.$refs.number_of_attack_nodes.innerHTML = "攻击面节点个数：" + e.data.data["number_of_attack_nodes"]
            this.$refs.number_of_category_attacks.innerHTML = "潜在攻击种类：" + e.data.data["number_of_category_attacks"]
            this.$refs.number_of_attacks.innerHTML = "潜在攻击总数：" + e.data.data["number_of_attacks"]
            
          }
        }
        else {
          if (this.$refs.node_name) {
            this.$refs.node_name.innerHTML = "节点名称：" + e.data.data["node_name"];
            this.$refs.node_type.innerHTML = "节点类型：" + e.data.data["node_type"];
            if(e.data.flag == "attack"){
              this.$refs.node_attack_num.innerHTML = "攻击数量：" + e.data.data["node_attack_num"];
              this.$refs.node_attack_prob.innerHTML = "攻击严重程度：" + e.data.data["attack_severity"];
              this.$refs.node_resilience.innerHTML = "攻击发生概率：" + e.data.data["attack_prob"];
            }
            else{
              this.$refs.node_attack_num.innerHTML = "" // "潜在攻击数：" + e.data.data["node_attack_num"];
              this.$refs.node_attack_prob.innerHTML = "" // "被攻击概率：" + e.data.data["node_attack_prob"];
              this.$refs.node_resilience.innerHTML = "节点韧性：" + e.data.data["node_resilience"];
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
  