<template>
	<div class="container">
        <div class="card" v-for="(card, index) in badRatioResult" :key="index">
            <el-card shadow="always">
                <div slot="header" class="card-header">
                    {{ card.name }}
                </div>
                <div class="card-body">
                    <div class="card-body-index1">
                        <div style="margin-top:10%; margin-bottom:30%;">定义：{{ card.def }}</div>
                        <div>阈值：{{ card.threshold }}</div>
                    </div>
                    <div class="card-body-index2">
                        <el-table
                        :data="card.detectionResults"
                        :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}"
                        height="95%"
                        stripe>
                            <el-table-column
                            type="index"
                            align="center">
                            </el-table-column>
                            <el-table-column
                            v-for="(item, index) in Object.keys(card.title)"
                            :key="index"
                            :prop="item"
                            :label="card.title[item]"
                            align="center">
                            </el-table-column>
                        </el-table>
                        <el-pagination
                            small
                            background
                            layout="prev, pager, next"
                            :current-page.sync="card.currentPage"
                            :page-size="20"
                            :total="card.totalNum"
                            @current-change="currentChange(card.key, index, card.currentPage)">
                        </el-pagination>
                    </div>
                    <div class="card-body-index3">
                        <el-table
                        class="total_table"
                        :data="card.otherInfo"
                        :header-cell-style="()=>{return 'background: antiquewhite;color:black;'}"
                        :show-header="false"
                        height="100%">
                            <el-table-column
                            prop="name"
                            align="center">
                            </el-table-column>
                            <el-table-column
                            prop="value"
                            align="center">
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-card>
        </div>
	</div>
</template>

<script>
import Cache from "@/utils/cache.js"
import utils from '@/utils/utils'
export default {
    props: ["typeName"],
	data(){
		return {
            badRatioResult: [],
            projectName: this.$store.state.current_project.name
		}
	},
    watch: {
        typeName(newVal) {
            this.typeName = newVal
            // this.getData()
        }
    },
	mounted(){
        let badRatioResult = Cache.getCache(this.projectName + "_badSmellKindNum")
        console.log("$$$$", this.projectName + "_badSmellKindNum", badRatioResult);
        for(let item of badRatioResult) {
            item["currentPage"] = 1
        }
        this.badRatioResult = badRatioResult
	},
	methods: {
        currentChange(key, index, currentPage) {
            let str = this.typeName == "c_plus_info" ? "cpp_" : "c_"
            const _this = this
            utils.axiosMethod({
                url: window.ipConfig.baseUrl + "/bad_ratio_detect/detection_results/" + str + key + "/" +  _this.$store.state.current_project.name + "/" + currentPage,
                method: "GET",
                callback: (res) => {
                    _this.badRatioResult[index].detectionResults = res.data.detectionResults
                },
                catch: (err) => {
                    _this.$message.error("获取数据异常")
                }
            })
        }
	}
}
</script>

<style scoped>
    .container{
        width: 100%;
        height: 73vh;
        overflow-y: scroll;
    }
    .card{
        width: 96%;
        padding: 8px;
    }
    .card-header{
        font-weight: bolder;
        font-size:calc(100vw * 16 / 1920);
    }
    .card-body{
        display: flex;
        width: 100%;
        height: 50vh;
    }
    .card-body-index1{
        width: 20%;
        height: 100%;
    }
    .card-body-index2{
        width: 40%;
        height: 100%;
    }
    .card-body-index3{
        width: 40%;
        height: 100%;
    }
</style>