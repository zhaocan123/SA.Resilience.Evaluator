<template>
  <el-container style="height: 88vh;">
    <el-header style="margin-top: 20px; height: 40px">
      <el-row type="flex">
        <el-col :span="20" style="
            font-size: 22px;
            text-align: center;
            margin-top: 5px;
          ">
          <span style="font-weight: bold">设计质量评估指标</span>
        </el-col>
        <el-col :span="4" style="font-size: 18px; text-align: left">
          <el-button type="primary" @click="goResultShow" style="margin-left: 30px">开始评估</el-button>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-table :data="this.expert_list[0].metrics" ref="singleTable" highlight-current-row
        border style="width: 100%">
        <el-table-column type="index" width="50" align="center" label="序号" min-width="5%">
        </el-table-column>
        <el-table-column prop="name" align="center" label="名称" min-width="10%">
        </el-table-column>
        <el-table-column prop="des" align="center" label="描述" min-width="20%"> </el-table-column>
        <el-table-column prop="formula" align="center" label="公式" min-width="30%">
        </el-table-column>
        <el-table-column prop="factors" align="center" label="公式因子" min-width="35%">
          <template slot-scope="scope">
            <li v-for="(value, index) in scope.row.factors" :key="index">
              <!-- {{ scope.row.factors[index] }} -->
              {{ value }}
            </li>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
import expertMetric from "@/utils/expertMetric.js";
import MathJax from "@/utils/MathJax.js";
export default {
  data() {
    return {
      expert_list: this.copyList(expertMetric.data),
      num: 0,
    };
  },
  mounted() {
    this.formatMath();
  },
  methods: {
    handleChange() {
      this.$forceUpdate();
    },
    goResultShow() {
      this.$router.push({ name: "result_show1" });
    },
    copyList(objList) {
      let newList = [];
      for (var i = 0; i < objList.length; i++) {
        newList.push(JSON.parse(JSON.stringify(objList[i])));
      }
      return newList;
    },
    formatMath() {
      let that = this;
      setTimeout(function () {
        that.$nextTick(function () {
          if (MathJax.isMathjaxConfig) {
            //判断是否初始配置，若无则配置。
            MathJax.initMathjaxConfig();
          }
          MathJax.MathQueue("MathJax"); //传入组件id，让组件被MathJax渲染
        });
      }, 500);
    },
  },
};
</script>