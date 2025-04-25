<template>
    <div class="container">
        <div class="main-top">
            <div class="top-left">
                <el-table height="88%" style="margin-top: 10px;" :data="tableData" border
                    :header-cell-style="() => { return 'background: antiquewhite;color:black;' }">
                    <el-table-column prop="name" label="代码坏味名称" align="center">
                    </el-table-column>
                    <el-table-column prop="num" label="坏味个数" align="center">
                    </el-table-column>
                </el-table>
            </div>

            <div class="top-right">
                <div class="top-right-row">
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">DT</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.DT }}秒</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>detection time</span>
                    </el-card>
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">NPF</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.NPF }}个</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span>number of project files</span>
                    </el-card>
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">NCBFS</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.NCFBS }}个</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span v-if="typeName == 'c_info'">number of C files with bad smell</span>
                        <span v-else>number of C++ files with bad smell</span>
                    </el-card>
                </div>
                <div class="top-right-row">
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">NCF</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.NCF }}个</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span v-if="typeName == 'c_info'">number of C files</span>
                        <span v-else>number of C++ files</span>
                    </el-card>
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">RNCF</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.RNCF }}%</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span v-if="typeName == 'c_info'">ratio of number of C files</span>
                        <span v-else>ratio of number of C++ files</span>
                    </el-card>
                    <el-card class="box-card">
                        <el-row slot="header">
                            <el-col :span="12">
                                <div>
                                    <span class="span-header">RNCFBS</span>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div>
                                    <span>{{ cardData.RNCFBS }}%</span>
                                </div>
                            </el-col>
                        </el-row>
                        <span v-if="typeName == 'c_info'">ratio of number of C files with bad smell</span>
                        <span v-else>ratio of number of C++ files with bad smell</span>
                    </el-card>
                </div>

            </div>
        </div>
        <div class="main-bottom">
            <div ref="myChart" class="my-chart"></div>
        </div>
    </div>
</template>

<script>
import Cache from '@/utils/cache.js';
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
            tableData: [],
            cardData: {
                DT: 0,
                NPF: 0,
                NCFBS: 0,
                NCF: 0,
                RNCF: 0,
                RNCFBS: 0,
            }
        }
    },
    mounted() {
        this.tableData = Cache.getCache(this.projectName + "_statisticTable");
        this.cardData = Cache.getCache(this.projectName + "_cardData");
        this.chartInit();
    },
    methods: {
        chartInit() {
            let fileBadvalue = Cache.getCache(this.projectName + "_fileBadvalue");
            let fileNameList = [];
            let badSmellNumList = [];
            let badSmellKindNumList = [];
            for (let index in fileBadvalue) {
                let item = fileBadvalue[index];
                fileNameList.push(item.filename);
                badSmellNumList.push(item.badSmellNum);
                badSmellKindNumList.push(item.badSmellKindNum);
            }
            let option = {
                title: {
                    text: '文件中代码坏味数量及坏味种类数量情况',
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
                    right: '10%',
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                yAxis: {
                    type: 'value'
                },
                xAxis: {
                    type: 'category',
                    data: fileNameList,
                    axisLabel: {
                        show: false
                    }
                },
                series: [
                    {
                        name: 'badSmellNum',
                        type: 'bar',
                        stack: 'total',
                        label: {
                            show: true
                        },
                        emphasis: {
                            focus: 'series'
                        },
                        data: badSmellNumList
                    },
                    {
                        name: 'badSmellKindNum',
                        type: 'bar',
                        stack: 'total',
                        label: {
                            show: true
                        },
                        emphasis: {
                            focus: 'series'
                        },
                        data: badSmellKindNumList
                    },
                ],
            };

            this.myChart = this.$echarts.init(this.$refs.myChart)
            this.myChart.setOption(option)
            let myChart = this.myChart
            // 根据窗口大小进行动态缩放
            window.addEventListener("resize", () => {
                if (myChart) {
                    myChart.resize()
                }
            })
        },
    }
}
</script>

<style scoped>
.container{
    height: 73vh;
    width: 100%;
    overflow-y: scroll;
}
.main-top {
    display: flex;
    width: 100%;
    height: 45vh;
}

.main-bottom {
    width: 100%;
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
    width: 30%;
    height: 75%;
}

.span-header {
    font-size: large;
    font-weight: bold;
}

.my-chart {
    height: 50vh;
    width: 80vw;
    margin: 0 auto;
}
</style>