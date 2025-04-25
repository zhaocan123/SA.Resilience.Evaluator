<template>
    <div class="container">
        <div class="main-top">
            <div class="top-left">
                <div ref="myChart0" class="resilience-chart"></div>
            </div>

            <div class="top-right">
                <div class="top-right-row">
                    <el-card class="box-card"> 
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">系统韧性值</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.resilience }}</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>对当前系统的韧性评估结果值</span>
                    </el-card>
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">平均节点韧性</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.average_node_resilience }}</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>系统中平均每个节点的韧性值</span>
                    </el-card>
                    <!-- <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">攻击面韧性</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.attack_surface_resilience }}</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>系统暴露在攻击面中的部分的韧性评估值</span>
                    </el-card> -->
                </div>
                <div class="top-right-row">
                    <!-- <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">潜在攻击总数</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.total_attack_num }}个</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>系统可能受到的潜在攻击的总数</span>
                    </el-card> -->
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">攻击面大小</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.entry_exit_points_num }}个</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>系统攻击面包含的节点个数</span>
                    </el-card>
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">平均攻击个数</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.average_attack_num }}</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>系统平均每个节点受到攻击的个数</span>
                    </el-card>
                    <!-- <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">平均恢复率</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.average_recovery }}</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>系统中平均每个节点从攻击中恢复的概率</span>
                    </el-card> -->
                </div>

            </div>
        </div>
        <div class = "main-bottom">
            <el-col :span="8" style="height: 100%">
                    <div ref="myChart1" class="my-chart"></div>
            </el-col>
            <el-col :span="8" style="height: 100%">
                    <div ref="myChart2" class="my-chart"></div>
            </el-col>
            <el-col :span="8" style="height: 100%">
                    <div ref="myChart3" class="my-chart"></div>
            </el-col>
        </div>
    </div>
</template>

