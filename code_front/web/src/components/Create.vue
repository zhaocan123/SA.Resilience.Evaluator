<template>
  <div>
    <div class="header">
      <el-steps style="width: 100%;" :active="active" process-status="finish" finish-status="success">
        <el-step title="上传项目压缩包"></el-step>
        <el-step title="选择解析目标"></el-step>
        <el-step title="上传项目文档"></el-step>
      </el-steps>
      <div>
        <el-link v-if="active > 0" style="font-size: larger; margin-top: 10px; margin-right: 5vw;" 
          icon="el-icon-back" :underline="false" type="warning"
          @click="goBack">
          上一步
        </el-link>
        <el-link style="font-size: larger; margin-top: 10px;" 
          icon="el-icon-close" :underline="false" type="danger"
          @click="cancel">
          取消
        </el-link>
      </div>
    </div>

    <div v-loading="loading">
      <div class="main" v-if="active == 0">
        <el-card v-loading="processing" class="box-card">
          <a class="upload" v-on:click="selectCode">
            <i class="el-icon-folder-opened" style="font-size: 40px;"></i>
            <div>{{ fileName == null || fileName == "" ? "选择压缩包" : fileName }}</div>
          </a>
        </el-card>
        <el-progress v-if="processing" :percentage="percentage"
        style="width: 40vw;" :text-inside="true" :stroke-width="20" status="success"></el-progress>
        <el-button style="margin-top: 5%;" type="primary" @click="submitProjectZip">上 传</el-button>
      </div>

      <div class="main" v-if="active == 1">
        <el-tree
          class="file-tree"
          :data="fileTree"
          ref="fileTree"
          show-checkbox
          node-key="id"
          accordion
          default-expand-all
          :default-checked-keys="checkedKeys"
          :props="defaultProps">
        </el-tree>
        <el-button style="margin-top: 2%;" type="primary" @click="selectPath">确 定</el-button>
      </div>

      <div class="main" v-if="active == 2">
        <el-card class="box-card">
          <a class="upload" v-on:click="selectDocs">
            <i class="el-icon-folder-opened" style="font-size: 40px;"></i>
            <!-- <i class="el-icon-circle-check" style="font-size: 40px;"></i> -->
          </a>
          <el-select v-model="value" placeholder="Select">
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled">
            </el-option>
          </el-select>
        </el-card>
        <el-button style="margin-top: 5%;" type="primary" @click="submit">提 交</el-button>
      </div>
    </div>

    <el-dialog :visible.sync="dialogVisible">
      <p>是否仅源码分析</p>
      <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="dialogVisible = false;onSubmit()">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog :visible.sync="dialogVisible2">
      <p>必须上传源码</p>
      <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible2 = false">取 消</el-button>
      <el-button type="primary" @click="dialogVisible2 = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import utils from "@/utils/utils"
import axios from 'axios'

