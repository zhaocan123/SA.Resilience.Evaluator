<template>
    <div>
        <el-main class="main—wrapper">
            <el-card class="box-card">
                <a class="upload" v-on:click="selectCode">
                    <i class="el-icon-folder-opened" style="font-size: 40px;"></i>
                    <div>{{ form.codeRoot === "" ? "选择源码" : form.codeRoot }}</div>
                </a>

            </el-card>

            <el-card class="box-card">
                <a class="upload" v-on:click="selectDocs">
                    <i class="el-icon-folder-opened" style="font-size: 40px;"></i>
                </a>
                <el-select v-model="value" placeholder="Select" style="display: flex;">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"
                        :disabled="item.disabled">
                    </el-option>
                </el-select>


            </el-card>
            <el-form ref="form" :model="form" class="form" style="margin-top: 40px;">

                <el-form-item>
                    <el-input placeholder="请输入项目名称" v-model="form.projectName"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="Submit">立即创建</el-button>
                </el-form-item>
            </el-form>
        </el-main>
        <el-dialog :visible.sync="dialogVisible">
            <p>是否仅源码分析</p>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false;onSubmit()">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog :visible.sync="dialogVisible2">
            <p>必须选择源码</p>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible2 = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible2 = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>


import NaviBar from "./NaviBar";
import utils from "../utils/utils"

