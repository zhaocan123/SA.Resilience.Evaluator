<template>
  <div>
    <el-row>
      <el-button class="button" type="primary" style="position: absolute; right: 10px; z-index: 10;" @click="dialogPdfVisible = true">打印</el-button>
      
      <el-tabs type="card" v-model="activeName1" @tab-click="tabClick">
        <el-tab-pane label="C信息" name="c_info" v-if="projectType != 1"></el-tab-pane>
        <el-tab-pane
          label="C++信息"
          name="c_plus_info"
          v-if="projectType != 0"
        ></el-tab-pane>
      </el-tabs>
    </el-row>
    <el-row v-loading="loading" type="flex">
      <el-col :span="24">
        <el-button
          type="primary"
          @click="dialogFormVisible = true"
          style="margin-left: 25px; margin-bottom: 10px"
          plain
          >阈值设置</el-button
        >
        
       
        <el-tabs tab-position="left">
          <el-tab-pane label="统计信息">
            <StatisticInfo :key="key1" :typeName="activeName1"></StatisticInfo>
          </el-tab-pane>
          <el-tab-pane label="检测结果">
            <DetectionResult :key="key1" :typeName="activeName1"></DetectionResult>
          </el-tab-pane>
        </el-tabs>

        <el-dialog width="35%" title="指标阈值设置" :visible.sync="dialogFormVisible">
          <div class="file_select">
            <el-button
              slot="trigger"
              class="el-button"
              type="success"
              @click="importFile"
              plain
              >导入模板</el-button
            >
            <el-button
              slot="trigger"
              class="el-button"
              type="primary"
              @click="exportFile"
              plain
              >导出数据</el-button
            >
          </div>
          <div class="form">
            <el-form :model="threshold">
              <el-checkbox class="checkbox" v-model="threshold_checked_list.overLongFunc">
                <el-form-item label="长函数" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.overLongFunc"
                    v-model="threshold.overLongFunc"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-model="threshold_checked_list.overLongParam"
              >
                <el-form-item label="长参数" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.overLongParam"
                    v-model="threshold.overLongParam"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-model="threshold_checked_list.overCommentLineFile"
              >
                <el-form-item label="注释过多" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.overCommentLineFile"
                    v-model="threshold.overCommentLineFile"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox class="checkbox" v-model="threshold_checked_list.overDeepCall">
                <el-form-item label="过深调用" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.overDeepCall"
                    v-model="threshold.overDeepCall"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-model="threshold_checked_list.overInOutDegreeFunc"
              >
                <el-form-item label="扇入扇出" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.overInOutDegreeFunc"
                    v-model="threshold.overInOutDegreeFunc"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox class="checkbox" v-model="threshold_checked_list.textCopy">
                <el-form-item label="代码克隆" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 100%"
                    resize="both"
                    oninput="if(value == '' || value < 0 || value > 1) value = 0; if(value == 1) value = Number(value)"
                    :disabled="!threshold_checked_list.textCopy"
                    v-model="threshold.textCopy"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :max="1"
                    :min="0"
                    :step="0.1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-model="threshold_checked_list.overCyclComplexityFunc"
              >
                <el-form-item label="圈复杂度" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.overCyclComplexityFunc"
                    v-model="threshold.overCyclComplexityFunc"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-if="this.$store.state.current_project.projectType != 0"
                v-model="threshold_checked_list.lazyClass"
              >
                <el-form-item label="冗赘类" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.lazyClass"
                    v-model="threshold.lazyClass"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-if="this.$store.state.current_project.projectType != 0"
                v-model="threshold_checked_list.LargeClass"
              >
                <el-form-item label="过大的类" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.LargeClass"
                    v-model="threshold.LargeClass"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-if="this.$store.state.current_project.projectType != 0"
                v-model="threshold_checked_list.ShotgunSurgery"
              >
                <el-form-item label="散弹式修改" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.ShotgunSurgery"
                    v-model="threshold.ShotgunSurgery"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-if="this.$store.state.current_project.projectType != 0"
                v-model="threshold_checked_list.FeatureEnvy"
              >
                <el-form-item label="依赖情节" label-width="auto">
                  <el-input
                    type="number"
                    style="width: 60%"
                    resize="both"
                    oninput="value = Number(value) || 0"
                    :disabled="!threshold_checked_list.FeatureEnvy"
                    v-model="threshold.FeatureEnvy"
                    placeholder="请输入阈值"
                    controls-position="right"
                    @change="handleChange"
                    :min="1"
                  ></el-input>
                </el-form-item>
              </el-checkbox>

              <el-checkbox
                class="checkbox"
                v-if="this.$store.state.current_project.projectType != 0"
                v-model="threshold_checked_list.DataClass"
              >
                <span style="margin-left: 1.5vw">纯数据类</span>
              </el-checkbox>
            </el-form>
          </div>

          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="setThreshold()">确 定</el-button>
          </div>
        </el-dialog>
        
        <el-dialog title="pdf预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
          <pdf_bad_ratio_calculation v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_bad_ratio_calculation>
          <span slot="footer" class="dialog-footer">
              <el-button @click="dialogPdfVisible = false">取 消</el-button>
              <el-button type="primary" @click="goPrint">打 印</el-button>
          </span>
      </el-dialog>
        
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Cache from "@/utils/cache.js";
import utils from "../../utils/utils";
import config from "../../config";
import StatisticInfo from "./result/statistic_information.vue";
import DetectionResult from "./result/detection_result.vue";
import FileSaver from "file-saver";
import pdf_bad_ratio_calculation from "@/views/pdf_template/pdf_bad_ratio_calculation.vue"

