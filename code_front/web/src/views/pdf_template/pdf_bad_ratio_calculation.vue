<template>
    <div class="pdf_main" style="width: 21cm;">
        <div>
            <h1 style="text-align: center">{{ this.projectName + " 项目坏味评估报告" }}</h1>
        </div>

        <div v-for="(datainfo, typeName, index) in badtotalData" :key="index">
            <!-- C 代码详情 -->
            <!-- 加一个判断，typeName 是C 还是C++ -->
            <h2>{{ (index + 1) * 2 - 1 + ". " + (typeName == 'c_info' ? "C" : "C++") + " 代码坏味概况" }}</h2>

            <h3>{{ (index + 1) * 2 - 1 + ".1 " + (typeName == 'c_info' ? "C" : "C++") + " 代码坏味个数" }}</h3>

            <el-table style="margin-top: 10px; width: 21cm" :data="datainfo.statisticTable"
                border:header-cell-style="() => { return 'background: antiquewhite;color:black;' }">
                <el-table-column prop="name" label="代码坏味名称" align="center">
                </el-table-column>
                <el-table-column prop="num" label="坏味个数" align="center">
                </el-table-column>
            </el-table>

            <h3>{{ (index + 1) * 2 - 1 + ".2 文件坏味概况" }}</h3>

            <el-table   :data="datainfo.fileBadvalue" style="margin-top: 10px; width: 21cm">
                <!-- 加载fileBadvalue 数据，以表格形式呈现，总共4列 -->
                <el-table-column prop="name" label="文件" align="center">
                </el-table-column>
                <el-table-column prop="filename" label="路径" align="center">
                </el-table-column>
                <el-table-column prop="badSmellNum" label="存在坏味数量" align="center">
                </el-table-column>
                <el-table-column prop="badSmellKindNum" label="存在坏味种类" align="center">
                </el-table-column>
            </el-table>
            <h2>{{ (index + 1) * 2 + ". " + (typeName == 'c_info' ? "C" : "C++") + " 代码坏味详情" }}</h2>
            <div v-for="(card, index2) in datainfo.result" :key="index2">
                <div slot="header" class="card-header">
                    <h3>{{ (index + 1) * 2 + "." + (index2 + 1) + card.name + "——阈值" + card.threshold }}</h3>
                    <h5>定义：{{ card.def }}</h5>
                </div>

                <div class="card-body">
                    <h4>{{ (index + 1) * 2 + "." + (index2 + 1) + ".1 " + card.name + "坏味检测概况" }}</h4>
                    <div class="card-body-index3">
                        <el-table border class="total_table" :data="card.otherInfo"
                            :header-cell-style="() => { return 'background: antiquewhite;color:black;' }"
                            :show-header="false" height="100%"
                            style="margin-top: 10px; width: 21cm">
                            <el-table-column prop="name" align="center">
                            </el-table-column>
                            <el-table-column prop="value" align="center">
                            </el-table-column>
                        </el-table>
                    </div>

                    <h4>{{ (index + 1) * 2 + "." + (index2 + 1) + ".2 " + card.name + "坏味检测详情" }}</h4>
                    <div class="card-body-index2">
                        <el-table :data="card.detectionResults"
                            :header-cell-style="() => { return 'background: antiquewhite;color:black;' }" height="100%"
                            stripe>
                            <el-table-column type="index" align="center">
                            </el-table-column>
                            <el-table-column v-for="(item, index) in Object.keys(card.title)" :key="index" :prop="item"
                                :label="card.title[item]" align="center">
                            </el-table-column>
                        </el-table>

                    </div>
                </div>
            </div>
        </div>
        <el-backtop target=".pdf_main" :right="250" :bottom="60"></el-backtop>
    </div>
</template>

<script>
import Cache from "@/utils/cache.js";
export default {
    data() {
        return {
            projectType: 0,
            projectName: "xx1",
            badtotalData: [],

        }
    },
    mounted() {
        this.projectName = this.$store.state.current_project.name
        this.projectType = this.$store.state.current_project.type
        this.badtotalData = Cache.getCache(this.projectName + "_badtotalResult")
        // 遍历badtotalData，将其中的数据进行处理，将其中的路径进行处理，只保留文件名
        for (let datainfo in this.badtotalData) {
            if (this.badtotalData[datainfo] == null) {
                delete this.badtotalData[datainfo]
                continue
            }
            // console.log("%%%", this.badtotalData[datainfo])
            // console.log("!!!", this.badtotalData[datainfo].fileBadvalue)
            for(let fileBadvalue in this.badtotalData[datainfo].fileBadvalue){
                // console.log(this.badtotalData[datainfo].fileBadvalue[fileBadvalue].filename)
              // 增加一个name属性，只保留文件名
              this.badtotalData[datainfo].fileBadvalue[fileBadvalue].name = this.badtotalData[datainfo].fileBadvalue[fileBadvalue].filename.split("/").pop()
            //   console.log(this.badtotalData[datainfo].fileBadvalue[fileBadvalue].name)
            }
        }
    }
}
</script>
