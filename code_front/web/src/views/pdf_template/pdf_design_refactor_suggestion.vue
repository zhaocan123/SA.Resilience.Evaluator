<template>
    <div class="pdf_main" style="width: 21cm;">
        <div>
            <h1 style="text-align: center;">{{ this.projectName }} 项目设计重构建议</h1>
        </div>
        <div>
            <h1>1.重构阈值</h1>
            <el-table class="total_table" stripe :header-cell-style="{ textAlign: 'center' }"
                :cell-style="{ textAlign: 'center' }" :data="this.thresholdtable">
                <el-table-column prop="name" label="阈值名称" min-width="30%">
                </el-table-column>
                <el-table-column prop="detail" label="阈值设置详情" min-width="70%">
                </el-table-column>
            </el-table>

        </div>
        <div>
            <h1>2.重构建议</h1>
            <div v-for="(suggestion, index) in suggestionTable" :key="index">
                <h2>2.{{ index + 1 }} 重构建议{{ index + 1 }}</h2>
                <h3>2.{{ index + 1 }}.1 建议内容</h3>
                <h4>&emsp;&emsp;{{ suggestion.suggestion }}</h4>
                <h3>2.{{ index + 1 }}.2 建议详情</h3>

                <el-table class="total_table" style=" text-align: center;" :data="suggestion.details"
                    :header-cell-style="() => { return 'background: rgb(240,249,235);color:black;' }" stripe>
                    <el-table-column prop="funcName" label="函数名" align="center">
                    </el-table-column>
                    <el-table-column label="信息" align="center">
                        <template slot-scope="scope">
                            <el-tag type="warning" style="margin-right: 1px;"
                                v-for="(item, index) in Object.keys(scope.row.info)" :key="index">
                                {{ scope.row.info[item].label }} : {{ scope.row.info[item].value }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="path" label="所在路径" align="center">
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <el-backtop target=".pdf_main" :right="250" :bottom="60"></el-backtop>
    </div>
</template>

<script>
import utils from '@/utils/utils';
import Cache from "@/utils/cache"
export default {
    data() {
        return {
            suggestionData: [],
            suggestionTable: [],
            threshold: {
                "par": [0, 0],
                "var": [0, 0],
                "cir": [0, 0],
                "out": [0, 0],
                "in": [0, 0]
            },
            projectName: this.$store.state.current_project.name,
            thresholdtable: [{
                name: '参数个数',
                detail: '0'
            }, {
                name: '变量个数',
                detail: '0'
            }, {
                name: '圈复杂度',
                detail: '0'
            }, {
                name: '出度',
                detail: '0'
            }, {
                name: '入度',
                detail: '0'
            }]
        }
    },
    mounted() {
        // this.suggestionData = Cache.getCache("design_refactor_suggestion_data"),
        this.suggestionTable = Cache.getCache("design_refactor_suggestion_data_suggestionTable")
        this.threshold = Cache.getCache("design_refactor_suggestion_threshold")
        // console.log(this.threshold)
        this.$set(this.thresholdtable[0], "detail", `参数个数:${this.threshold.par[0]}%,函数的参数个数不超过${this.threshold.par[1]}`)
        this.$set(this.thresholdtable[1], "detail", `变量个数:${this.threshold.var[0]}%,函数的局部变量个数不超过${this.threshold.var[1]}`)
        this.$set(this.thresholdtable[2], "detail", `圈复杂度:${this.threshold.cir[0]}%,函数的圈复杂度不超过${this.threshold.cir[1]}`)
        this.$set(this.thresholdtable[3], "detail", `出度:${this.threshold.out[0]}%,函数的出度不超过${this.threshold.out[1]}`)
        this.$set(this.thresholdtable[4], "detail", `入度:${this.threshold.in[0]}%,函数的入度不超过${this.threshold.in[1]}`)
        // console.log(this.suggestionData)
        // console.log(this.suggestionTable)
    },
    methods: {

    }
}
</script>

