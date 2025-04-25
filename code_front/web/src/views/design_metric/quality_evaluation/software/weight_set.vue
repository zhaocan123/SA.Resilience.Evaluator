<template>
  <div>
    <el-container style="height: 88vh; border: 1px solid #eee">
      <el-aside>
        <div class="grid-content">
          <el-tree :data="treeData" :props="treeProps" node-key="id" max-depth="1" highlight-current default-expand-all
            :expand-on-click-node="false" :filter-node-method="filterNode" @node-click="handleNodeClick">
            <span class="custom-tree-node" slot-scope="{ node }">
              <span>{{ node.label }}</span>
              <span>
                <el-button type="text" size="mini" icon="el-icon-edit">
                  设置权重
                </el-button>
              </span>
            </span>
          </el-tree>
        </div>
      </el-aside>
      <el-main style="height: 100%">
        <div style="height: 38px; " v-if="this.metricSelected !==0">
          <span class="back" @click="back">
            <i class="el-icon-back"></i>
            上一步
          </span>
          <el-divider direction="vertical"></el-divider>
          <div v-if="tableName!=='' " style="display: inline-block">
            <span style="font-weight: bold;font-size: 25px">"{{ tableName }}"子指标权重设置</span>
          </div>

          <el-button type="primary" style="float: right;margin-right: 20px;" size="medium" @click="toResult">下一步
          </el-button>
          <el-button type="primary" style="float: right;margin-right: 10px;" size="medium" @click="toCheck">校验
          </el-button>
          <!-- 新增，关于权重的说明按钮-->
          <el-button @click="dialogTableVisible = true"
                     type="warning" style="float: right;margin-right: 10px;" icon="el-icon-question">权重说明
          </el-button>

          <el-dialog title="权重说明" :visible.sync="dialogTableVisible">
            <!--表名：层次分析法判断矩阵标准，居中，字体加粗-->
            <h3 style="text-align: center;font-weight: bold">层次分析法判断矩阵标准</h3>
            <!--加载表格，并从data中加载每行的背景色-->
            <el-table :data="gridData" border style="font-size: 16px" :row-style="tableRowClassName"
                      :header-cell-style="{backgroundColor:'#e3e3e3',color:'0D0B0BFF',fontSize:'18px'}">
              <el-table-column property="level" label="指标相比于另一指标" align="center"></el-table-column>
              <el-table-column property="weight" label="量化值" align="center"></el-table-column>
            </el-table>

            <p style="margin-top: 5%; font-size:16px"><strong>应用示例:</strong>功能性:性能效率<br/>
              （1）如果权值为1:5，表示<strong>性能效率</strong>相对于<strong>功能性</strong><span
                  style="color: #fdd381">较强重要</span><br/>
              （2）如果权值为5:1，表示<strong>功能性</strong>相对于<strong>性能效率</strong><span
                  style="color: #fdd381">较强重要</span></p>
          </el-dialog>

        </div>
        <div v-if="this.metricSelected ===0">
          <span></span>
          <el-col :sm="12" :lg="6">
            <el-result icon="success" title="提示" subTitle="您选择的指标不需要设置权重">
              <template slot="extra">
                <el-button type="primary" size="medium" @click="toResultWithNoWeight">下一步</el-button>
              </template>
            </el-result>
          </el-col>
        </div>

        <!-- 用表格设置彼此之间的权重-->
        <el-table :data="tableDetial" style="width: 100%;margin-top: 30px;" v-if="this.metricSelected !==0">
          <el-table-column fixed width="100" align="center" prop="name"></el-table-column>
          <!--从tableData中取出每个label,组合成n*n表格-->
          <div v-for="(tdata,index) in tableData" :key="index">
            <el-table-column :label="tdata" align="center">
              <template slot-scope="scope">
                <!--                weightMatrix[scope.$index][index] weightData[tableName].data[scope.$index][index]-->
                <el-select v-model="weightMatrix[scope.$index][index]" v-if="scope.$index>index"
                  @change="((val)=>changeEvent(val,tableName,scope.$index, index))">
                  <el-option v-for="item in weightOptions" :key="item.value" :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
                <el-select v-model="weightMatrix[scope.$index][index]" v-else disabled
                  @change="((val)=>changeEvent(val,tableName,scope.$index, index))">
                  <el-option v-for="item in weightOptions" :key="item.value" :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </template>
            </el-table-column>
          </div>

        </el-table>

      </el-main>
    </el-container>

  </div>
</template>

<script>
import utils from "@/utils/utils"
import config from "@/config"

