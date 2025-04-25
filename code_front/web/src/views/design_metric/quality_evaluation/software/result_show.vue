<template>
    <div class="container">
        <el-button class="button" style="right: 10vw" type="success" @click="dialogFormVisible = true">设置最值</el-button>
        <el-button class="button" type="primary" @click="dialogPdfVisible = true">打印</el-button>
        <div class="tree">
            <el-tree ref="menuTree" :data="treeNodes" :props="defaultProps" default-expand-all highlight-current
                node-key="id" :expand-on-click-node="false" @node-click="handleNodeClick" :indent="50" class="el-tree">
                <span class="tree-node" slot-scope="{ node }">
                    <span>{{ node.label }}</span>
                </span>
            </el-tree>
        </div>

        <div class="main">
            <div class="title">{{ selectedNode.label }}</div>
            <div class="cards" style="overflow:auto">
                <el-card v-if="isLeaf && card != null" class="card" shadow="hover" v-for="(card,index) in selectedNode.sub" :key="index">
                    <div slot="header" class="card-header">
                        <el-col :span="12">
                            <div>{{ card.id }}</div>
                        </el-col>
                        <el-col :span="12">
                            <div style="text-align: right;">{{ card.val ? card.val.toFixed(2) : card.val }}</div>
                        </el-col>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>描述</div>
                            </el-col>
                            <el-col :span="12">
                                <div class="text">{{ card.des }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>来源</div>
                            </el-col>
                            <el-col :span="12">
                                <div class="text">{{ card.source }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>来源类型</div>
                            </el-col>
                            <el-col :span="12">
                                <div class="text">{{ card.type }}</div>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>

                <el-card v-if="!isLeaf && card != null" class="card" shadow="hover" v-for="(card,index) in selectedNode.sub" :key="index">
                    <div slot="header" class="card-header">
                        <el-col :span="12">
                            <div>{{ card.id }}</div>
                        </el-col>
                        <el-col :span="12">
                            <div style="text-align: right;">{{ card.val }}</div>
                        </el-col>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>值</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.value ? card.value.toFixed(2) : card.value }}</div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="card-item">
                        <el-row>
                            <el-col :span="12">
                                <div>权重</div>
                            </el-col>
                            <el-col :span="12">
                                <div style="text-align: right;">{{ card.weight ? card.weight.toFixed(2) : card.weight }}
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>
            </div>
        </div>

        <el-dialog width="25%" title="指标最值设置" :visible.sync="dialogFormVisible">
            <div class="file_select">
                <el-button slot="trigger" class="el-button" type="success" @click="importFile" plain>导入模板</el-button>
                <el-button slot="trigger" class="el-button" type="primary" @click="exportFile" plain>导出数据</el-button>
            </div>
            <div style="padding: 0 15px;" v-for="(item, index) in minMaxIndexList" :key="index">
                <div class="titleIndex">{{ item.title }}</div>
                <el-form :inline="true">
                    <el-form-item label="最小值" size="small" >
                        <el-input type="number" v-model="minMaxData[item.label].min" style="width: 5vw;"
                        oninput="if(value < 0 || value > 1000000) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                    </el-form-item>
                    <el-form-item label="最大值" size="small" style="float: right;">
                        <el-input type="number" v-model="minMaxData[item.label].max" style="width: 5vw;"
                        oninput="if(value < 0 || value > 1000000) {value = 0}"
                        onblur="if(value == '' || value == null) {value = 0}"></el-input>
                    </el-form-item>
                </el-form>
            </div>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="getIndexSubInfo">提 交</el-button>
            </div>
        </el-dialog>

        <el-dialog class="scroll_none" title="打印预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
            <pdf_software_eval v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_software_eval>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPdfVisible = false">取 消</el-button>
                <el-button type="primary" @click="goPrint">打 印</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import utils from "@/utils/utils"
import FileSaver from "file-saver"
import pdf_software_eval from "@/views/pdf_template/pdf_software_eval.vue"
import Cache from '@/utils/cache'