export default {
  name: "Create",
  data() {
    return {
      loading: false,
      processing: false,
      percentage: 0,
      active: 0,
      fileTree: [],
      checkedKeys: [],
      defaultProps: {
        children: "children",
        label: "label",
      },
      projectName: null,
      fileSelect: [],
      cddocs: [],
      pdocs: [],
      fileName: null,
      filePathList: [],
      dialogVisible:false,
      dialogVisible2:false,
      msg: "",
      wddoc: [],
      options: [{
          value: 1,
          label: '选择UML文档'
      }
      // , {
      //     value: 2,
      //     label: '选择禅道文档',
      // }, {
      //     value: 3,
      //     label: '选择TMMi文档',
      // }, {
      //     value: 4,
      //     label: '选择PingCode文档',
      // }
    ],
      value: 1
    }
  },
  watch: {
    "$route.params.projectName"(newVal, oldVal) {
      // console.log("@#@#@#", oldVal, newVal);
      this.projectName = newVal
    },
    // 监听防止active越界
    "active"(newVal, oldVal) {
      if(newVal < 0) {
        this.active = 0
      } else if(newVal > 3) {
        this.active = 3
      }
    }
  },
  mounted() {
    this.projectName = this.$route.params.projectName
  },
  methods: {
    goBack(){
      if(this.active >= 1) {
        this.active--
      }
    },
    cancel() {
      Object.assign(this.$data, this.$options.data())
      this.$router.push({name: 'home'})
    },
    submitProjectZip() {
      if (this.projectName === "" || this.projectName === null) {
        this.$message.warning("项目名称不能为空")
        return
      }
      let code = document.getElementById("code")
      if(code == null || code == undefined || code.files.length == 0) {
        this.$message.warning("未选择压缩包文件")
        return
      }
      let codeFile = code.files[0]
      let formData = new FormData()
      formData.append("projectZip", codeFile)
      let url = window.ipConfig.baseUrl + "/uploadProjectZip/" + this.projectName
      const _this = this
      this.processing = true
      axios({
        method: "POST",
        url: url,
        data: formData,
        headers: {'Content-Type': 'multipart/form-data'},
        // 文件上传进度条
        onUploadProgress: (e) => {
          // console.log("---", e);
          _this.percentage = parseInt(e.loaded / e.total * 100)
        }
      })
      .then((res) => {
        _this.processing = false
        _this.percentage = 0
        _this.active++
        _this.checkedKeys = res.data.uvprojx
        _this.fileTree = res.data.floder_tree
      })
      .catch((err) => {
        _this.processing = false
        _this.percentage = 0
        _this.$message.error("提交异常")
      })
    },
    // check(node, treeInfo) {
    //   // console.log(node, treeInfo);
    //   if (treeInfo.checkedNodes.length > 0) {
    //     //单选实现
    //     this.$refs.fileTree.setCheckedNodes([node])
    //   } else {
    //     //删除之前选中的节点
    //     this.$refs.fileTree.setCheckedNodes([])
    //   }
    // },
    selectPath() {
      let nodes = this.$refs.fileTree.getCheckedNodes()
      // console.log("$$$$$$$", nodes)
      if(nodes.length == 0) {
        this.$message.warning("未选择需要解析的文件夹")
        return
      }
      
      // bfs
      // let fileList = []
      // let queue = []
      // let num = 0
      // for(let node of nodes) {
      //   if(node.type == "file") {
      //     fileList.push(node.path)
      //   } else {
      //     queue.push(node)
      //     num++
      //   }
      // }

      // while(queue.length != 0) {
      //   let nextNum = 0
      //   while(num-- > 0) {
      //     let node = queue.shift()
      //     for(let i in node.children) {
      //       let child = node.children[i]
      //       if(child.type == "file") {
      //         fileList.push(child.path)
      //       } else {
      //         queue.push(child)
      //         nextNum++
      //       }
      //     }
      //   }
      //   num = nextNum
      // }

      let fileList = []
      for(let node of nodes) {
        if(node.type == "file") {
          fileList.push(node.path)
        }
      }
      // console.log("^^^^^^^^^", fileList);
      this.filePathList = fileList
      this.active++
    },
    submit:function(){
      let doc = document.getElementById("docs")
      let code = document.getElementById("code")
      if(code!=null&&code.files!=null&&doc!=null&&doc.files!=null) {
        this.onSubmit()
      }else if(code==null||code.files==null){
        this.dialogVisible2 = true
      } else{
        this.dialogVisible = true;
      }
    },
    onSubmit: function () {
      this.loading = true
      if (this.projectName == "" || this.projectName == null) {
        this.$message.warning("项目名称不能为空")
        return
      }
      let formData = new FormData()
      let createFormData = {}
      if(this.$route.params.typeList != null) {
        this.fileSelect = this.$route.params.typeList
      }
      formData.append("project", this.projectName)
      createFormData["projectName"] = this.projectName
      formData.append("selectCodeFiles", this.filePathList)
      createFormData["selectCodeFiles"] = this.filePathList
      formData.append("cddocs", this.cddocs)
      createFormData["cddocs"] = this.cddocs
      formData.append("pdocs", this.pdocs)
      createFormData["pdocs"] = this.pdocs
      formData.append("fileSelect", JSON.stringify(this.fileSelect))
      createFormData["fileSelect"] = this.fileSelect

      let doc = document.getElementById("docs")
      if(doc != null && doc.files != null) { 
        for (let docsdata of doc.files) {
          formData.append('docs', docsdata)
        }
      }
      let url = window.ipConfig.baseUrl + "/uploadProjectFile/" + this.projectName;
      const _this = this;
      utils.axiosMethod({
        method: "POST",
        url: url,
        data: formData,
        callback: (res) => {
          utils.axiosMethod({
            method: "post",
            url: window.ipConfig.baseUrl + "/createProject",
            data: createFormData,
            callback: (new_res) => {
              if (new_res.data.createFlag === 1) {
                _this.loading = false
                _this.$message.error(new_res.data.msg);
              } else if (new_res.data.createFlag === 0) {
                _this.loading = false
                _this.$message.success("创建项目成功")
                _this.active++
                setTimeout(() => {
                  // 清空所有数据
                  Object.assign(_this.$data, _this.$options.data())
                  _this.$router.push({name: 'home'})
                }, 1500);
              }
            }
          })
        },
        catch: (err) => {
          _this.loading = false
          _this.$message.error("请求异常")
        }
      })
    },
    selectCode: function () {
      const item = document.getElementById("code")
      if(item!=null){
        item.parentNode.removeChild(item)
      }
      const _this = this
      const inputFile = document.createElement("input")
      inputFile.type = "file"
      inputFile.style.display = "none"
      inputFile.id = "code"
      inputFile.accept = ".zip,.rar,.tar"
      document.body.appendChild(inputFile)
      inputFile.click()
      inputFile.addEventListener("change", function (e) {
        const file = e.target.files[0];
        _this.fileName = file.name;
      })
    },
    selectDocs: function () {
      const item = document.getElementById("docs")
      if(item!=null){
        item.parentNode.removeChild(item)
      }
      const _this = this
      const inputFile = document.createElement("input")
      inputFile.type = "file"
      inputFile.style.display = "none"
      inputFile.id = "docs"
      // inputFile.accept = ".doc,.docx,.csv,.xls,.xlsx"
      inputFile.multiple = true
      document.body.appendChild(inputFile)
      inputFile.click()
      if (this.value === 1) {
        inputFile.addEventListener("change", function () {
          for (let i = 0; i < inputFile.files.length; i++) {
            const file = inputFile.files[i];
            _this.wddoc[i] = file.name
          }
          _this.$router.push({
            name: "selectDoc",
            // 传参给页面
            params: {
              projectName: _this.projectName,
              wd: _this.wddoc
            }
          });
        })
      } else if (this.value === 3) {
          inputFile.addEventListener("change", function () {
              for (let i = 0; i < inputFile.files.length; i++) {
                  const file = inputFile.files[i];
                  _this.wddoc[i] = file.name
              }
              _this.$router.push({
                  name: "selectDoc2",
                  // 传参给页面
                  params: {
                    projectName: _this.projectName,
                    wd: _this.wddoc
                  }
              });
          })
      } else if (this.value === 4){
          inputFile.addEventListener("change", function () {
              for (let i = 0; i < inputFile.files.length; i++) {
                  const file = inputFile.files[i];
                  _this.pdocs[i] = file.name
              }
          })
      } else {
        inputFile.addEventListener("change", function () {
          for (let i = 0; i < inputFile.files.length; i++) {
            const file = inputFile.files[i];
            _this.cddocs[i] = file.name
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.header {
  width: 100vw;
  height: 15vh;
  padding: 15px 3%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.main {
  /* height: 600px; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.file-tree {
  height: 65vh;
  width: 100vw;
  padding-left: 5vw;
  padding-right: 5vw;
  overflow-y: scroll;
}

.box-card {
  width: 40vw;
  height: 30vh;
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

</style>
