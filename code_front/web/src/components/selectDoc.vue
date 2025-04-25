<template>
  <div>
    <el-main class="main—wrapper">
      <el-card class="box-card">
        <el-form ref="form" label-position="left" label-width="400px">
          <el-form-item v-for="(item,index) in docname" :key="item.id" :label="item">
            <el-select v-model="type[index]" placeholder="please select your zone">
              <el-option label="需求文档" :value="1"></el-option>
              <el-option label="测试说明文档" :value="2"></el-option>
              <el-option label="测试报告文档" :value="3"></el-option>
              <el-option label="接口设计文档" :value="4"></el-option>
              <el-option label="系统设计文档" :value="5"></el-option>
              <el-option label="用户手册" :value="6"></el-option>
              <el-option label="维护文档" :value="7"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </el-card>

      <el-form ref="form" class="form" style="margin-top: 40px;">
        <el-form-item>
          <el-button type="primary" @click="onSubmit">选择完成</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="back">返回</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </div>
</template>

<script>


import NaviBar from "./NaviBar";

export default {
  name: "selectDoc",
  components: {NaviBar},
  data() {
    return {
      fileSelect: [],
      type: [],
      doclist: [],
      docname: []
    }
  },
  mounted() {
    this.doclist = this.$route.params.wd
    this.doclist.forEach((self, index) => {
      this.$set(this.docname, index, self)
      this.$set(this.type, index, 1)
    })
  },
  beforeRouteLeave(to, from, next) {
    //设置下一个路由的meta,让列表页面缓存,即不刷新
    to.meta.keepAlive = true;
    next();
  },
  methods: {
    onSubmit: function () {
      // console.log("msg", this.doclist)
      // console.log(this.docname)
      // console.log(this.type)
      this.doclist.forEach((self, index) => {
        switch (this.type[index]) {
          case 1:
            this.fileSelect.push({path: self, type: "需求文档"});
            break
          case 2:
            this.fileSelect.push({path: self, type: "测试说明文档"})
            break
          case 3:
            this.fileSelect.push({path: self, type: "测试报告文档"})
            break
          case 4:
            this.fileSelect.push({path: self, type: "接口设计文档"})
            break
          case 5:
            this.fileSelect.push({path: self, type: "系统设计文档"})
            break
          case 6:
            this.fileSelect.push({path: self, type: "用户手册"})
            break
          case 7:
            this.fileSelect.push({path: self, type: "维护文档"})
            break
        }
      })
      this.$router.push({
        name: "create",
        // 传参给页面
        params: {
          projectName: this.$route.params.projectName,
          typeList: this.fileSelect
        }
      });
    },
    back() {
      // window.history.back()
      this.doclist = []
      this.$router.push({
        name: "create",
        params: {
          projectName: this.$route.params.projectName
        }
      })
    }
  }
}
</script>

<style scoped>

.main—wrapper {
  height: 900px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  /*align-items: center;*/
  align-content: center;
  flex-flow: row wrap
}

.box-card {
  width: 70%;
  height: 600px;
  overflow: auto;
  margin-top: 50px;
  display: flex;
  justify-content: center;
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

<style scoped>

</style>