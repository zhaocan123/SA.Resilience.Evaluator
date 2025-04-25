<template>
    <div>
        <el-button class="button" type="primary" @click="dialogPdfVisible = true">打印</el-button>
        <el-button class="button" style="right: 10vw" type="success" @click="dialogVisible = true">项目名选择</el-button>
        <el-tabs type="card" style="margin: 0 15px 0 15px;" v-model="typeName">
            <el-tab-pane label="C信息" name="c_info"
                v-if="this.$store.state.current_project.projectType == 0 || this.$store.state.current_project.projectType == 2">
                <el-tabs v-loading="loading" v-model="activeName1">
                    <el-tab-pane label="系统级别" name="systemLevel" :key="key1">
                        <systemLevel :typeName="typeName"></systemLevel>
                    </el-tab-pane>
                    <el-tab-pane label="文件级别" name="fileLevel" :key="key1">
                        <fileLevel :typeName="typeName"></fileLevel>
                    </el-tab-pane>
                    <el-tab-pane label="函数级别" name="functionLevel" :key="key1">
                        <functionLevel :typeName="typeName"></functionLevel>
                    </el-tab-pane>
                </el-tabs>
            </el-tab-pane>
            <el-tab-pane label="C++信息" name="c_plus_info"
                v-if="this.$store.state.current_project.projectType == 1 || this.$store.state.current_project.projectType == 2">
                <el-tabs v-loading="loading" v-model="activeName2">
                    <el-tab-pane label="系统级别" name="systemLevel" :key="key1">
                        <systemLevel :typeName="typeName"></systemLevel>
                    </el-tab-pane>
                    <el-tab-pane label="文件级别" name="fileLevel" :key="key1">
                        <fileLevel :typeName="typeName"></fileLevel>
                    </el-tab-pane>
                    <el-tab-pane label="类级别" name="classLevel" :key="key1">
                        <classLevel :typeName="typeName"></classLevel>
                    </el-tab-pane>
                </el-tabs>
            </el-tab-pane>
        </el-tabs>
        <el-dialog title="提示" :visible.sync="dialogVisible" width="30vw" center>
            <span slot="title">项目名选择</span>
            <el-select style="width: 20vw; margin-left: 4vw;" v-model="selectedVersion" placeholder="请选择项目名">
                <el-option v-for="item in versions" :key="item" :label="item" :value="item">
                </el-option>
            </el-select>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="selectVersion()">检 测</el-button>
            </span>
        </el-dialog>

        <el-dialog class="scroll_none" title="打印预览" top="2vh" :visible.sync="dialogPdfVisible" width="60vw" center>
            <pdf_change_infonation_detection v-if="dialogPdfVisible" ref="print" style="height: 70vh; margin: 0 auto; overflow-y: scroll;"></pdf_change_infonation_detection>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogPdfVisible = false">取 消</el-button>
                <el-button type="primary" @click="goPrint">打 印</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import systemLevel from "./result/system_level.vue"
import fileLevel from "./result/file_level.vue"
import functionLevel from "./result/function_level.vue"
import classLevel from "./result/class_level.vue"
import Cache from "@/utils/cache"
import utils from "@/utils/utils"
import pdf_change_infonation_detection from "@/views/pdf_template/pdf_change_infonation_detection.vue"
export default {
    components: {
        systemLevel,
        fileLevel,
        functionLevel,
        classLevel,
        pdf_change_infonation_detection
    },
    data() {
        return {
            typeName: "c_info",
            activeName1: "systemLevel",
            activeName2: "systemLevel",
            dialogVisible: true,
            versions: [],
            selectedVersion: null,
            key1: true,
            loading: false,
            dialogPdfVisible: false
        }
    },
    mounted() {
        if(this.$store.state.current_project.projectType == 1) {
            this.typeName = "c_plus_info"
        } else {
            this.typeName = "c_info"
        }
        let _this = this
        utils.axiosMethod({
            method: "GET",
            url: window.ipConfig.baseUrl + "/get_all_same_project/" + _this.$store.state.current_project.name,
            params: {
                "projectType": _this.$store.state.current_project.projectType
            },
            callback: (response) => {
                _this.versions = response.data
            },
            catch: (err) => {
                _this.$message.error("请求失败")
            }
        })
    },
    methods: {
        getData(data) {
            this.dialogVisible = false
            Cache.setCache("change_information_detection_data", data);
            this.key1 = !this.key1
            this.loading = false
        },
        selectVersion() {
            if(this.selectedVersion == null) {
                this.$message.warning("选择项目不能为空")
                return
            }
            this.loading = true
            let _this = this
            Cache.setCache("selectedVersion", this.selectedVersion)
            utils.axiosMethod({
                method: "GET",
                url: window.ipConfig.baseUrl + "/change_information_detection/" + _this.$store.state.current_project.name,
                params: {
                    "selectedVersion": _this.selectedVersion
                },
                callback: (response) => {
                    _this.getData(response.data)
                },
                catch: (err) => {
                    _this.$message.error("获取异常")
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
.button {
    z-index: 3;
    position: absolute;
    right: 2vw;
}

/* 隐藏滚动条 */
/* .scroll_none ::-webkit-scrollbar{
    display: none;
} */
</style>