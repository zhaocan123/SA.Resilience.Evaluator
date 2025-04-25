<template>
    <div class="pdf_main" style="width: 21cm;">
        <div>  
            <el-container style=";border: 1px ; page-break-after: always;">
    
            <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
              <!--模块级详细信息-->
              <el-row :gutter="15" style="height: 80% " class="detailCards">
                <!-- <h1 style="text-align: center">{{ this.moduleLevel.projectName+"项目模块级信息"}}</h1> -->
                <h1 style="text-align: center">{{ projecName }} 项目设计质量评估结果</h1>
    
                <h3>目录</h3>
                <el-col :span="24" style="height: 100% ">
                  <div style="height: 100% ">
                    <li class="mulu_list" v-for="(item,idx) in pageinfo.content" :key="idx">
                      <p >{{idx}}</p>
                      <p style="flex-grow: 1;border-bottom: 1px dashed;margin-bottom: 28px;"></p>
                      <p>{{item}}</p>
                    </li>
                  </div>
                </el-col>
              </el-row>
    
    
              <!--文件列表& halstead复杂度-->
            </el-main>
          </el-container>
          </div>
    
            <div>
                <el-container style="height: 29.7cm;;page-break-after: always;">
                    <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
                        <el-row :gutter="16" style="height: 100% ">
                            <h3>1.设计质量评估概况</h3>
                            <div class="main">
                                <div class="col2">
                                        <div ref="Chart3" class="col2-1"></div>
                                </div>
                                
                            </div>
                            <el-table
                                :key="check3"
                                :data="table3"
                                height="35%"
                                style="width: 100%;margin: auto"
                                :cell-style="{padding: '10px'
                                ,'text-align':'center'}"
                                :header-cell-style="{'text-align':'center'}"
                            >
                            <el-table-column :label="'设计质量评估概况'">
                                <el-table-column
                                prop="name"
                                label="指标名称">
                                </el-table-column>
                                <el-table-column
                                prop="text"
                                label="描述">
                                </el-table-column>
                                <el-table-column
                                prop="value"
                                label="度量值">
                                </el-table-column>
                            </el-table-column>
                            </el-table>
                        <!-- <div style="text-align: center; margin-top: 10px;bottom:16px">第{{ pageinfo.content["1.设计质量评估概况"] }}页，共{{ pageinfo.total}}页</div> -->
    
                        </el-row>
                        
                                            
                            
                    </el-main>
                    <el-footer style="text-align: center;">第{{ pageinfo.content["1.设计质量评估概况"] }}页，共{{ pageinfo.total}}页</el-footer>
    
                </el-container>  
    
            </div>
    
            <div>
                <el-container style="height: 29.7cm;;page-break-after: always;">
                    <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
                        <el-row :gutter="16" style="height: 40% ">
                            <h3>2.函数信息概况</h3>
                            <h4>
                                2.1接口函数占比
                            </h4>
                            <div class="main2" >
                                <div class="col1">
                                        <div ref="Chart1" class="col1-1"></div>
                                </div>
                            </div>
                            <el-table
                                :key="check1"
                                :data="table1"
                                height="45%"
                                style="width: 100%;margin: auto"
                                :cell-style="{padding: '10px'
                                ,'text-align':'center'}"
                                :header-cell-style="{'text-align':'center'}"
                            >
                            <el-table-column :label="'接口函数占比'">
                                <el-table-column
                                prop="name"
                                label="指标名称">
                                </el-table-column>
    
                                <el-table-column
                                prop="value"
                                label="度量值">
                                </el-table-column>
                            </el-table-column>
                            </el-table>
                            <h4>
                                2.2注释函数占比
                            </h4>
                            <div class="main2" >
                                <div class="col1">
                                        <div ref="Chart4" class="col1-2"></div>
                                </div>
                            </div>
                            <el-table
                                :key="check4"
                                :data="table4"
                                height="35%"
                                style="width: 100%;margin: auto"
                                :cell-style="{padding: '10px'
                                ,'text-align':'center'}"
                                :header-cell-style="{'text-align':'center'}">
                                <el-table-column :label="'注释函数占比'">
    
                                <el-table-column
                                prop="value1"
                                label="注释函数个数">
                                </el-table-column>
    
                                <el-table-column
                                prop="value2"
                                label="注释函数占比">
                                </el-table-column>
                                </el-table-column>
    
                            </el-table>
    
                        </el-row>
                                            
                            
                    </el-main>
                    <el-footer style="text-align: center">第{{ pageinfo.content["2.函数信息概况"] }}页，共{{ pageinfo.total}}页</el-footer>
    
                </el-container>  
    
            </div>
    
            <div>
                <el-container style="height: 29.7cm;;page-break-after: always;">
                    <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
                        <el-row :gutter="16" style="height: 90% ">
                            <h4>
                                2.3函数入度、函数出度与可替换性
                            </h4>
                            <div class="main1" style="margin-bottom:0px">
                                <div class="col3">
                                        <div ref="Chart2" class="col3-1"></div>
                                </div>
                            </div>
                            <!-- <h4>
                                2.4函数的可替换性
                            </h4> -->
                            <div class="main1" >
                                <div class="col3">
                                        <div ref="Chart5" class="col3-2"></div>
                                </div>
                            </div>
                            <!-- <el-table
                                :key="check5"
                                :data="table5"
                                height="50%"
                                style="width: 100%;margin: auto"
                                :cell-style="{padding: '10px'
                                ,'text-align':'center'}"
                                :header-cell-style="{'text-align':'center'}"                          >
                                <el-table-column
                                prop="index"
                                label="序号">
                                </el-table-column>
                                <el-table-column
                                prop="name"
                                label="函数名">
                                </el-table-column>
                                <el-table-column
                                prop="indegree"
                                label="入度">
                                </el-table-column>
    
                                <el-table-column
                                prop="outdegree"
                                label="出度">
                                </el-table-column>
                                <el-table-column
                                prop="value"
                                label="可替换性">
                                </el-table-column>
    
                            </el-table> -->
                            
    
                        </el-row>                        
                            
                    </el-main>
                    <el-footer  style="text-align: center">第{{ pageinfo.content["2.3函数入度、函数出度与可替换性"] }}页，共{{ pageinfo.total}}页</el-footer>
    
                </el-container>  
    
            </div>
    
            <div v-for="(tableData, index) in CtableDataPages" :key="index"> 
                <el-table
                    :key="check5"
                    :data="tableData"
                    @height-change="handleTableHeightChange"
                    style="width: 100%;margin-top: auto"
                    :cell-style="{padding: '10px'
                    ,'text-align':'center'}"
                    :header-cell-style="{'text-align':'center'}" >
                    <el-table-column :label="'函数入度、函数出度与可替换性'">
                    <el-table-column
                    prop="index"
                    label="序号">
                    </el-table-column>
                    <el-table-column 
                    prop="name"
                    label="函数名">
                    </el-table-column>
                    <el-table-column
                    prop="indegree"
                    label="入度">
                    </el-table-column>

                    <el-table-column
                    prop="outdegree"
                    label="出度">
                    </el-table-column>
                    <el-table-column
                    prop="value"
                    label="可替换性">
                    </el-table-column>
                    </el-table-column>
                </el-table>
            </div>
            
            
            <div v-if="projectType != 0">
                <div>
                    <el-container style="height: 29.7cm;;page-break-after: always;">
                        <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
                            <el-row :gutter="16" style="height: 40% ">
                                <!-- <h1 style="text-align: center">{{ this.project.name+"项目设计评估结果"}}</h1> -->
                                <h3>3.类信息概况</h3>
                                <h4>3.1接口类占比</h4>
                                <div class="main2">
                                    <div class="col1">
                                        <div ref="Chart11" class="col1-1"></div>
                                    </div>
                                </div>
                                <el-table
                                    :key="check11"
                                    :data="table11"
                                    height="40%"
                                    style="width: 100%;margin: auto"
                                    :cell-style="{padding: '10px'
                                    ,'text-align':'center'}"
                                    :header-cell-style="{'text-align':'center'}"
                                >
                                <el-table-column :label="'接口类占比'">
                                    <el-table-column
                                    prop="value1"
                                    label="接口类数量">
                                    </el-table-column>
        
                                    <el-table-column
                                    prop="value2"
                                    label="非接口类数量">
                                    </el-table-column>
                                </el-table-column>
        
                                </el-table>
                                <h4>
                                    3.2注释类占比
                                </h4>
                                <div class="main2" >
                                    <div class="col1">
                                            <div ref="Chart14" class="col1-2"></div>
                                    </div>
                                </div>
                                <el-table
                                    :key="check14"
                                    :data="table14"
                                    height="40%"
                                    style="width: 100%;margin: auto"
                                    :cell-style="{padding: '10px'
                                    ,'text-align':'center'}"
                                    :header-cell-style="{'text-align':'center'}" >
                                <el-table-column :label="'注释类占比'">
                                    <el-table-column
                                    prop="value1"
                                    label="注释类个数">
                                    </el-table-column>
        
                                    <el-table-column
                                    prop="value2"
                                    label="注释类占比">
                                    </el-table-column>
                                </el-table-column>
        
                                </el-table>
        
                            </el-row>
                                                
                                
                        </el-main>
                        <el-footer style="text-align: center">第{{ pageinfo.content["3.类信息概况"] }}页，共{{ pageinfo.total}}页</el-footer>
        
                    </el-container>  
        
                </div>
        
                <div>
                    <el-container style="height: 29.7cm;;page-break-after: always;">
                        <el-main style="height:100%; padding-top: 10px; padding-bottom: 10px">
                            <el-row :gutter="16" style="height: 90% ">
                                <h4>
                                    3.3类入度、类出度与可替换性
                                </h4>
                                <div class="main1" style="margin-bottom:0px">
                                    <div class="col3">
                                            <div ref="Chart12" class="col3-1"></div>
                                    </div>
                                </div>
        
                                <div class="main1" >
                                    <div class="col3">
                                            <div ref="Chart15" class="col3-2"></div>
                                    </div>
                                </div>
                                <!-- <el-table
                                    :key="check15"
                                    :data="table15"
                                    :max-height="auto"
                                    style="width: 100%;margin: auto"
                                    :cell-style="{padding: '10px'
                                    ,'text-align':'center'}"
                                    :header-cell-style="{'text-align':'center'}"                          >
                                    <el-table-column
                                    prop="index"
                                    label="序号">
                                    </el-table-column>
                                    <el-table-column
                                    prop="name"
                                    label="类名">
                                    </el-table-column>
                                    <el-table-column
                                    prop="indegree"
                                    label="入度">
                                    </el-table-column>
        
                                    <el-table-column
                                    prop="outdegree"
                                    label="出度">
                                    </el-table-column>
                                    <el-table-column
                                    prop="value"
                                    label="可替换性">
                                    </el-table-column>
        
                                </el-table> -->
                                
        
                            </el-row>
                                                
                                
                        </el-main>
                        <el-footer style="text-align: center;">第{{ pageinfo.content["3.3类入度、类出度与可替换性"] }}页，共{{ pageinfo.total}}页</el-footer>
        
                    </el-container>  
        
                </div>
        
                
                <div v-for="(tableData, index) in tableDataPages" :key="index">
                    <el-table
                        :key="check15"
                        :data="tableData"
                        @height-change="handleTableHeightChange"
                        style="width: 100%;margin-top: auto"
                        :cell-style="{padding: '10px'
                        ,'text-align':'center'}"
                        :header-cell-style="{'text-align':'center'}"  >
                        <el-table-column :label="'类入度、类出度与可替换性'">
                        <el-table-column
                        prop="index"
                        label="序号">
                        </el-table-column>
                        <el-table-column
                        prop="name"
                        label="类名">
                        </el-table-column>
                        <el-table-column
                        prop="indegree"
                        label="入度">
                        </el-table-column>

                        <el-table-column
                        prop="outdegree"
                        label="出度">
                        </el-table-column>
                        <el-table-column
                        prop="value"
                        label="可替换性">
                        </el-table-column>
                    </el-table-column>

                    </el-table>
                </div>
            </div>
            <el-backtop target=".pdf_main" :right="250" :bottom="60"></el-backtop>
        </div>
    </template>
    
    <script>
    import Cache from  "@/utils/cache"
    export default {
      data() {
        return {
            projecName: this.$store.state.current_project.name,
            projectType: this.$store.state.current_project.projectType,
            printObj: {
                id: "printMe", // 这里是要打印元素的ID
                popTitle: "&nbsp", // 打印的标题
            },
            pageinfo:{
                total:0,
                content:{}
            },
            activeName: "funcInfo",
            metrix: null,
            Chart1: null,
            Chart2: null,
            Chart3: null,
            Chart4: null,
            Chart5: null,
            Chart11: null,
            Chart12: null,
            // Chart13: null,
            Chart14: null,
            Chart15: null,
            
            table3:null,
            table1:null,
            table4:null,
            table2:null,
            table5:null,
            table11:null,
            table12:null,
            table14:null,
            table15:null,
            check15:true,
            check14:true,
            check12:true,
            check11: true,
            check5:true,
            check2:true,
            check4:true,
            check1:true,
            check3:true,
    
            tableDataPages: [], // 分页后的表格数据
            CtableDataPages: [],
            maxTableHeight: 'auto', // 使用 'auto' 表示高度自动延伸
            tableHeight: 0, // 当前表格高度
            maxTableHeightPerPage: 20, // 每页最大高度，根据实际需求调整
    
        }
      },
      mounted() {
        let _this = this;
        this.metrix = Cache.getCache("design_eval")
        _this.initCharts();
    
    //     window.onresize = function temp() {
    //     _this.maxTableHeightPerPage = `${document.documentElement.clientHeight}` - 242;
    //   };
      },
      methods: {
        initCharts(){
            this.initChart3();
            this.initChart1();
            this.initChart4();
            this.initChart2();
            this.initChart5();
    
            this.initChart11();
            this.initChart14();
            this.initChart12();
            this.initChart15();
            // console.log(this.pageinfo);
        },
    
        print(){
          this.$print(this.$refs.print)
          //因为每次打印都会多一个img（将echarts的canvas转为img），我的print.js里头已经配置给这个img里头加的classname为isNeedRemove，所以每次打印完需去除，我只有一张echarts、去除的数量根据业务需求定。
          this.$nextTick(()=>{
            let arr=document.getElementsByClassName('isNeedRemove')
            while(arr.length) arr[0].remove();
          })
        },
    
        initChart3() {
                const map = {
                    "comprehensibility": "易理解性",
                    "refundability": "可替换性",
                    "scalability": "可扩展性",
                    "modifiability": "可修改性",
                    "testability": "易测试性"
                }
                let indicator = []
                let values = []
                let names = []
                // this.metrix={
                //     "comprehensibility": 0.3,
                //     "refundability": 0.4,
                //     "scalability": 0.5,
                //     "modifiability": 0.4,
                //     "testability": 0.3
                // }           
    
                for (let key in map) {
                    indicator.push({
                        name: map[key],
                        max: 1
                    })
                    values.push(this.metrix[key].value.toFixed(2))
                    names.push(map[key])
                }
                let option3 = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    title: {
                        text: '设计质量评估概况',
                        left: "center",
                        top: "2%"
                    },
                    radar: {
                        // shape: 'circle',
                        indicator: indicator,
                        axisName: {
                            color: 'black',
                            fontSize: '16px'
                        },
                    },
                    series: [
                        {
                            tooltip: {
                                trigger: 'item'
                            },
                            name: '指标',
                            type: 'radar',
                            data: [
                                {
                                    value: values,
                                    name: names
                                }
                            ],
                            color: "red"
                        }
                    ]
                }
                this.Chart3 = this.$echarts.init(this.$refs.Chart3)
                this.Chart3.setOption(option3)
                // 根据窗口大小进行动态缩放
                window.addEventListener("resize", () => {
                    if (this.Chart3) {
                        this.Chart3.resize()
                    }
                });
                this.table3 = []
                let textdict={
                    "comprehensibility": "comprehensibility",
                    "refundability": "refundability",
                    "scalability": "scalability",
                    "modifiability": "modifiability",
                    "testability": "testability"
                }   
                
                for (const [key, value] of Object.entries(this.metrix)) {
                    let obj = {};
                    if(key in textdict) {
                    obj.name = map[key];
                    obj.text = textdict[key];
                    obj.value = value.value.toFixed(3);
                    this.table3.push(obj);
                    };
            }   
                this.check3 = !this.check3;
                let text = '1.设计质量评估概况';
                this.pageinfo.total++;
                let pageindex = this.pageinfo.total;
                this.pageinfo.content[text] = pageindex;
    
            },
        initChart1() {
            let data = []
            // let metrix1 = {
            //     "scalability":{
            //         "apiNum":10,
            //         "funcNum":40,
            //     }
            // }
        
            let num1 = this.metrix.scalability.apiNum
            let num = this.metrix.scalability.funcNum
    
            data.push({
                name: "接口函数数量",
                value: num1,
                rate: (num1 / num * 100).toFixed(2).toString(),
                itemStyle: {
                    color: "rgb(16, 135, 240)"
                }
            })
            data.push({
                name: "非接口函数数量",
                value: num - num1,
                rate: ((num - num1) / num * 100).toFixed(2).toString(),
                itemStyle: {
                    color: "rgb(251, 59, 136)"
                }
            })
            let option1 = {
                title: {
                    text: "接口函数占比",
                    left: "center",
                    top: "1%"
                },
                tooltip: {
                    trigger: 'item',
                    formatter: (param) => {
                        let item = param.data;
                        return `${item.name}:<br />${item.value}个<br />${item.rate}%`;
                    }
                },
                legend: {
                    top: 'bottom',
                    left: 'left'
                },
                series: [
                    {
                        name: '数据',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: 40,
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: data,
                        label: {
                            show: true,
                            position: 'inside'
                        },
                    }
                ]
            }
            this.Chart1 = this.$echarts.init(this.$refs.Chart1)
            this.Chart1.setOption(option1)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart1) {
                    this.Chart1.resize()
                }
            })
    
            this.table1 = []
            let obj = {
                "name":"接口函数数量",
                "value":num1,
            }
            this.table1.push(obj)
            let obj1 = {
                "name":"非接口函数数量",
                "value":num-num1,
            }
            this.table1.push(obj1)
            this.check1 = !this.check1;
    
            let text = '2.函数信息概况';
            this.pageinfo.total++;
            let pageindex = this.pageinfo.total;
            this.pageinfo.content[text] = pageindex;
    
            let text2 = '2.1接口函数占比';
            // this.pageinfo.total++;
            this.pageinfo.content[text2] = pageindex;
        },
        initChart4() {
            // let metrix4 = {
            //     "comprehensibility":{
            //         "funcNum":10,
            //         "commentFunc":5,
            //     }
            // }
            let data1 = {
                name: "函数数量",
                num: this.metrix.comprehensibility.funcNum,
                value: 100
            }
            let data2 = {
                name: "包含注释的函数数量",
                num: this.metrix.comprehensibility.commentFunc,
                value: (this.metrix.comprehensibility.commentFunc / this.metrix.comprehensibility.funcNum * 100).toFixed(2)
            }
            // let data3 = {
            //     name: "过多注释函数数量",
            //     num: 0,
            //     value: (0 / this.metrix.comprehensibility.funcNum * 100).toFixed(2)
            // }
            const gaugeData = [
                {
                    value: data2.value,
                    num: data2.num,
                    name: data2.name,
                    title: {
                        offsetCenter: ['0%', '-20%']
                    },
                    detail: {
                        valueAnimation: true,
                        offsetCenter: ['0%', '20%']
                    }
                }
            ]
            let option4 = {
                title: {
                    text: "包含注释函数占比",
                    subtext: "函数数量——" + data1.num + "个",
                    left: "center"
                },
                tooltip: {
                    trigger: "item",
                    formatter: (params) => {
                        let { name, num } = params.data;
                        return `${name}<br /> ${num}个`;
                    }
                },
                series: [
                    {
                        name: "数量",
                        type: 'gauge',
                        color: "green",
                        center: ["50%", "58%"],
                        startAngle: 90,
                        endAngle: -270,
                        pointer: {
                            show: false
                        },
                        progress: {
                            show: true,
                            overlap: false,
                            roundCap: true,
                            clip: false,
                            itemStyle: {
                                borderWidth: 1,
                                borderColor: '#464646'
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                width: 30
                            }
                        },
                        splitLine: {
                            show: false,
                            distance: 0,
                            length: 10
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            show: false,
                            distance: 50
                        },
                        data: gaugeData,
                        title: {
                            fontSize: 10
                        },
                        detail: {
                            width: 40,
                            height: 12,
                            fontSize: 10,
                            color: 'inherit',
                            borderColor: 'inherit',
                            borderRadius: 20,
                            borderWidth: 1,
                            formatter: '{value}%'
                        }
                    }
                ]
            }
            this.Chart4 = this.$echarts.init(this.$refs.Chart4)
            this.Chart4.setOption(option4)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart4) {
                    this.Chart4.resize()
                }
            })
    
            this.table4 = []
            let obj = {
                "name1":"注释函数个数",
                "value1":data2.num,
                "name2":"占比",
                "value2":data2.value,
            }
            this.table4.push(obj)
    
            this.check4 = !this.check4;
    
            let text = '2.2注释函数占比';
            // this.pageinfo.total++;
            let pageindex = this.pageinfo.total;
            this.pageinfo.content[text] = pageindex;
        },
        initChart2() {
            let _this = this
            let option2 = {
                title: {
                    text: '函数入度 & 函数出度',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        animation: false
                    },
                    position: function (point) {
                        return [point[0], point[1]]
                    },
                    formatter: (params) => {
                        // console.log('params', params)
                        let funcName = _this.metrix.funcNameList[params[0].dataIndex]
                        return `${funcName} 入度: ${params[0].data} 出度: ${params[1].data}`
                    }
                },
                legend: {
                    data: ['入度', '出度'],
                    right: 2,
                    bottom: 2
                },
                axisPointer: {
                    link: [
                        {
                            xAxisIndex: 'all'
                        }
                    ]
                },
                grid: [
                    {
                        left: 35,
                        right: 30,
                        height: '35%'
                    },
                    {
                        left: 35,
                        right: 30,
                        top: '55%',
                        height: '35%'
                    }
                ],
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        axisLine: { onZero: true },
                        data: this.metrix.xAxis
                    },
                    {
                        gridIndex: 1,
                        type: 'category',
                        boundaryGap: false,
                        axisLine: { onZero: true },
                        data: this.metrix.xAxis,
                        position: 'top'
                    }
                ],
                yAxis: [
                    {
                        name: '入度',
                        type: 'value',
                    },
                    {
                        gridIndex: 1,
                        name: '出度',
                        type: 'value',
                        inverse: true
                    }
                ],
                series: [
                    {
                        name: '入度',
                        type: 'line',
                        symbolSize: 8,
                        // prettier-ignore
                        data: this.metrix.funcInList
                    },
                    {
                        name: '出度',
                        type: 'line',
                        xAxisIndex: 1,
                        yAxisIndex: 1,
                        symbolSize: 8,
                        // prettier-ignore
                        data: this.metrix.funcOutList
                    }
                ]
            }
    
            this.Chart2 = this.$echarts.init(this.$refs.Chart2)
            this.Chart2.setOption(option2)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart2) {
                    this.Chart2.resize()
                }
            })
            let text = '2.3函数入度、函数出度与可替换性';
            this.pageinfo.total++;
            let pageindex = this.pageinfo.total;
            this.pageinfo.content[text] = pageindex;
        },
        initChart5() {
            let _this = this
            let option5 = {
                title: {
                    text: '函数的可替换性',
                    left: "center",
                    top: "1%"
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    position: function (point, params, dom, rect, size) {
                        return {right: size.viewSize[0] - point[0], top: point[1]}
                    },
                    formatter: (params) => {
                        let num = params[0].data;
                        let funcName = _this.metrix.funcNameList[params[0].dataIndex]
                        return `${funcName}<br /> 值: ${num}`;
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        data: this.metrix.xAxis,
                        axisTick: {
                            alignWithLabel: true
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'Ri',
                        color: "orange",
                        type: 'bar',
                        barWidth: '60%',
                        data: this.metrix.RiList
                    }
                ]
            }
            this.Chart5 = this.$echarts.init(this.$refs.Chart5)
            this.Chart5.setOption(option5)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart5) {
                    this.Chart5.resize()
                }
            })
            this.table5 = [];
            let indexx = 0;
            for (let funcname in this.metrix.funcNameList) {
                indexx++;
                let obj = {};
                obj.index = indexx;
                obj.name = this.metrix.funcNameList[funcname];
                obj.indegree = this.metrix.funcInList[indexx-1];
                obj.outdegree = this.metrix.funcOutList[indexx-1];
                obj.value = this.metrix.RiList[indexx-1];
                this.table5.push(obj);
                
            }
    
            this.check5 = !this.check5;
            this.ChandleTableHeightChange(indexx,this.table5);
    
    
        },
        // C++
        initChart11() {
            let data = []
            let num1 = this.metrix.scalability.interfaceNum
            let num = this.metrix.scalability.classNum
    
            data.push({
                name: "接口类数量",
                value: num1,
                rate: (num1 / num * 100).toFixed(2).toString(),
                itemStyle: {
                    color: "rgb(16, 135, 240)"
                }
            })
            data.push({
                name: "非接口类数量",
                value: num - num1,
                rate: ((num - num1) / num * 100).toFixed(2).toString(),
                itemStyle: {
                    color: "rgb(251, 59, 136)"
                }
            })
            let option11 = {
                title: {
                    text: "接口类占比",
                    left: "center",
                    top: "1%"
                },
                tooltip: {
                    trigger: 'item',
                    formatter: (param) => {
                        let item = param.data;
                        return `${item.name}:<br />${item.value}个<br />${item.rate}%`;
                    }
                },
                legend: {
                    top: 'bottom',
                    left: 'left'
                },
                series: [
                    {
                        name: '数据',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: 40,
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: data,
                        label: {
                            show: true,
                            position: 'inside'
                        },
                    }
                ]
            }
            this.Chart11 = this.$echarts.init(this.$refs.Chart11)
            this.Chart11.setOption(option11)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart11) {
                    this.Chart11.resize()
                }
            })
            this.table11 = []
            let obj = {
                
                "value1":num1,
                "value2":num-num1,
            }
            this.table11.push(obj)
    
            this.check11 = !this.check11;
    
            let text = '3.类信息概况';
            this.pageinfo.total++;
            let pageindex = this.pageinfo.total;
            this.pageinfo.content[text] = pageindex;
            let text2 = '3.1接口类占比';
            // this.pageinfo.total++;
            // let pageindex = this.pageinfo.total;
            this.pageinfo.content[text2] = pageindex;
    
        },
        initChart12() {
            let _this = this
            let option12 = {
                title: {
                    text: '类入度 & 类出度',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        animation: false
                    },
                    position: function (point) {
                        return [point[0], point[1]]
                    },
                    formatter: (params) => {
                        // console.log('params', params)
                        let methodName = _this.metrix.classNameList[params[0].dataIndex]
                        return `${methodName} 入度: ${params[0].data} 出度: ${params[1].data}`
                    }
                },
                legend: {
                    data: ['入度', '出度'],
                    right: 2,
                    bottom: 2
                },
                axisPointer: {
                    link: [
                        {
                            xAxisIndex: 'all'
                        }
                    ]
                },
                grid: [
                    {
                        left: 35,
                        right: 30,
                        height: '35%'
                    },
                    {
                        left: 35,
                        right: 30,
                        top: '55%',
                        height: '35%'
                    }
                ],
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        axisLine: { onZero: true },
                        data: this.metrix.xcAxis
                    },
                    {
                        gridIndex: 1,
                        type: 'category',
                        boundaryGap: false,
                        axisLine: { onZero: true },
                        data: this.metrix.xcAxis,
                        position: 'top'
                    }
                ],
                yAxis: [
                    {
                        name: '入度',
                        type: 'value',
                    },
                    {
                        gridIndex: 1,
                        name: '出度',
                        type: 'value',
                        inverse: true
                    }
                ],
                series: [
                    {
                        name: '入度',
                        type: 'line',
                        symbolSize: 8,
                        // prettier-ignore
                        data: this.metrix.classInList
                    },
                    {
                        name: '出度',
                        type: 'line',
                        xAxisIndex: 1,
                        yAxisIndex: 1,
                        symbolSize: 8,
                        // prettier-ignore
                        data: this.metrix.classOutList
                    }
                ]
            }
    
            this.Chart12 = this.$echarts.init(this.$refs.Chart12)
            this.Chart12.setOption(option12)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart12) {
                    this.Chart12.resize()
                }
            })
            let text = '3.3类入度、类出度与可替换性';
            this.pageinfo.total++;
            let pageindex = this.pageinfo.total;
            this.pageinfo.content[text] = pageindex;
        },
        initChart14() {
            let data1 = {
                name: "类数量",
                num: this.metrix.comprehensibility.classNum,
                value: 100
            }
            let data2 = {
                name: "包含注释的类数量",
                num: this.metrix.comprehensibility.commentClass,
                value: (this.metrix.comprehensibility.commentClass / this.metrix.comprehensibility.classNum * 100).toFixed(2)
            }
            const gaugeData = [
                {
                    value: data2.value,
                    num: data2.num,
                    name: data2.name,
                    title: {
                        offsetCenter: ['0%', '-20%']
                    },
                    detail: {
                        valueAnimation: true,
                        offsetCenter: ['0%', '20%']
                    }
                }
            ]
            let option14 = {
                title: {
                    text: "包含注释的类占比",
                    subtext: "类数量——" + data1.num + "个",
                    left: "center"
                },
                tooltip: {
                    trigger: "item",
                    formatter: (params) => {
                        let { name, num } = params.data;
                        return `${name}<br /> ${num}个`;
                    }
                },
                series: [
                    {
                        name: "数量",
                        type: 'gauge',
                        color: "green",
                        center: ["50%", "58%"],
                        startAngle: 90,
                        endAngle: -270,
                        pointer: {
                            show: false
                        },
                        progress: {
                            show: true,
                            overlap: false,
                            roundCap: true,
                            clip: false,
                            itemStyle: {
                                borderWidth: 1,
                                borderColor: '#464646'
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                width: 30
                            }
                        },
                        splitLine: {
                            show: false,
                            distance: 0,
                            length: 10
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            show: false,
                            distance: 50
                        },
                        data: gaugeData,
                        title: {
                            fontSize: 10
                        },
                        detail: {
                            width: 40,
                            height: 12,
                            fontSize: 10,
                            color: 'inherit',
                            borderColor: 'inherit',
                            borderRadius: 20,
                            borderWidth: 1,
                            formatter: '{value}%'
                        }
                    }
                ]
            }
            this.Chart14 = this.$echarts.init(this.$refs.Chart14)
            this.Chart14.setOption(option14)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart14) {
                    this.Chart14.resize()
                }
            })
            this.table14 = []
            let obj = {
                
                "value1":data2.num,
                "value2":data2.value,
            }
            this.table14.push(obj)
    
            this.check14 = !this.check14;
            let text = '3.2注释类占比';
            // this.pageinfo.total++;
            let pageindex = this.pageinfo.total;
            this.pageinfo.content[text] = pageindex;
        },
        initChart15() {
            let _this = this
            let option15 = {
                title: {
                    text: '类的可替换性',
                    left: "center",
                    top: "1%"
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    position: function (point, params, dom, rect, size) {
                        return {right: size.viewSize[0] - point[0], top: point[1]}
                    },
                    formatter: (params) => {
                        let num = params[0].data;
                        let className = _this.metrix.classNameList[params[0].dataIndex]
                        return `${className}<br /> 值: ${num}`;
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        data: this.metrix.xcAxis,
                        axisTick: {
                            alignWithLabel: true
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'Ri',
                        color: "orange",
                        type: 'bar',
                        barWidth: '60%',
                        data: this.metrix.RciList
                    }
                ]
            }
            this.Chart15 = this.$echarts.init(this.$refs.Chart15)
            this.Chart15.setOption(option15)
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (this.Chart15) {
                    this.Chart15.resize()
                }
            })
            // let prop = 1;
            // this.metrix.classNameList = this.metrix.classNameList * prop;
            // this.metrix.classInList = this.metrix.classInList * prop;
            // this.metrix.classOutList = this.metrix.classOutList * prop;
            // this.metrix.RciList = this.metrix.RciList * prop;
            this.table15 = [];
            let indexx = 0;
            for (let funcname in this.metrix.classNameList) {
                indexx++;
                let obj = {};
                obj.index = indexx;
                obj.name = this.metrix.classNameList[funcname];
                obj.indegree = this.metrix.classInList[indexx-1];
                obj.outdegree = this.metrix.classOutList[indexx-1];
                obj.value = this.metrix.RciList[indexx-1];
                this.table15.push(obj);
                
            }
            
            this.check15 = !this.check15;
            this.handleTableHeightChange(indexx,this.table15);
        //   // 确保 el-table 已经渲染完成，获取其高度
        //   this.$nextTick(() => {
        //     if (this.$refs.myTable) {
        //         console.log("1");
        //       this.handleTableHeightChange(this.$refs.myTable.$el.clientHeight);
        //     }
        //   });
      },
    
        handleTableHeightChange(height,tabledata) {
          this.tableHeight = height;
    
          // 判断当前表格高度是否超过每页最大高度
          if (this.tableHeight > this.maxTableHeightPerPage) {
            // 根据每页最大高度切分数据
            const pageCount = Math.ceil(this.tableHeight / this.maxTableHeightPerPage);
            this.pageinfo.total += pageCount;
    
            this.tableDataPages = new Array(pageCount).fill().map((_, index) => {
              const start = index * this.maxTableHeightPerPage;
              const end = start + this.maxTableHeightPerPage;
    
              return tabledata.slice(start, end);
            });
          } else {
            this.tableDataPages = [tabledata];
          }
        },
    
        ChandleTableHeightChange(height,tabledata) {
          this.tableHeight = height;
    
          // 判断当前表格高度是否超过每页最大高度
          if (this.tableHeight > this.maxTableHeightPerPage) {
            // 根据每页最大高度切分数据
            const pageCount = Math.ceil(this.tableHeight / this.maxTableHeightPerPage);
            this.pageinfo.total += pageCount;
            this.CtableDataPages = new Array(pageCount).fill().map((_, index) => {
              const start = index * this.maxTableHeightPerPage;
              const end = start + this.maxTableHeightPerPage;
    
              return tabledata.slice(start, end);
            });
          } else {
            this.CtableDataPages = [tabledata];
          }
        }
      }
    }
    </script>
    
    <style scoped>
    
    .chart{
      height: 80%
    }
    
    @page {
      size: auto;
      margin: 3mm;
    }
    
    @media print {
      .el-table {
        font-size: 16px;
        color: #000000;
      }
    
         
    }
    /* .el-container {
      min-height: 100vh;
    } */
    
    .main {
        height: 60vh;
        width: 98%;
        display: flex;
        flex-direction: row;
        margin: 1% auto;
    }
    .main1 {
        height: 50%;
        width: 98%;
        display: flex;
        flex-direction: row;
        margin: auto;
        margin-bottom: 10% auto;
    }
    .main2 {
        height: 60%;
        width: 98%;
        display: flex;
        flex-direction: row;
        margin: auto;
    }
    
    .col1 {
        height: 100%;
        width: 65%;
         margin: auto;
    
    }
    
    .col1-1 {
        height: 95%;
        width: 100%;
        margin-bottom: 2%;
        box-shadow: 2px 2px 8px rgb(150, 150, 150);
    }
    
    .col1-2 {
        height: 95%;
        width: 100%;
        margin-bottom: 2%;
    
        box-shadow: 2px 2px 8px rgb(150, 150, 150);
    }
    
    .col2 {
        height: 90%;
        width: 80%;
        margin: auto;
    }
    
    .col2-1 {
        height: 100%;
        width: 100%;
        box-shadow: 2px 2px 8px rgb(150, 150, 150);
    }
    
    .col3 {
        height: 100%;
        width: 65%;
        margin: auto;
    }
    
    .col3-1 {
        height: 68%;
        width: 100%;
        margin-bottom: 10%;
        box-shadow: 2px 2px 8px rgb(150, 150, 150);
    }
    
    .col3-2 {
        height: 68%;
        width: 100%;
        margin-bottom: 2%;
    
        box-shadow: 2px 2px 8px rgb(150, 150, 150);
    }
    
    .mulu_list{
      line-height: 28px;
      position: relative;
      display: flex;
      overflow: hidden;
    }
    .mulu_list p{
      font-family: '微软雅黑',Sans-serif,serif;
      font-size:20px;
      font-style: normal;
      padding:0 10px;
      box-sizing: border-box;
    }
    .detailCards {
      /*外边距*/
      margin-top: 10px;
    }
    
    </style>
    