export default {

  name: "weight_set",
  data() {
    return {
      // 新增，关于权重的dialogTableVisible: false,
      dialogTableVisible: false,
      gridData: [{
        level: '同等重要',
        weight: '1',
        color: '#fdeeba'
      }, {
        level: '稍微重要',
        weight: '3',
        color: '#f7e16f'
      }, {
        level: '较强重要',
        weight: '5',
        color: '#fdd381'
      }, {
        level: '强烈重要',
        weight: '7',
        color: '#f0b76f'
      }, {
        level: '极端重要',
        weight: '9',
        color: '#e59c58'
      }, {
        level: '两相邻判断的中间值',
        weight: '2, 4, 6, 8',
        color: '#fff8e3'
      }],

      // main部分的表格数据,传入子指标的数据
      tableData: [],
      tableName: "",
      tableDetial: [],

      // 所选指标树
      metricTree: {},
      metricSelected: 1, // -1表示从来没存储指标选择记录，0表示无指标字典需要设置权重，1表示需要设置指标权值，需要解析metricTree

      // 权重矩阵
      metricWeight: {},

      //权重选项
      weightOptions: [
        {value: 9 / 1, label: '9/1'},
        {value: 8 / 1, label: '8/1'},
        {value: 7 / 1, label: '7/1'},
        {value: 6 / 1, label: '6/1'},
        {value: 5 / 1, label: '5/1'},
        {value: 4 / 1, label: '4/1'},
        {value: 3 / 1, label: '3/1'},
        {value: 2 / 1, label: '2/1'},
        {value: 1 / 1, label: '1/1'},
        {value: 1 / 2, label: '1/2'},
        {value: 1 / 3, label: '1/3'},
        {value: 1 / 4, label: '1/4'},
        {value: 1 / 5, label: '1/5'},
        {value: 1 / 6, label: '1/6'},
        {value: 1 / 7, label: '1/7'},
        {value: 1 / 8, label: '1/8'},
        {value: 1 / 9, label: '1/9'},
      ],

      // 权重中间表
      weightMatrix: [],

      // 三级已选择的树形结构数据
      selectedData: [],

      // 树形结构数据(用于展示,只记录前两级)
      treeData: [],
      treeProps: {
        children: 'children',
        label: 'label',
      },

      // 校验状态
      checkFlag: false,
      // 临时存储校验信息
      checkData: {
        "weightFlag":
            1,
        "data":
            {
              "levelOne":
                  ["指标1", "指标2"],
              "levelTwo":
                  ["指标1", "指标2"]
            }
      },
    };
  },
  methods: {
    // 加载层次分析法说明表格的颜色
    tableRowClassName({row}) {
      return {background: row.color};
    },

    //返回上一步
    back() {
      this.$router.push({name: 'index_select'});
    }
    ,

    filterNode(value, data) {
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
    }
    ,


    // 改变权重
    changeEvent(e, tableName, index1, index2) {
      // 校验状态置为false
      this.checkFlag = false;
      // weightData[tableName].data[scope.$index][index]
      let row = this.weightMatrix[index1]
      this.$set(this.weightMatrix, index1, row)
      this.weightMatrix[index2][index1] = 1 / e;
      this.metricWeight[tableName].data[index1][index2] = e; //更新总表的值
      this.metricWeight[tableName].data[index2][index1] = 1 / e; //更新总表的值

    }
    ,

    // 校验权重设置是否合理
    toCheck() {
      // 权重发给后端测试
      let project = this.$store.state.current_project.name;
      

      const _this = this
      // 将metricTree和metricWeight传给后端
      let obj = {
        "metricTree": this.metricTree,
        "metricWeight": this.metricWeight
      }

      // 发送请求
      utils.axiosMethod({
        method: "POST",
        url: window.ipConfig.baseUrl + "/weightCheck/" + _this.$store.state.current_project.name,
        data: {
          "metricWeight":_this.metricWeight
        },
        callback: (res) => {
          _this.checkData = JSON.parse(JSON.stringify(res.data));
          if (_this.checkData.weightFlag == 1) {
        // 校验状态置为true
        _this.checkFlag = true;
        _this.$notify({
          title: '成功',
          message: '校验通过，去提交',
          type: 'success'
        });
      } else {
        // 校验状态置为false
        _this.checkFlag = false;
        const h = _this.$createElement;
        _this.$notify({
          title: '提示',
          message: h('p', null, [
            h('span', null, '以下指标的权重设置不合理'),
            h('div', null, '软件总质量: ' + _this.checkData.data.levelZero),
            h('div', null, '一级指标: ' + _this.checkData.data.levelOne),
            h('div', null, '二级指标: ' + _this.checkData.data.levelTwo),
          ]),
          type: 'warning',
          duration: 6000,
        });

      }
        }
      })
      
    }
    ,

    // 提交权重设置
    toResult() {
      const _this = this
      // 先判断校验状态
      if (this.checkFlag == false) {
        this.$notify.error({
          title: '错误',
          message: '请先校验权重设置'
        });
        return;
      }
      this.$router.push({name: 'result_show'});

    }
    ,

    // 不用设置权重时，提交按钮
    toResultWithNoWeight() {
      // 跳转到result_show页面
      this.$router.push({name: 'result_show'});
    }
    ,

    // // 加载左侧树形控件
    loadTree(data) {
      //selectedData 用来存放三层所有已选择的信息;
      //遍历data,将树形数据保存到treeData中,只显示两层,且selected为true的,
      this.selectedData = [];
      // data为字典形式，key 存储各级指标
      // 遍历data字典
      for (const [key, value] of Object.entries(data)) {
        let obj = {};
        obj.id = key;
        obj.label = key;
        obj.children = [];
        for (const [key2, value2] of Object.entries(value)) {
          let obj2 = {};
          obj2.id = key2;
          obj2.label = key2;
          obj2.children = [];
          for (const [key3, value3] of Object.entries(value2)) {
            let obj3 = {};
            obj3.id = key3;
            obj3.label = key3;
            obj2.children.push(obj3);
          }
          obj.children.push(obj2);
        }
        this.selectedData.push(obj);
      }
      //只渲染前两层给treeData，
      this.treeData = this.selectedData.map(item => {
        return {
          id: item.id,
          label: item.label,
          children: item.children.map(item1 => {
            return {
              id: item1.id,
              label: item1.label,
              children: []
            }
          })
        }
      });
      // 给treedata外再加个总层
      this.treeData = [{
        id: 0,
        label: "软件总质量",
        children: this.treeData
      }]
    },

    // 加载已选节点传给后端
    load(data) {
      //selectedData 用来存放三层所有已选择的信息;
      //遍历data,将树形数据保存到treeData中,只显示两层,且selected为true的,
      this.metricTree = {}; // 要返回给后端的树形结构数据
      for (let i = 0; i < data.length; i++) {
        if (data[i].selected == false) {
          continue;
        }
        let obj = {};
        obj.id = data[i].id;
        obj.label = data[i].label;
        obj.selected = data[i].selected;
        obj.children = [];
        let mobj2 = {};
        for (let j = 0; j < data[i].children.length; j++) {
          if (data[i].children[j].selected == false) {
            continue;
          }

          let mobj3 = {};
          for (let k = 0; k < data[i].children[j].children.length; k++) {
            if (data[i].children[j].children[k].selected == false) {
              continue;
            }

            mobj3[data[i].children[j].children[k].label] = 0.0;

          }
          mobj2[data[i].children[j].label] = mobj3;

        }
        this.metricTree[data[i].label] = mobj2;

      }
    },

    //加载右侧weight初始化信息
    loadWeight(data) {
      this.metricWeight = {};
      // 给所有一级指标也设置权重，一级指标的老大写为软件总质量
      this.metricWeight["软件总质量"] = {
        index: [],
        data: []
      }
      // i 为 遍历的每个一级指标
      for (let i = 0; i < data.length; i++) {
        this.metricWeight["软件总质量"].index.push(data[i].label); // weightData[软件总质量] 的 index中 存入 每个一级指标的名字
        this.metricWeight["软件总质量"].data.push([]); // 为  软件总质量的data 初始化  一级指标的权重数组
        //给每个一级指标的权重数组 初始化 n 个 1/1
        for (let n1 = 0; n1 < data.length; n1++) {
          this.metricWeight["软件总质量"].data[i].push(1);
        }

        // 一级指标的权重初始化
        this.metricWeight[data[i].label] = {
          index: [],
          data: []
        }
        // j 为 遍历的每个二级指标
        for (let j = 0; j < data[i].children.length; j++) {
          this.metricWeight[data[i].label].index.push(data[i].children[j].label); //weightData[一级指标] 的 index中 存入 每个二级指标的名字
          this.metricWeight[data[i].label].data.push([]); //为  一级指标的data 初始化  二级指标的权重数组
          //给每个二级指标的权重数组 初始化 n 个 1/1
          for (let n2 = 0; n2 < data[i].children.length; n2++) {
            this.metricWeight[data[i].label].data[j].push(1);
          }
          // k 为 遍历的每个三级指标
          for (let k = 0; k < data[i].children[j].children.length; k++) {
            //二级指标也需要对其三级指标进行权重的初始化设置
            this.metricWeight[data[i].children[j].label] = {
              index: [],
              data: []
            }
            //
            for (let m = 0; m < data[i].children[j].children.length; m++) {
              this.metricWeight[data[i].children[j].label].index.push(data[i].children[j].children[m].label); //weightData[二级指标] 的 index中 存入 每个三级指标的名字
              this.metricWeight[data[i].children[j].label].data.push([]);// 为  二级指标的data 初始化  三级指标的权重数组
              //给每个三级指标的权重数组 初始化 n 个 1/1
              for (let n = 0; n < data[i].children[j].children.length; n++) {
                this.metricWeight[data[i].children[j].label].data[m].push(1);
              }
            }
          }
        }
      }

    },

    // 点击左侧树形控件节点时触发--主要作用:存储数据传给table信息中,用于右侧信息的渲染
    handleNodeClick(data) {
      this.tableData = [];
      this.tableDetial = [];
      this.tableName = data.label; //存储选择的指标名字
      // var id = data.id; //获取点击节点的id,第二位数表示第几个一级指标,第三位数表示第几个二级指标 // 更： 直接用指标名称来表示，没用
      //解析id 获取该元素的位置,并取出其子节点
      // let index1 = id.toString().charAt(1);//获取id的第二位数,一级指标的下标

      //根据metricWeight取出其index,作为表头，data作为表格数据
      this.tableData = this.metricWeight[data.label].index;
      // 遍历metricWeight中的data,将其作为表格数据
      for (let i = 0; i < this.metricWeight[data.label].data.length; i++) {
        let obj = {};
        obj.name = this.metricWeight[data.label].index[i]; //表格数据的第一列(name: 指标本身的名字,  eg. name: 功能完整性)
        obj.data = [];
        obj.id = i;
        for (let j = 0; j < this.metricWeight[data.label].data.length; j++) {
          obj.data[j] = this.metricWeight[data.label].data[i][j]; //表格数据的2-最后一列(要对比的指标的位置: 权重比 eg.  0: 1/1, 1: 1/3, 2: 3/1)
        }
        this.tableDetial.push(obj);
      }

      //权重中间二维矩阵设置
      this.weightMatrix = [];
      for (let i = 0; i < this.tableDetial.length; i++) {
        this.weightMatrix[i] = [];
        for (let j = 0; j < this.tableDetial.length; j++) {
          //中间矩阵初始化为weightData对应的值
          this.weightMatrix[i][j] = this.metricWeight[this.tableName].data[i][j];
        }
      }
    }

  },


  mounted() {
    
    this.load(this.$store.state.index_list);

    const _this = this

    // 如果树字典是空的,则提示用户先选择指标
    if (Object.keys(this.metricTree).length === 0) {
      this.$message({
        message: '请先选择指标',
        type: 'warning'
      });
      return;
    }

    // 给后端传树
    utils.axiosMethod({
      method: "POST",
      url: window.ipConfig.baseUrl + "/metricSelected/" + _this.$store.state.current_project.name,
      data: {
        "metricTree": _this.metricTree
      },
      callback: (res) => {
        // 接收后端传来的树
        utils.axiosMethod({
          method: "GET",
          url: window.ipConfig.baseUrl + "/metricWeight/" + _this.$store.state.current_project.name,
          callback: (res) => {
            _this.metricSelected = res.data.metricSelected;
            _this.metricTree = res.data.metricTree;
            
            // 如果不需要做选择
            if (res.data.metricSelected === 0) {
              _this.load(_this.$store.state.index_list);
              return;
            }

            // 加载树
            _this.loadTree(res.data.metricTree)

            _this.loadWeight(_this.selectedData);

            // 进入页面时,树默认点击第一个一级指标
            _this.$nextTick(() => {
            //this.$refs.tree.setCurrentKey(this.fileTreeData[0].children[0].children[0].id);
            // 点击该节点
            document.querySelector('.el-tree-node__content').click()
            })
            

          }
        })
      }
    })
  }
}


</script>

<style scoped>
.grid-content {
  border: 1px solid #dcdfe6;
  /*自适应高度*/
  height: 100%;
}

/*自定义树节点样式*/
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.back:hover {
  color: #409eff;
}
</style>