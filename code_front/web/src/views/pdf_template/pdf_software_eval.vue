<template>
    <div class="pdf_main" style="width:21cm;">
        <el-container>
          <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
            <el-row :gutter="24" style="height: 80% " class="detailCards">
              <h1 style="text-align: center">{{ projectName }} 项目软件质量评估结果</h1>
            </el-row>
            <el-row :gutter="24" style="height: 80% " class="detailCards">
              <h2>{{ "1.评估概况" }}</h2>
              <h3>{{ "软件总质量:"+this.totalResult }}</h3>
            </el-row>
            <el-row :gutter="24" style="height: 80% " class="detailCards">
              <div class="tree">
                <table class="assetPrintTable">
                  <!-- 重点--一定要写thead -->
                  <thead>
                  <tr>
                    <th style="font-size: 20px;font-weight: bolder;border-top: 2px solid;border-bottom: 2px solid">指标名称</th>
                    <th style="font-size: 20px;font-weight: bolder;border-top: 2px solid;border-bottom: 2px solid">指标值</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="item in tableNodes" :key="item.id">
                    <td v-if="item.level === 2" style="color: #fe441a; font-size: 20px;font-weight: bolder;border-top: 2px solid black;border-bottom: 2px solid black">{{ item.label }}</td>
                    <td v-if="item.level === 2" style="color: #fe441a; font-size: 20px;font-weight: bolder;border-top: 2px solid black;border-bottom: 2px solid black">{{ item.val }}</td>
                    <td v-if="item.level === 3" style="color: #fd942b; font-size: 18px;font-weight: bolder;border-top: 1px dashed black;border-bottom: 1px dashed black;">{{ item.label }}</td>
                    <td v-if="item.level === 3" style="color: #fd942b; font-size: 18px;font-weight: bolder;border-top: 1px dashed black;border-bottom: 1px dashed black">{{ item.val }}</td>
                    <td v-if="item.level === 4" style="color: #fce43c; font-size: 15px;font-weight: bolder;border-top: 0;border-bottom: 0">{{ item.label }}</td>
                    <td v-if="item.level === 4" style="color: #fce43c; font-size: 15px;font-weight: bolder;border-top: 0;border-bottom: 0">{{ item.val }}</td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </el-row>
            <el-row :gutter="24" style="height: 80% " class="detailCards">
              <h2>{{ "2.评估详情" }}</h2>
            </el-row>
            <el-row :gutter="24" style="height: 80% " class="detailCards" v-for="item in treeNodes[0]['subMetric']" :key="item.id">
              <h3>{{ "2."+item["pos"]+item["label"] }}</h3>
              <table class="assetPrintTable">
                <!-- 重点--一定要写thead -->
                <thead>
                <tr>
                  <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">指标</th>
                  <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">值</th>
                  <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">权重</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="i in item['sub']" :key="i.id">
                  <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.id }}</td>
                  <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.value.toFixed(2) }}</td>
                  <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.weight.toFixed(2) }}</td>
                </tr>
                </tbody>
              </table>
              <div v-for="(item1,idx) in item['subMetric']" :key="idx">
                <h4>{{ "2."+item["pos"]+"."+item1["pos"]+item1["label"] }}</h4>
                <table class="assetPrintTable">
                  <!-- 重点--一定要写thead -->
                  <thead>
                  <tr>
                    <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">指标</th>
                    <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">值</th>
                    <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">权重</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="i in item1['sub']" :key="i.id">
                    <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.id }}</td>
                    <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.value ? i.value.toFixed(2) : i.value }}</td>
                    <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.weight ? i.weight.toFixed(2) : i.weight }}</td>
                  </tr>
                  </tbody>
                </table>
                <div v-for="(item2,idx) in item1['subMetric']" :key="idx">
                  <h4>{{ "2."+item["pos"]+"."+item1["pos"]+"."+item2["pos"]+item2["label"] }}</h4>
                  <table class="assetPrintTable">
                    <!-- 重点--一定要写thead -->
                    <thead>
                    <tr>
                      <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">参数</th>
                      <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">描述</th>
                      <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">来源</th>
                      <th style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">来源类型</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="i in item2['sub']" :key="i.id">
                      <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.id }}</td>
                      <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.des }}</td>
                      <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.source }}</td>
                      <td  style="font-size: 15px;border-top: 1px solid;border-bottom: 1px solid">{{ i.type }}</td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </el-row>
          </el-main>
        </el-container>
        <el-backtop target=".pdf_main" :right="250" :bottom="60"></el-backtop>
      <!--    <div class="main">-->
      <!--      <div class="title">{{ selectedNode.label }}</div>-->
      <!--      <div class="cards" style="overflow:auto">-->
      <!--        <el-card v-if="isLeaf && card != null" class="card" shadow="hover" v-for="(card,index) in selectedNode.sub" :key="index">-->
      <!--          <div slot="header" class="card-header">-->
      <!--            <el-col :span="12">-->
      <!--              <div>{{ card.id }}</div>-->
      <!--            </el-col>-->
      <!--            <el-col :span="12">-->
      <!--              <div style="text-align: right;">{{ card.val ? card.val.toFixed(2) : card.val }}</div>-->
      <!--            </el-col>-->
      <!--          </div>-->
      <!--          <div class="card-item">-->
      <!--            <el-row>-->
      <!--              <el-col :span="12">-->
      <!--                <div>描述</div>-->
      <!--              </el-col>-->
      <!--              <el-col :span="12">-->
      <!--                <div class="text">{{ card.des }}</div>-->
      <!--              </el-col>-->
      <!--            </el-row>-->
      <!--          </div>-->
      <!--          <div class="card-item">-->
      <!--            <el-row>-->
      <!--              <el-col :span="12">-->
      <!--                <div>来源</div>-->
      <!--              </el-col>-->
      <!--              <el-col :span="12">-->
      <!--                <div class="text">{{ card.source }}</div>-->
      <!--              </el-col>-->
      <!--            </el-row>-->
      <!--          </div>-->
      <!--          <div class="card-item">-->
      <!--            <el-row>-->
      <!--              <el-col :span="12">-->
      <!--                <div>来源类型</div>-->
      <!--              </el-col>-->
      <!--              <el-col :span="12">-->
      <!--                <div class="text">{{ card.type }}</div>-->
      <!--              </el-col>-->
      <!--            </el-row>-->
      <!--          </div>-->
      <!--        </el-card>-->
  
      <!--        <el-card v-if="!isLeaf && card != null" class="card" shadow="hover" v-for="(card,index) in selectedNode.sub" :key="index">-->
      <!--          <div slot="header" class="card-header">-->
      <!--            <el-col :span="12">-->
      <!--              <div>{{ card.id }}</div>-->
      <!--            </el-col>-->
      <!--            <el-col :span="12">-->
      <!--              <div style="text-align: right;">{{ card.val }}</div>-->
      <!--            </el-col>-->
      <!--          </div>-->
      <!--          <div class="card-item">-->
      <!--            <el-row>-->
      <!--              <el-col :span="12">-->
      <!--                <div>值</div>-->
      <!--              </el-col>-->
      <!--              <el-col :span="12">-->
      <!--                <div style="text-align: right;">{{ card.value ? card.value.toFixed(2) : card.value }}</div>-->
      <!--              </el-col>-->
      <!--            </el-row>-->
      <!--          </div>-->
      <!--          <div class="card-item">-->
      <!--            <el-row>-->
      <!--              <el-col :span="12">-->
      <!--                <div>权重</div>-->
      <!--              </el-col>-->
      <!--              <el-col :span="12">-->
      <!--                <div style="text-align: right;">{{ card.weight ? card.weight.toFixed(2) : card.weight }}-->
      <!--                </div>-->
      <!--              </el-col>-->
      <!--            </el-row>-->
      <!--          </div>-->
      <!--        </el-card>-->
      <!--      </div>-->
      <!--    </div>-->
    </div>
  </template>
  
  <script>
  import Cache from  "@/utils/cache"
  
  export default {
    data() {
      return {
        projectName: this.$store.state.current_project.name,
        treeNodes: [],
        tableNodes: [],
        defaultProps: {
          label: 'label',
          children: 'subMetric'
        },
        selectedNode: {
          label: "请选择指标",
          sub: []
        },
        totalResult:null,
        isLeaf: false,
        dialogFormVisible: true,
        minMaxIndexList: {},
        minMaxData: {},
        minMaxRes: {}
      }
    },
    mounted() {
      let _this = this
      let data0 = Cache.getCache("software_eval")
      let tableNodes = []
      let flag = 1
      for (let data1 of data0) {
        tableNodes.push({
          id: flag,
          label: data1.name,
          val: data1.val.toFixed(2),
          level: 1
        })
        this.totalResult = data1.val.toFixed(2)
        for (let data2 of data1.subMetric) {
          tableNodes.push({
            id: flag,
            label: data2.name,
            val: data2.val.toFixed(2),
            level: 2
          })
          for (let data3 of data2.subMetric) {
            tableNodes.push({
              id: flag,
              label: data3.name,
              val: data3.val.toFixed(2),
              level: 3
            })
            for (let data4 of data3.subMetric) {
              if (data4.val != null) {
                tableNodes.push({
                  id: flag,
                  label: data4.name,
                  val: data4.val.toFixed(2),
                  level: 4
                })
                flag++
              }
            }
            flag++
          }
  
          flag++
        }
  
        flag++
      }
      flag++
      let treeNodes = []
      for (let data1 of data0) {
        let treeNodes1 = []
        let level1_id = 1;
        for (let data2 of data1.subMetric) {
          let treeNodes2 = []
          let level2_id = 1;
          for (let data3 of data2.subMetric) {
            let level3_id = 1;
            let treeNodes3 = []
            for (let data4 of data3.subMetric) {
              if(data4.val != null) {
                treeNodes3.push({
                  id: flag,
                  label: data4.name,
                  isLeaf: true,
                  sub: data4.sub,
                  pos:level3_id
                })
                level3_id++
                flag++
              }
            }
            treeNodes2.push({
              id: flag,
              label: data3.name,
              isLeaf: false,
              sub: data3.sub,
              subMetric: treeNodes3,
              pos:level2_id
            })
            level2_id++
            flag++
          }
          treeNodes1.push({
            id: flag,
            label: data2.val != null ? data2.name + " — " + data2.val.toFixed(2) : data2.name,
            isLeaf: false,
            sub: data2.sub,
            subMetric: treeNodes2,
            pos:level1_id
          })
          level1_id++
          flag++
        }
        treeNodes.push({
          id: flag,
          label: data1.name,
          isLeaf: false,
          sub: data1.sub,
          subMetric: treeNodes1
        })
        flag++
      }
      _this.tableNodes = tableNodes
      _this.treeNodes = treeNodes
      console.log(_this.treeNodes)
    },
    methods: {
      getIndexSubInfo() {
        let data = this.minMaxRes
        let minMaxData = this.minMaxData
        for (let k1 in data) {
          let data1 = data[k1]
          for (let k2 in data1) {
            let data2 = data1[k2]
            for (let k3 in data2) {
              let data3 = data2[k3]
              if (k3 in minMaxData) {
                data3.min = minMaxData[k3].min
                data3.max = minMaxData[k3].max
              }
            }
          }
        }
  
      }, print() {
        this.$print(this.$refs.print)
        //因为每次打印都会多一个img（将echarts的canvas转为img），我的print.js里头已经配置给这个img里头加的classname为isNeedRemove，所以每次打印完需去除，我只有一张echarts、去除的数量根据业务需求定。
        this.$nextTick(() => {
          let arr = document.getElementsByClassName('isNeedRemove')
          while (arr.length) {
            arr[0].remove()
          }
        })
      },
      handleNodeClick(e) {
        this.selectedNode = e
        // console.log("selectedNode", this.selectedNode)
        this.isLeaf = e.isLeaf
      }
    },
  }
  </script>
  
  <style scoped>
  
  .tree {
    height: 100%;
    width: 100%;
  }
  
  .el-tree {
    width: 100%;
    margin-top: 2%;
  }
  
  .tree-node {
    margin-left: 1%;
  }
  
  .main {
    height: 100%;
    width: 50%;
    display: flex;
    flex-direction: column;
  }
  
  .title {
    height: 10%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: x-large;
  }
  
  .cards {
    height: 85%;
    overflow: auto;
  }
  
  .card {
    height: auto;
    width: 60%;
    margin: 2% auto;
  }
  
  .card-header {
    font-weight: bolder;
    padding-bottom: 10%;
    font-size: medium;
    color: rgb(244, 70, 163);
  }
  
  .card-item {
    margin-bottom: 2%;
    font-size: small;
  }
  
  .text {
    text-align: right;
    word-break: break-all;
    word-wrap: break-word;
  }
  
  .titleIndex {
    font-size: medium;
    font-weight: bold;
    margin-bottom: 8px;
  }
  
  .file_select {
    margin-bottom: 3vh;
  }
  
  .button {
    z-index: 3;
    position: absolute;
    right: 2vw;
  }
  
  .assetPrintTable {
    width: 100%;
    border-collapse: collapse;
    border-spacing: 0;
    border: 0;
    border-bottom: solid;
    border-top: solid;
  }
  
  tr {
    page-break-inside: avoid;
  }
  
  th, td {
    width: 150px;
    border-bottom: 1px solid #e4e7ed;
    padding: 10px;
    text-align: center;
  }
  
  th {
    background-color: #f5f7fa;
  }
  
  @page {
    size: auto;
    margin: 3mm;
  
  }
  
  @media print {
  
    .assetPrintTable {
      width: 100%;
      border-collapse: collapse;
      border-spacing: 0;
    }
  
    tr {
      page-break-inside: avoid;
    }
  
    th, td {
      width: 150px;
      padding: 10px;
      text-align: center;
    }
  
    th {
      background-color: #f5f7fa;
    }
  }
  
  
  </style>
  
  
  