export default {
  components: {
    StatisticInfo,
    DetectionResult,
    pdf_bad_ratio_calculation,
  },
  data() {
    return {
      dialogPdfVisible: false,
      projectType: 0,
      projectName: null,
      activeName1: "c_info",
      dialogFormVisible: true,
      loading: false,
      // projectType: this.$store.state.current_project.projectType,
      threshold: {
        //C
        overLongFunc: 1, // 长函数
        overLongParam: 1, // 长参数
        overCommentLineFile: 1, // 注释过多
        overDeepCall: 1, // 过深调用
        overInOutDegreeFunc: 1, // 扇入扇出
        textCopy: 0.1, // 代码克隆
        overCyclComplexityFunc: 1, // 圈复杂度
        //CPP
        lazyClass: 1, // 冗赘类
        LargeClass: 1, // 过大的类
        ShotgunSurgery: 1, // 散弹式修改
        FeatureEnvy: 1, // 依赖情节
        DataClass: true, // 纯数据类
      },
      threshold_checked_list: {
        //C
        overLongFunc: false,
        overLongParam: false,
        overCommentLineFile: false,
        overDeepCall: false,
        overInOutDegreeFunc: false,
        textCopy: false,
        overCyclComplexityFunc: false,
        //CPP
        lazyClass: false,
        LargeClass: false,
        ShotgunSurgery: false,
        FeatureEnvy: false,
        DataClass: false,
      },
      // name: {
      //   overLongFunc: "函数长度", // 函数长度阈值
      //   overLongParam: "函数参数列表长度", // 函数参数列表长度阈值
      //   overCommentLineFile: "文件注释行数", // 文件注释行数阈值
      //   overDeepCall: "函数调用深度", // 函数调用深度阈值
      //   overInOutDegreeFunc: "函数入度", // 函数入度阈值
      //   textCopy: "代码克隆", // 代码克隆阈值
      //   overCyclComplexityFunc: "函数圈复杂度", // 函数圈复杂度阈值
      // },
      key1: true,
      totalData: null,
    };
  },
  mounted() {
    this.projectType = this.$store.state.current_project.projectType;
    this.projectName = this.$store.state.current_project.name;
    this.activeName1 = this.projectType == 1 ? "c_plus_info" : "c_info";
  },
  methods: {
    goPrint() {
            this.$print(this.$refs.print)
            this.dialogPdfVisible = false
    },
    
    handleChange() {
      this.$forceUpdate();
    },
    getData(data) {
      if (data == null) {
        return;
      }
      Cache.setCache(this.projectName + "_statisticTable", data[this.activeName1].statisticTable);
      Cache.setCache(this.projectName + "_badtotalResult", data);
      let cardData = {
        DT: data[this.activeName1].DT,
        NPF: data[this.activeName1].NPF,
        NCFBS: data[this.activeName1].NCFBS,
        NCF: data[this.activeName1].NCF,
        RNCF: data[this.activeName1].RNCF, //百分比
        RNCFBS: data[this.activeName1].RNCFBS, //百分比
      };
      Cache.setCache(this.projectName + "_cardData", cardData);
      Cache.setCache(this.projectName + "_fileBadvalue", data[this.activeName1].fileBadvalue);
      Cache.setCache(this.projectName + "_badSmellKindNum", data[this.activeName1].result);
      this.dialogFormVisible = false;
      this.key1 = !this.key1;
      this.loading = false;
    },
    setThreshold() {
      this.dialogFormVisible = false;
      this.loading = true;
      let _this = this;
      let threshold = {};
      for (let k in this.threshold_checked_list) {
        if (this.threshold_checked_list[k]) {
          threshold[k] = this.threshold[k];
        }
      }
      utils.axiosMethod({
        method: "POST",
        url:
          window.ipConfig.baseUrl +
          "/bad_ratio_detect/setThreshold/" +
          _this.$store.state.current_project.name,
        data: threshold,
        callback: (response) => {
          // console.log("res", response.data)
          _this.totalData = response.data;
          _this.getData(response.data);
        },
        catch: (err) => {
          _this.$message.error("获取坏味率数据失败");
        },
      });
    },
    tabClick(item) {
      this.getData(this.totalData);
    },
    // verifyFile(data){

    // },
    importFile() {
      let _this = this;
      const inputFile = document.createElement("input");
      inputFile.type = "file";
      inputFile.style.display = "none";
      inputFile.id = "fileInput";
      // inputFile.webkitdirectory = false
      // inputFile.multiple = false
      document.body.appendChild(inputFile);
      inputFile.click();
      inputFile.addEventListener("change", function (e) {
        let file = inputFile.files[0];
        // console.log("#########", file)
        if (file.type != "application/json") {
          _this.$message.error("上传文件要求为json格式");
          return;
        }
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => {
          // console.log("文件内容", JSON.parse(reader.result))
          let data = null;
          try {
            data = JSON.parse(reader.result);
          } catch (e) {
            _this.$message.error("上传文件解析错误");
            return;
          }
          // 逐个字段赋值，防止json格式非法
          for (let k in _this.threshold) {
            if (k in data.threshold) {
              _this.threshold[k] = data.threshold[k];
            }
            if (k in data.threshold_checked_list) {
              _this.threshold_checked_list[k] = data.threshold_checked_list[k];
            }
          }
        };
      });
    },
    exportFile() {
      let data = {
        threshold: this.threshold,
        threshold_checked_list: this.threshold_checked_list,
      };
      let blob = new Blob([JSON.stringify(data)], {
        type: "application/json",
      });
      let downloadName = "threshold_bad_ratio_detect_" + new Date().getTime() + ".json";
      FileSaver.saveAs(blob, downloadName);
    },
  },
};
</script>

<style scoped>
.checkbox {
  display: block;
}

::v-deep .el-dialog .el-dialog__body {
  /* display: flex; */
  justify-content: center;
  align-items: center;
}

.file_select {
  margin-bottom: 2vh;
  margin-left: 1vw;
}

.form {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
