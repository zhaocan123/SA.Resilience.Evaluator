<template>
  <div style="height: 85vh">
    <!-- <div>
            <iframe :src="g_url+url" style="width:100%;height: 90%;"></iframe>
          </div> -->
    <el-row style="height: 20%; width: 100%">
      <el-col :span="24"
        ><el-card class="box-card" style="height: 100%">
          <div slot="header" class="clearfix">
            <span class="fileLevelTitle">管道过滤器风格架构图</span>
          </div>
          <p id="intro_text">
            过滤器和管道体系结构风格为处理数据流的系统提供了一种结构。每个处理步骤封装在一个过滤器组件中。数据通过相邻过滤器之间的管道传输。每个过滤器有一组输入端和输出端。一个过滤器从输入端读取数据流,通过本地转换和渐增计算,向输出端输出数据流。管道充当数据流的通道,将一个过滤器的输出端连接到另一个过滤器的输入端。
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
          <div ref="number_of_nodes" class="text item">过滤器个数：</div>
          <div ref="number_of_edges" class="text item">管道个数：</div>
          <div ref="number_of_data_ins" class="text item">数据入口个数：</div>
          <div ref="number_of_data_outs" class="text item">数据出口个数：</div>
          <div ref="max_in_degree" class="text item">最大入度：</div>
          <div ref="max_out_degree" class="text item">最大出度：</div>
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
          <div ref="node_path" class="text item">节点所在文件：</div>
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
      url: "/pipe_filter.html",
    };
  },
  mounted() {
    let _this = this;
    utils.axiosMethod({
      method: "GET",
      url:
        window.ipConfig.baseUrl +
        "/PIPEFILTER_SHOW/" +
        _this.$store.state.current_project.name,
      callback: (res) => {
        // console.log(res)
        _this.fileTreeData = JSON.parse(JSON.stringify(res.data));
        _this.url = "/pipe_filter.html";
      },
    });
    // 接受iframe组件传过来的数据
    window.addEventListener("message", (e) => {
      console.log("接受html页面的数据", e.data);
      if (e.data.flag == "graph") {
        if (this.$refs.number_of_edges) {
          this.$refs.number_of_edges.innerHTML = "管道个数：" + e.data.data["管道个数："];
          this.$refs.max_in_degree.innerHTML = "最大入度：" + e.data.data["最大入度："];
          this.$refs.max_out_degree.innerHTML = "最大出度：" + e.data.data["最大出度："];
          this.$refs.number_of_nodes.innerHTML =
            "过滤器个数：" + e.data.data["过滤器个数："];
          this.$refs.number_of_data_ins.innerHTML =
            "数据入口个数：" + e.data.data["数据入口个数："];
          this.$refs.number_of_data_outs.innerHTML =
            "数据出口个数：" + e.data.data["数据出口个数："];
        }
      }
      if (e.data.flag == "node") {
        if (this.$refs.number_of_edges) {
          this.$refs.node_name.innerHTML = "节点名称：" + e.data.data["节点名称："];
          this.$refs.node_path.innerHTML = e.data.data["节点所在文件："];
          this.$refs.node_type.innerHTML = e.data.data["节点类型："];
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