export default {
    name: "New",
    components: {NaviBar},
    watch: {
        $route(to, from) {
            if (from.meta.noCache) {
                this.form = {
                    projectName: null,
                    codeRoot: '',
                    fileSelect: null,
                    cddocs: [],
                    pdocs:[]
                }
                this.wddoc = []
                this.value = 1
            }
        }
    },
    data() {
        return {
            dialogVisible: false,
            dialogVisible2: false,
            msg: "",
            form: {
                projectName: null,
                codeRoot: '',
                fileSelect: null,
                fileSelect1: null,
                cddocs: [],
                pdocs:[]
            },
            wddoc: [],
            options: [{
                value: 1,
                label: '选择word文档'
            }, {
                value: 2,
                label: '选择禅道文档',
            }, {
                value: 3,
                label: '选择TMMi文档',
            },
             {
                value: 4,
                label: '选择PingCode文档',
            }],
            value: 1
        }
    },
// created() {
//   this.form.fileSelect = this.$route.params.typeList['fileSelect']
//   console.log("1231231231",this.$route.params.typeList)
// },

    methods: {
        Submit: function () {
            let doc = document.getElementById("docs")
            let code = document.getElementById("code")
            if (code != null && code.files != null && doc != null && doc.files != null) {
                this.onSubmit()
            } else if (code == null || code.files == null) {
                this.dialogVisible2 = true
            } else {
                this.dialogVisible = true;
            }

        }
        ,
        onSubmit: function () {
            if (this.$route.params.typeList != null) {
                this.form.fileSelect = this.$route.params.typeList['fileSelect']
            }
            var formData = new FormData()
            let code = document.getElementById("code");
            let doc = document.getElementById("docs")
            let codedata = code.files
            for (let i = 0; i < codedata.length; i++) {
                formData.append('files', codedata[i])
            }
            let docsdata = null
            if (doc != null && doc.files != null) {
                docsdata = doc.files
                for (let i = 0; i < docsdata.length; i++) {
                    formData.append('docs', docsdata[i])
                }
            }
            formData.append("project", this.form.projectName)
            let url = window.ipConfig.baseUrl + "/upload";
            const _this = this;
            utils.axiosMethod({
                method: "POST",
                url: url,
                data: formData,
                callback: (res) => {
                    if (_this.form.projectName === "" || _this.form.projectName === null) {
                        _this.$message({
                            message: "项目名称不能为空",
                            type: "error",
                        });
                    } else {
                        utils.axiosMethod({
                            method: "post",
                            url: window.ipConfig.baseUrl + "/createProject",
                            data: _this.form,
                            callback: (response) => {
                                if (response.data.createFlag === 1) {
                                    _this.$message({
                                        message: response.data.msg,
                                        type: "error",
                                    });
                                } else if (response.data.createFlag === 0) {
                                    _this.$router.push({name: 'home'})
                                }
                            },
                            catch: (err) => {
                                _this.$message.error("创建异常")
                            }
                        })
                    }
                }
            })
        }
        ,
        selectCode: function () {
            const item = document.getElementById("code")
            if (item != null) {
                item.parentNode.removeChild(item)
            }

            const _this = this
            const inputFile = document.createElement("input")
            inputFile.type = "file"
            inputFile.style.display = "none"
            inputFile.id = "code"
            document.body.appendChild(inputFile)
            inputFile.webkitdirectory = true;
            inputFile.multiple = true;
            inputFile.click()
            inputFile.addEventListener("change", function (e) {
                const file = e.target.files[0];
                let codeRootPath = file.webkitRelativePath
                _this.form.codeRoot = codeRootPath.split("/")[0];
            })
        }
        ,
        selectDocs: function () {
            const item = document.getElementById("docs")
            if (item != null) {
                item.parentNode.removeChild(item)
            }
            if (this.value === 1) {
                const _this = this
                const inputFile = document.createElement("input")
                inputFile.type = "file"
                inputFile.style.display = "none"
                inputFile.id = "docs"
                document.body.appendChild(inputFile)
                inputFile.multiple = true
                inputFile.click()
                inputFile.addEventListener("change", function () {
                    for (let i = 0; i < inputFile.files.length; i++) {
                        const file = inputFile.files[i];
                        _this.wddoc[i] = file.name
                    }
                    _this.$router.push({
                        name: "selectDoc",
                        // 传参给页面
                        params: {wd: _this.wddoc}
                    });
                })
            } else if (this.value === 3) {
                const _this = this
                const inputFile = document.createElement("input")
                inputFile.type = "file"
                inputFile.style.display = "none"
                inputFile.id = "docs"
                document.body.appendChild(inputFile)
                inputFile.multiple = true
                inputFile.click()
                inputFile.addEventListener("change", function () {
                    for (let i = 0; i < inputFile.files.length; i++) {
                        const file = inputFile.files[i];
                        _this.wddoc[i] = file.name
                    }
                    _this.$router.push({
                        name: "selectDoc2",
                        // 传参给页面
                        params: {wd: _this.wddoc}
                    });
                })
            }else if (this.value === 4){
                const _this = this
                const inputFile = document.createElement("input")
                inputFile.type = "file"
                inputFile.style.display = "none"
                inputFile.id = "docs"
                document.body.appendChild(inputFile)
                inputFile.multiple = true
                inputFile.click()
                inputFile.addEventListener("change", function () {
                    for (let i = 0; i < inputFile.files.length; i++) {
                        const file = inputFile.files[i];
                        _this.form.pdocs[i] = file.name
                    }
                })
            } else {
                const _this = this
                const inputFile = document.createElement("input")
                inputFile.type = "file"
                inputFile.style.display = "none"
                inputFile.id = "docs"
                document.body.appendChild(inputFile)
                inputFile.multiple = true
                inputFile.click()
                inputFile.addEventListener("change", function () {
                    for (let i = 0; i < inputFile.files.length; i++) {
                        const file = inputFile.files[i];
                        _this.form.cddocs[i] = file.name
                    }
                })
            }
        }
    }
}
</script>

<style scoped>
.main—wrapper {
    height: 600px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    align-content: center;
    flex-flow: row wrap
}

.box-card {
    width: 40%;
    height: 200px;
    margin-top: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    align-content: center;
}

.box-card:hover {
    background-color: cornsilk;
}

.upload {
    width: 100%;
    height: 100px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    align-content: center;
}

.form {
    margin-top: 40px;
    width: 40%;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    align-content: center;
}
</style>
