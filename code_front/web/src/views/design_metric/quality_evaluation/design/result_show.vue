<template>
    <div style="height: 80vh;">
        <el-button style="position: absolute; right: 2vw; z-index: 3;" type="primary" @click="dialogPdfVisible = true">打印</el-button>

        <el-tabs v-if="this.$store.state.current_project.projectType != 0" type="card" v-model="activeName" @tab-click="changeInfo">
            <el-tab-pane label="函数信息" name="funcInfo"></el-tab-pane>
            <el-tab-pane label="类信息" name="classInfo"></el-tab-pane>
        </el-tabs>


        <div class="main" v-if="activeName == 'funcInfo'">
            <div class="col1">
                <div ref="Chart1" class="col1-1"></div>
                <div ref="Chart2" class="col1-2"></div>
            </div>
            <div class="col2">
                <div ref="Chart3" class="col2-1"></div>
            </div>
            <div class="col3">
                <div ref="Chart4" class="col3-1"></div>
                <div ref="Chart5" class="col3-2"></div>
            </div>
        </div>
        <div class="main" v-else>
            <div class="col1">
                <div ref="Chart11" class="col1-1"></div>
                <div ref="Chart12" class="col1-2"></div>
            </div>
            <div class="col2">
                <div ref="Chart13" class="col2-1"></div>
            </div>
            <div class="col3">
                <div ref="Chart14" class="col3-1"></div>
                <div ref="Chart15" class="col3-2"></div>
            </div>
        </div>

        <el-dialog class="scroll_none" title="打印预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
            <pdf_design_eval v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_design_eval>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPdfVisible = false">取 消</el-button>
                <el-button type="primary" @click="goPrint">打 印</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import utils from '@/utils/utils'
import Cache from "@/utils/cache"
import pdf_design_eval from "@/views/pdf_template/pdf_design_eval.vue"

export default {
    components: {
        pdf_design_eval
    },
    data() {
        return {
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
            dialogPdfVisible: false
        }
    },
    mounted() {
        let _this = this
        utils.axiosMethod({
            method: "GET",
            url: window.ipConfig.baseUrl + "/getDesignMetric/" + _this.$store.state.current_project.name,
            callback: (response) => {
                _this.metrix = response.data.metrix
                Cache.setCache("design_eval", response.data.metrix)
                _this.changeInfo()
            },
            catch: (err) => {
                _this.$message.error("获取异常")
            }
        })
    },
    methods: {
        changeInfo(){
            setTimeout(() => {
                if(this.activeName == "funcInfo") {
                    this.initChart1()
                    this.initChart2()
                    this.initChart3()
                    this.initChart4()
                    this.initChart5()
                } else {
                    this.initChart11()
                    this.initChart12()
                    // this.initChart3()
                    this.initChart14()
                    this.initChart15()
                }
            }, 100)
        },
        initChart1() {
            let data = []
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
            for (let key in map) {
                indicator.push({
                    name: map[key],
                    max: 1
                })
                values.push(this.metrix[key].value.toFixed(3))
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
            })
        },
        initChart4() {
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
        },
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
        },
        goPrint() {
            this.$print(this.$refs.print)
            this.dialogPdfVisible = false
        }
    }
}
</script>

<style scoped>
.main {
    height: 80vh;
    width: 98%;
    display: flex;
    flex-direction: row;
    margin: 1% auto;
}

.col1 {
    height: 100%;
    width: 25%;
}

.col1-1 {
    height: 48%;
    width: 100%;
    margin-bottom: 2%;
    box-shadow: 2px 2px 8px rgb(150, 150, 150);
}

.col1-2 {
    height: 48%;
    width: 100%;
    box-shadow: 2px 2px 8px rgb(150, 150, 150);
}

.col2 {
    height: 97%;
    width: 48%;
    margin: 0 auto;
}

.col2-1 {
    height: 100%;
    width: 100%;
    box-shadow: 2px 2px 8px rgb(150, 150, 150);
}

.col3 {
    height: 100%;
    width: 25%;
}

.col3-1 {
    height: 48%;
    width: 100%;
    margin-bottom: 2%;
    box-shadow: 2px 2px 8px rgb(150, 150, 150);
}

.col3-2 {
    height: 48%;
    width: 100%;
    box-shadow: 2px 2px 8px rgb(150, 150, 150);
}
</style>