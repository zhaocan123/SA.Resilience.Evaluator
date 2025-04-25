<template>
    <div class="pdf_main" style="width: 21cm;">
        <div>
          <el-container style="height: 29.7cm;;page-break-after: always;">
            <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
              <el-row :gutter="16" style="height: 40% ">
                <h1 style="text-align: center">{{ this.projectName + "项目级信息" }}</h1>
                <h3>1.源码信息概况</h3>
                <el-col :span="24" style="height: 100% ">
                  <div ref="myChart" class="chart"></div>
                </el-col>
              </el-row>
              <el-row :gutter="16" style="height: 50% ;width:100%;">
                <el-col :span="24" style="height: 100% ">
                  <div class="table1">
                    <el-table :data="tableData1"  :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
                      <!-- <el-table-column
                          prop="dirNumber"
                          label="文件夹"
                          align="center">
                      </el-table-column> -->
                      <el-table-column prop="fileNumber" label="文件" align="center">
                      </el-table-column>
                      <el-table-column prop="functionNumber" label="函数" align="center">
                      </el-table-column>
                    </el-table>
                  </div>
                  <div class="table2"  style="margin-top: 20px">
                    <el-table :data="tableData2" :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
                      <el-table-column prop="codeLine" label="代码行" align="center">
                      </el-table-column>
                      <el-table-column prop="codeLineExp" label="有效代码行" align="center">
                      </el-table-column>
                      <el-table-column prop="commentLine" label="注释行" align="center">
                      </el-table-column>
                      <el-table-column prop="commentLineExp" label="有效注释行" align="center">
                      </el-table-column>
                    </el-table>
                  </div>
                  <div class="table3" style="margin-top: 20px">
                    <el-table :data="tableData3" :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}">
                      <el-table-column prop="codeLineExpProp" label="有效代码行占比" align="center">
                      </el-table-column>
                      <el-table-column prop="emptyLineProp" label="空行占比" align="center">
                      </el-table-column>
                      <el-table-column prop="commentLineExpProp" label="有效注释行占比" align="center">
                      </el-table-column>
                    </el-table>
  
                  </div>
                </el-col>
              </el-row>
            </el-main>
  
          </el-container>
  
  
        </div>
        <div >
          <el-container style="height: 29.7cm;;page-break-after: always;">
            <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
              <div v-if="projectType != 1">
                <h3>2.C信息概况</h3>
                <div class="cards" style="width:100%">
                    <el-card class="card" shadow="hover">
                        <div slot="header" style="font-weight: bolder;">
                            <span>{{ mainInfo.fileType }}</span>
                        </div>
                        <div class="card-item">
                            <el-row style="color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ mainInfo.fileProp_k }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ mainInfo.fileProp }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ mainInfo.totalNum_k }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ mainInfo.totalNum }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        </el-card>
                        <el-card class="card" shadow="hover" v-for="(card, index) in cardInfo" :key="index">
                        <div slot="header" style="font-weight: bolder;">
                            <span>{{ card.title }}</span>
                        </div>
                        <div class="card-item">
                            <el-row style=" color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ card.key1 }}</div>
                            </el-col>
                            <!--    <el-col :span="12">
                                <div style="text-align: right;">{{ card.val1 }}</div>
                            </el-col> -->
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ card.msg }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val1 }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="">
                            <el-col :span="12">
                                <div>{{ card.key2 }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val2 }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        <div class="card-item" style="">
                            <el-row>
                            <el-col :span="12">
                                <div>{{ card.key3 }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val3 }}</div>
                            </el-col>
                            </el-row>
                        </div>
                    </el-card>
                </div>
              </div>

              <div v-if="projectType != 0">
                <h3>{{ projectType == 1 ? '2' : '3' }}.C++信息概况</h3>
                <div class="cards">
                    <el-card class="card" shadow="hover">
                        <div slot="header" style="font-weight: bolder;">
                            <span>{{ CPPmainInfo.fileType }}</span>
                        </div>
                        <div class="card-item">
                            <el-row style=" color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ CPPmainInfo.fileProp_k }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ CPPmainInfo.fileProp }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style=" color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ CPPmainInfo.totalNum_k }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ CPPmainInfo.totalNum }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        </el-card>
                        <el-card class="card" shadow="hover" v-for="(card, index) in cardInfocpp" :key="index">
                        <div slot="header" style="font-weight: bolder;">
                            <span>{{ card.title }}</span>
                        </div>
                        <div class="card-item">
                            <el-row style=" color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ card.key1 }}</div>
                            </el-col>
                            <!--    <el-col :span="12">
                                <div style="text-align: right;">{{ card.val1 }}</div>
                            </el-col> -->
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style=" color: rgb(244, 70, 163);">
                            <el-col :span="12">
                                <div style="text-align: left;">{{ card.msg }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val1 }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        <div class="card-item">
                            <el-row style="">
                            <el-col :span="12">
                                <div>{{ card.key2 }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val2 }}</div>
                            </el-col>
                            </el-row>
                        </div>
                        <div class="card-item" style="">
                            <el-row>
                            <el-col :span="12">
                                <div>{{ card.key3 }}</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.val3 }}</div>
                            </el-col>
                            </el-row>
                        </div>
                    </el-card>
                </div>
              </div>
            </el-main>
  
          </el-container>
  
        </div>
        <el-backtop target=".pdf_main" :right="250" :bottom="60"></el-backtop>
      </div>
  </template>
  
  <script>
  import Cache from "@/utils/cache"
  
  export default {
    data() {
      return {
        projectType: this.$store.state.current_project.projectType,
        projectName: this.$store.state.current_project.name,
        printObj: {
          id: "printMe", // 这里是要打印元素的ID
          popTitle: "&nbsp", // 打印的标题
        },
        mainInfo: {
          fileType: ".c",
          fileProp_k: "C文件占比",
          fileProp: "",
          totalNum_k: "函数总数",
          totalNum: "",
  
        },
        CPPmainInfo: {
          fileType: ".cpp",
          fileProp_k: "CPP文件占比",
          fileProp: "",
          totalNum_k: "类总数",
          totalNum: "",
  
        },
        cardInfo: [
          // {
          //     title: "C信息",
          //     key1: null,
          //     val1: null,
          //     key2: null,
          //     val2: null,
          //     key3: null,
          //     val3: null
          // }
        ],
        cardInfocpp: [],
  
        project: {
          name: "CUnit"
        },
        projectInfo: null,
        myChart: null,
        option: {
          title: {
            text: "test" + '文件种类',
            left: 'center',
            top: '5%'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: '5%'
          },
          series: [
            {
              // name: 'Access From',
              type: 'pie',
              radius: '50%',
              data: [
                {value: 1048, name: 'header'},
                {value: 735, name: 'c_source'},
                {value: 580, name: 'c++_source'},
                // {value: 484, name: 'other_file'}
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        },
  
        tableData1: [],
        tableData2: [],
        tableData3: []
      }
    },
    mounted() {
      this.getData()
    },
    methods: {
      chartInit() {
        this.myChart = this.$echarts.init(this.$refs.myChart)
        this.myChart.setOption(this.option)
        let myChart = this.myChart
        window.addEventListener("resize", () => {
          if (myChart) {
            myChart.resize()
          }
        })
      },
      getData() {  
        let _this = this

        let data = Cache.getCache("project_info")

        let code_info = Cache.getCache("project_code_info")

        console.log('data', code_info)
        if (this.projectType != 1) {
          this.mainInfo.fileProp = code_info.c_info.cFileProp
          this.mainInfo.totalNum = code_info.c_info.funcTotal
          _this.cardInfo = []
          _this.cardInfo.push({
            title: "最大行数函数",
            key1: code_info.c_info.functionLine.maxLineFunc,
            msg: "行数",
            val1: code_info.c_info.functionLine.maxLine + "行",
            key2: "平均行数",
            val2: code_info.c_info.functionLine.avgLine.toFixed(2) + "行",
            key3: "最小行数",
            val3: code_info.c_info.functionLine.minLine + "行"
          })
          _this.cardInfo.push({
            title: "最大行数文件",
            key1: code_info.c_info.fileLine.maxLineFile,
            msg: "行数",
            val1: code_info.c_info.fileLine.maxLine + "行",
            key2: "平均行数",
            val2: code_info.c_info.fileLine.avgLine.toFixed(2) + "行",
            key3: "最小行数",
            val3: code_info.c_info.fileLine.minLine + "行"
          })
          _this.cardInfo.push({
            title: "包含函数最多的文件",
            key1: code_info.c_info.defineFuncFile.maxFuncFile,
            msg: "包含函数",
            val1: code_info.c_info.defineFuncFile.maxFunc + "个",
            key2: "平均包含函数",
            val2: code_info.c_info.defineFuncFile.avgFunc.toFixed(2) + "个",
            key3: "最小包含函数",
            val3: code_info.c_info.defineFuncFile.minFunc + "个"
          })
        } 
        if (this.projectType != 0) {
          this.CPPmainInfo.fileProp = code_info.c_plus_info.cppFileProp
          this.CPPmainInfo.totalNum = code_info.c_plus_info.classTotal
          _this.cardInfocpp = []
          _this.cardInfocpp.push({
            title: "包含最多成员的类",
            key1: code_info.c_plus_info.classMember.maxMemberClass,
            msg: "包含成员数",
            val1: code_info.c_plus_info.classMember.maxMember + "个",
            key2: "平均包含成员数",
            val2: code_info.c_plus_info.classMember.avgMember.toFixed(2) + "个",
            key3: "最小包含成员数",
            val3: code_info.c_plus_info.classMember.minMember + "个"
          })
          _this.cardInfocpp.push({
            title: "最大行数文件",
            key1: code_info.c_plus_info.fileLine.maxLineFile,
            msg: "行数",
            val1: code_info.c_plus_info.fileLine.maxLine + "行",
            key2: "平均行数",
            val2: code_info.c_plus_info.fileLine.avgLine.toFixed(2) + "行",
            key3: "最小行数",
            val3: code_info.c_plus_info.fileLine.minLine + "行"
          })
          _this.cardInfocpp.push({
            title: "包含类最多的文件",
            key1: code_info.c_plus_info.defineClassFile.maxClassFile,
            msg: "包含类数",
            val1: code_info.c_plus_info.defineClassFile.maxClass + "个",
            key2: "平均包含类数",
            val2: code_info.c_plus_info.defineClassFile.avgClass.toFixed(2) + "个",
            key3: "最小包含类数",
            val3: code_info.c_plus_info.defineClassFile.minClass + "个"
          })
        }
        
        this.option = {
          title: {
            text: "test" + '文件种类',
            left: 'center',
            top: '5%'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            top: '5%'
          },
          series: [
            {
              // name: 'Access From',
              type: 'pie',
              radius: '50%',
              data: data.fileProp,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        this.chartInit()
  
        this.tableData1 = [{
          dirNumber: data.dirNumber + "个",
          fileNumber: data.fileNumber + "个",
          functionNumber: data.functionNumber + "个"
        }]
        this.tableData2 = [{
          codeLine: data.codeLine + "行",
          codeLineExp: data.codeLineExp + "行",
          commentLine: data.commentLine + "行",
          commentLineExp: data.commentLineExp + "行"
        }]
        this.tableData3 = [{
          codeLineExpProp: data.codeLineExpProp,
          emptyLineProp: data.emptyLineProp,
          commentLineExpProp: data.commentLineExpProp
        }]
      },
      print() {
        this.$print(this.$refs.print)
        //因为每次打印都会多一个img（将echarts的canvas转为img），我的print.js里头已经配置给这个img里头加的classname为isNeedRemove，所以每次打印完需去除，我只有一张echarts、去除的数量根据业务需求定。
        this.$nextTick(() => {
          let arr = document.getElementsByClassName('isNeedRemove')
          while (arr.length) arr[0].remove();
        })
      }
    }
  }
  </script>
  
  <style scoped>
  
  >>> .chart {
    height: 80%
  }
  
  >>>.el-table__header th{
    background-color: #f0f0f0;
  }
  >>> .el-table tr {
    font-weight: normal;
    font-size: 18px;
    color: black;
    border: 1px solid black;
    border-collapse: collapse;
  }
  @page {
    size: auto;
    margin: 3mm;
  }
  
  @media print {
    /*>>> .el-table {*/
    /*  font-size: 16px;*/
    /*  color: #000000;*/
    /*}*/
    /* 表格内容边框 */
  
    .el-table__header-wrapper, .el-table__fixed-header-wrapper th
    {
      background: blue;
      color: #939598 !important;
    }
    >>> .el-table tr {
      font-weight: normal;
      font-size: 18px;
      color: black;
      border: 1px solid black;
      border-collapse: collapse;
    }
    /* 表格内容边框 */
  
  
    /*>>> .el-table--border {*/
    /*  background-color: #000000;*/
    /*}*/
  
    /*>>> .el-table--border th, >>> .el-table--border td {*/
    /*  border: solid #000000;*/
    /*}*/
  
    /*>>> .el-table--group, >>> .el-table--border {*/
    /*  border-color: #000000;*/
    /*}*/
  
    /*>>> .el-table th.is-leaf, >>> .el-table td {*/
    /*  border-bottom: 1px solid #000000;*/
    /*}*/
  
    /*!*!*减小单元格间距*!*!*/
    /*!*>>> .el-table th, >>> .el-table td {*!*/
    /*!*  padding: 0 0;*!*/
    /*!*}*!*/
  
    /*!*显示底部边框 估计打印时伪元素把border覆盖了 height设为0隐藏伪元素*!*/
    /*>>> .el-table::before {*/
    /*  height: 0;*/
    /*}*/
  
    /*!*显示右边框*!*/
    /*>>> .el-table--group::after, >>> .el-table--border::after {*/
    /*  width: 0;*/
    /*}*/
  
    html {
      background-color: #ff23ff;
      height: auto;
      margin: 0px;
    }
  
    >>> .chart {
      height: 80%;
    }
  
  }
  
  .cards {
    height: 40%;
    width: 100%;
    display: flex;
    flex-flow: wrap;
  }
  
  .card {
    /* height: 40%; */
    width: 44%;
    margin-left: 3%;
    margin-right: 2%;
    margin-bottom: 1%;
  }
  
  .card-item {
    margin-bottom: 2%;
  }
  </style>
  