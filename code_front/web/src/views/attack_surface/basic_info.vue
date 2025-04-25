<template>
    <div class="container">
      <el-row>
        <el-tabs type="card" >
              <div style="width: 100%;">
                  <el-tabs tab-position="left">
                      <el-tab-pane label="总览信息">
                          <div>
                              <el-table
                              class="total_table"
                              :data="attack_surface_info_table"
                              :header-cell-style="()=>{return 'background: lightblue;color:black;'}"
                              stripe>
                                  <el-table-column
                                  prop="entry_exit_points_num"
                                  label="入口/出口节点个数"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="untrusted_data_item_nums"
                                  label="不可信数据元素个数"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="data_channel_num"
                                  label="数据通道个数"
                                  align="center">
                                  </el-table-column>
                              </el-table>
                              <!-- <el-table
                              class="total_table"
                              :data="attack_surface_prop_table"
                              :header-cell-style="()=>{return 'background: lightgreen;color:black;'}"
                              stripe>
                                  <el-table-column
                                  prop="type"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="entry_exit_points_prop"
                                  label="攻击面节点占比"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="attack_surface_files_prop"
                                  label="攻击面文件占比"
                                  align="center">
                                  </el-table-column>
                              </el-table> -->
                              <el-table
                              class="total_table"
                              :data="attacks_catogery_info_table"
                              :header-cell-style="()=>{return 'background: orange;color:black;'}"
                              stripe>
                                  <el-table-column
                                  prop="type"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="attack_catergory_id"
                                  label="潜在攻击类型"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="attack_num"
                                  label="潜在攻击个数"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="attack_type_prop"
                                  label="潜在攻击占比"
                                  align="center">
                                  </el-table-column>
                              </el-table>
                              <div ref="myChart1" class="my_chart"></div>
                          </div>
                      </el-tab-pane>
  
                      <el-tab-pane class="el-tab-pane" label="详细信息">
                            <div class="detect_class">
                              <h4>入口节点/出口节点</h4>
                              <el-table
                              class="total_table"
                              :data="entry_exit_points_table"
                              :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                              height="30vh"
                              stripe>
                                  <el-table-column
                                  prop="location"
                                  label="节点位置"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="type"
                                  label="类型"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="library"
                                  label="依赖库信息"
                                  align="center">
                                  </el-table-column>
                              </el-table>
                          </div>
                          <div class="detect_class">
                              <h4>不可信数据元素</h4>
                              <el-table
                              class="total_table"
                              :data="untrusted_data_items_table"
                              :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                              height="30vh"
                              stripe>
                                  <el-table-column
                                  prop="name"
                                  label="元素名称"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="location"
                                  label="位置"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="type"
                                  label="类型"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="library"
                                  label="依赖库信息"
                                  align="center">
                                  </el-table-column>
                              </el-table>
                          </div>
                          <div class="detect_class">
                              <h4>CAPEC-based 潜在攻击集合</h4>
                              <el-table
                              class="total_table"
                              :data="attack_set_detail_table"
                              :header-cell-style="()=>{return 'background: rgb(182, 254, 230);color:black;'}"
                              height="30vh"
                              stripe>
                                  <el-table-column
                                  prop="source"
                                  label="攻击发生位置"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="standard"
                                  label="CAPEC-ID"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="severity"
                                  label="严重程度"
                                  align="center">
                                  </el-table-column>
                                  <el-table-column
                                  prop="prop"
                                  label="发生概率"
                                  align="center">
                                  </el-table-column>
                              </el-table>
                          </div>
                      </el-tab-pane>
                  </el-tabs>
              </div>
        </el-tabs>
      </el-row>
    </div>
  </template>
  
  <script>
  import utils from '@/utils/utils'
  import config from '@/config'
  export default {
      data(){
          return{
            myChart: null,
            attack_surface_info_table : [],
            attack_surface_prop_table : [],
            attacks_catogery_info_table : [],
            entry_exit_points_table : [],
            untrusted_data_items_table : [],
            attack_set_detail_table : [],

            chartData: [
                      { value: 1, name: "CAPEC-123", key: "CAPEC-123" },
                      { value: 2, name: "CAPEC-234", key: "CAPEC-234" },
                      { value: 3, name: "CAPEC-567", key: "CAPEC-567" }
                  ],
          }
      },
      mounted(){
            let _this = this;
            // get table infos from backend
            utils.axiosMethod({
                method: "GET",
                url: window.ipConfig.baseUrl + "/ATTACK_SURFACE_IFNO/" + this.$store.state.current_project.name,
                callback: (response)=>{
                    let data = response.data
                    console.log(data)
                    _this.chartData = data.attackSetChartData;
                    _this.attack_surface_info_table = [data.attack_surface_info_table];
                    // _this.attack_surface_prop_table = data.attack_surface_prop_table;
                    _this.attacks_catogery_info_table = data.attacks_catogery_info_table;
                    _this.entry_exit_points_table = data.entry_exit_points_table;
                    _this.untrusted_data_items_table = data.untrusted_data_items_table;
                    _this.attack_set_detail_table = data.attack_set_detail_table;
                    _this.chartInit();
                }
            })
            
      },
      methods: {
          
          chartInit(){
              this.myChart = this.$echarts.init(this.$refs.myChart1)
              let option = {
                  title: {
                      text: '潜在攻击集合',
                      left: 'center'
                  },
                  tooltip: {
                      trigger: 'item'
                  },
                  // legend: {
                  //     orient: 'vertical',
                  //     left: 'left'
                  // },
                  series: [
                      {
                          // name: 'Access From',
                          type: 'pie',
                          radius: '50%',
                          data: this.chartData,
                          emphasis: {
                              itemStyle: {
                                  shadowBlur: 10,
                                  shadowOffsetX: 0,
                                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                              }
                          }
                      }
                  ]
              };
              this.myChart.setOption(option)
              // 根据窗口大小进行动态缩放
              window.addEventListener("resize", () => {
                  if(this.myChart){
                    this.myChart.resize()
                  }
              })
          },
      }
  }
  </script>
  
  <style scoped>
  .container{
      height: 89vh;
      width: 100vw;
  }
  .file_select{
      display: flex;
      height: 6vh;
      justify-content: center;
      align-items: center;
  }
  .el-input{
      width: 15vw;
      margin-left: 2vw;
      margin-right: 2vw;
  }
  .el-button{
      height: 4vh;
  }
  .total_table{
      width: 90%;
      margin: 0 auto;
  }
  .weight_input{
      display: flex;
      height: 6vh;
      justify-content: center;
      align-items: center;
      margin-top: 5px;
      margin-bottom: 5px;
  }
  .el-input1{
      width: 8vw;
      margin-left: 3vw;
      margin-right: 3vw;
  }
  .my_chart{
      height: 50vh;
      width: 50vw;
      margin: 0 auto;
  }
  .el-tab-pane{
      height: 83vh;
      overflow-y: scroll;
  }
  .detect_class{
      width: 80vw;
      margin: 3vh auto;
  }
  </style>