export default {
    components: {
        pdf_software_eval
    },
    data() {
        return {
            treeNodes: [],
            defaultProps: {
                label: 'label',
                children: 'subMetric'
            },
            selectedNode: {
                label: "请选择指标",
                sub: []
            },
            isLeaf: false,
            dialogFormVisible: true,
            minMaxIndexList: {},
            minMaxData: {},
            minMaxRes: {},
            dialogPdfVisible: false
        }
    },
    mounted() {
        const _this = this
        utils.axiosMethod({
            method: "GET",
            url: window.ipConfig.baseUrl + "/getMinMaxMetrics/" + _this.$store.state.current_project.name,
            callback: (res) => {
                if (parseInt(res.data.metricCalculated) == -1) {
                    _this.$message.warning('计算未完毕')
                    return
                }
                let data = res.data
                if(Object.keys(data).length == 0) {
                    _this.dialogFormVisible = false
                    _this.getIndexSubInfo()
                    return
                }
                let minMaxIndexList = []
                for (let k1 in data) {
                    let data1 = data[k1]
                    for (let k2 in data1) {
                        let data2 = data1[k2]
                        for (let k3 in data2) {
                            let data3 = data2[k3]
                            data3["min"] = 0
                            data3["max"] = 1
                            minMaxIndexList.push({
                                "label": k3,
                                "title": data3.val != null ? k3 + " — " + data3.val.toFixed(2) : k3
                            })
                        }
                    }
                }
                let minMaxData = {}
                for(let index of minMaxIndexList) {
                    minMaxData[index.label] = {
                        "min": 0,
                        "max": 1
                    }
                }
                _this.minMaxData = minMaxData
                _this.minMaxIndexList = minMaxIndexList
                _this.minMaxRes = res.data
            },
            // catch: (err) => {
            //     _this.$message.warning('获取异常')
            // }
        })
    },
    methods: {
        setMinMax() {
            for(let k in this.minMaxData){
                if(this.minMaxData[k].min >= this.minMaxData[k].max){
                    this.$message.warning("最小值不能超过最大值")
                    return
                }
            }

            let data = this.minMaxRes
            let minMaxData = this.minMaxData
            for (let k1 in data) {
                let data1 = data[k1]
                for (let k2 in data1) {
                    let data2 = data1[k2]
                    for (let k3 in data2) {
                        let data3 = data2[k3]
                        if(k3 in minMaxData) {
                            data3.min = minMaxData[k3].min
                            data3.max = minMaxData[k3].max
                        }
                    }
                }
            }

            const _this = this
            utils.axiosMethod({
                method: "POST",
                url: window.ipConfig.baseUrl + "/setMinMax/" + _this.$store.state.current_project.name,
                data: data,
                callback: (res) => {
                    _this.$message.success("设置成功")
                    _this.getIndexSubInfo()
                },
                catch: (err) => {
                    _this.$message.error("设置最大最小值异常")
                }
            })
            _this.dialogFormVisible = false
        },
        getIndexSubInfo() {
            for(let k in this.minMaxData){
                if(this.minMaxData[k].min >= this.minMaxData[k].max){
                    this.$message.warning("最小值不能超过最大值")
                    return
                }
            }

            let data = this.minMaxRes
            let minMaxData = this.minMaxData
            for (let k1 in data) {
                let data1 = data[k1]
                for (let k2 in data1) {
                    let data2 = data1[k2]
                    for (let k3 in data2) {
                        let data3 = data2[k3]
                        if(k3 in minMaxData) {
                            data3.min = minMaxData[k3].min
                            data3.max = minMaxData[k3].max
                        }
                    }
                }
            }

            const _this = this
            utils.axiosMethod({
                method: "POST",
                url: window.ipConfig.baseUrl + "/getSelectedMetrics/" + _this.$store.state.current_project.name,
                data: data,
                callback: (res) => {
                    if (parseInt(res.data.metricCalculated) == -1) {
                        _this.$message({
                            message: '计算未完毕',
                            type: 'warning'
                        })
                        return
                    }
                    // 将返回的数据转换为嵌套树形嵌套列表
                    let data = res.data.data
                    // console.log("data", data)
                    Cache.setCache("software_eval", data)
                    let treeNodes = []
                    let flag = 1
                    for (let data1 of data) {
                        let treeNodes1 = []
                        for (let data2 of data1.subMetric) {
                            let treeNodes2 = []
                            for (let data3 of data2.subMetric) {
                                let treeNodes3 = []
                                for (let data4 of data3.subMetric) {
                                    if(data4.val != null) {
                                        treeNodes3.push({
                                            id: flag,
                                            label: data4.val != null ? data4.name + " — " + data4.val.toFixed(2) : data4.name,
                                            isLeaf: true,
                                            sub: data4.sub
                                        })
                                        flag++
                                    }
                                }
                                treeNodes2.push({
                                    id: flag,
                                    label: data3.val != null ? data3.name + " — " + data3.val.toFixed(2) : data3.name,
                                    isLeaf: false,
                                    sub: data3.sub,
                                    subMetric: treeNodes3
                                })
                                flag++
                            }
                            treeNodes1.push({
                                id: flag,
                                label: data2.val != null ? data2.name + " — " + data2.val.toFixed(2) : data2.name,
                                isLeaf: false,
                                sub: data2.sub,
                                subMetric: treeNodes2
                            })
                            flag++
                        }
                        treeNodes.push({
                            id: flag,
                            label: data1.val != null ? data1.name + " — " + data1.val.toFixed(2) : data1.name,
                            isLeaf: false,
                            sub: data1.sub,
                            subMetric: treeNodes1
                        })
                        flag++
                    }
                    _this.treeNodes = treeNodes
                    // console.log("$$$$$", treeNodes);
                },
                catch: (err) => {
                    _this.$message.error("获取结果异常")
                }
            })
            _this.dialogFormVisible = false
        },
        handleNodeClick(e) {
            this.selectedNode = e
            // console.log("selectedNode", this.selectedNode)
            this.isLeaf = e.isLeaf
        },
        importFile() {
            let _this = this
            const inputFile = document.createElement("input")
            inputFile.type = "file"
            inputFile.style.display = "none"
            inputFile.id = "fileInput"
            // inputFile.webkitdirectory = false
            // inputFile.multiple = false
            document.body.appendChild(inputFile)
            inputFile.click()
            inputFile.addEventListener("change", function (e) {
                let file = inputFile.files[0]
                // console.log("#########", file)
                if (file.type != "application/json") {
                _this.$message.error("上传文件要求为json格式")
                return
                }
                const reader = new FileReader()
                reader.readAsText(file)
                reader.onload = () => {
                    // console.log("文件内容", JSON.parse(reader.result))
                    let data = null
                    try {
                        data = JSON.parse(reader.result)
                    } catch (e) {
                        _this.$message.error("上传文件解析错误")
                        return
                    }
                    // 逐个字段赋值，防止json格式非法
                    for(let k in data) {
                        if(k in _this.minMaxData) {
                            _this.minMaxData[k] = data[k]
                        }
                    }
                }
            })
        },
        exportFile() {
            let data = this.minMaxData
            let blob = new Blob([JSON.stringify(data)], {
                type: "application/json",
            })
            let downloadName = "software_quality_evaluation_index_min_max_" + new Date().getTime() + ".json";
            FileSaver.saveAs(blob, downloadName);
        },
        goPrint() {
            this.$print(this.$refs.print)
            this.dialogPdfVisible = false
        }
    },
}
</script>

<style scoped>
.container {
    height: 89vh;
    width: 100%;
    display: flex;
}

.tree {
    height: 100%;
    width: 50%;
    overflow: auto;
    padding-left: 5%;
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
    word-break:break-all; 
    word-wrap:break-word;
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
</style>