<script>
import utils from "@/utils/utils";
export default {
    props: ["typeName"],
    watch: {
        typeName(newVal) {
            this.typeName = newVal
            this.chartInit()
        }
    },
    data() {
        return {
            projectName: this.$store.state.current_project.name,
            cardData: {
                resilience: -1,
                attack_node_prob: -1,
                attack_surface_resilience: -1,
                total_attack_num: -1,
                average_attack_num: -1,
                average_recovery: -1
            },
            resilience_distribution : [],
            capec_distribution: [],
            top10_distribution : []
        }
    },
    mounted() {
        let _this = this;
        utils.axiosMethod({
        method: "GET",
        url:
            window.ipConfig.baseUrl + "/RESILIENCE_REPORT_INFO/" + _this.$store.state.current_project.name,
        callback: (res) => {
            // console.log(res.data)
            let resilience_data = JSON.parse(JSON.stringify(res.data));
            _this.cardData = resilience_data.cardData;
            _this.resilience_distribution = resilience_data.resilience_distribution;
            _this.capec_distribution = resilience_data.capec_distribution;
            _this.top10_distribution = resilience_data.top10_distribution;
            // get table and card data
            this.resilence_chart_init();
            // get graph data
            this.chartInit();
        },
        });
        
    },
    methods: {
        resilence_chart_init(){
            let option = {
            series: [
                {
                type: 'gauge',
                center: ['50%', '50%'],
                startAngle: 200,
                endAngle: -20,
                min: 0,
                max: 1,
                splitNumber: 10,
                itemStyle: {
                    color: '#FFAB91'
                },
                progress: {
                    show: true,
                    width: 15
                },
                pointer: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                    width: 30
                    }
                },
                axisTick: {
                    distance: -45,
                    splitNumber: 5,
                    lineStyle: {
                    width: 2,
                    color: '#999'
                    }
                },
                splitLine: {
                    distance: -52,
                    length: 14,
                    lineStyle: {
                    width: 3,
                    color: '#999'
                    }
                },
                axisLabel: {
                    distance: -20,
                    color: '#555',
                    fontSize: 10
                },
                anchor: {
                    show: false
                },
                title: {
                    show: false
                },
                detail: {
                    valueAnimation: true,
                    width: '60%',
                    lineHeight: 40,
                    borderRadius: 8,
                    offsetCenter: [0, '-15%'],
                    fontSize: 15,
                    fontWeight: 'bolder',
                    formatter: 'Resilience: {value}',
                    color: 'inherit'
                },
                data: [
                    {
                    value: this.cardData.resilience
                    }
                ]
                }
            ]
            };
            this.myChart0 = this.$echarts.init(this.$refs.myChart0)
            this.myChart0.setOption(option)
            let myChart0 = this.myChart0
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (myChart0) {
                    myChart0.resize()
                }
            })
        },
        left_chart_init(){
            let option = {
                title: {
                    text: 'TOP10危险节点攻击数量/概率分布',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        // Use axis to trigger tooltip
                        type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
                    }
                },
                legend: {
                    left: '10%',
                },
                dataset: {
                    source: this.top10_distribution,
                },
                grid: { containLabel: true },
                xAxis: { name: 'amount' },
                yAxis: { type: 'category' },
                visualMap: {
                    orient: 'horizontal',
                    left: 'center',
                    min: 0,
                    max: 10,
                    text: ['High Score', 'Low Score'],
                    // Map the score column to color
                    dimension: 0,
                    inRange: {
                    color: ['#65B581', '#FFCE34', '#FD665F']
                    }
                },
                series: [
                    {
                    type: 'bar',
                    encode: {
                        // Map the "amount" column to X axis.
                        x: 'amount',
                        // Map the "product" column to Y axis
                        y: 'product'
                    }
                    }
                ]
            };
            this.myChart1 = this.$echarts.init(this.$refs.myChart1)
            this.myChart1.setOption(option)
            let myChart1 = this.myChart1
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (myChart1) {
                    myChart1.resize()
                }
            })
        },
        mid_chart_init(){
            let option = {
                title: {
                    text: '系统节点韧性分布',
                    left: 'center'
                },
                xAxis: {
                    name: '韧性值',
                    type: 'category',
                    data: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
                },
                yAxis: {
                    name: '数量',
                    type: 'value'
                },
                series: [
                    {
                    data: this.resilience_distribution,
                    type: 'bar',
                    showBackground: true,
                    backgroundStyle: {
                        color: 'rgba(180, 180, 180, 0.2)'
                    }
                    }
                ]
            };
            this.myChart2 = this.$echarts.init(this.$refs.myChart2)
            this.myChart2.setOption(option)
            let myChart2 = this.myChart2
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (myChart2) {
                    myChart2.resize()
                }
            })
        },
        right_chart_init(){
            let option = {
                title: {
                    text: 'CAPEC-潜在攻击分布',
                    left: 'center'
                },
                legend: {
                    top: 'bottom'
                },
                toolbox: {
                    show: true,
                    feature: {
                    mark: { show: true },
                    dataView: { show: true, readOnly: false },
                    restore: { show: true },
                    saveAsImage: { show: true }
                    }
                },
                series: [
                    {
                    name: 'Nightingale Chart',
                    type: 'pie',
                    radius: [10, 125],
                    center: ['50%', '50%'],
                    roseType: 'area',
                    itemStyle: {
                        borderRadius: 8
                    },
                    data: this.capec_distribution,
                    
                    }
                ]
            };
            this.myChart3 = this.$echarts.init(this.$refs.myChart3)
            this.myChart3.setOption(option)
            let myChart3 = this.myChart3
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (myChart3) {
                    myChart3.resize()
                }
            })
        },
        chartInit() {
            this.left_chart_init();
            this.mid_chart_init();
            this.right_chart_init();
            
        },
    }
}
</script>

<style scoped>
.container{
    height: 90vh;
    width: 100%;
    overflow-y: scroll;
}
.main-top {
    display: flex;
    width: 100%;
    height: 40vh;
}

.main-bottom {
    display: flex;
    width: 100%;
    height: 45vh;
}

.left-bottom {
    width: 30%;
}

.center-bottom {
    width: 30%;
}

.right-bottom {
    width: 30%;
}

.top-left {
    width: 30%;
}

.top-right {
    width: 70%;
}

.top-right-row {
    height: 50%;
    display: flex;
}

.box-card {
    margin-top: 10px;
    margin-left: 15px;
    width: 45%;
    height: 75%;
}

.span-header {
    font-size: large;
    font-weight: bold;
}

.my-chart {
    height: 40vh;
    width: 32vw;
    margin: 0 auto;
}

.resilience-chart {
    height: 100%;
    width: 100%;
    margin-top: 20px;
}
</style>