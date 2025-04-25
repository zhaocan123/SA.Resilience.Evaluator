<template>
    <div>
        <div class="container">
            <div class="tree">
                <div>项目名: {{ latestVersion }}</div>
                <el-tree 
                ref="menuTree"
                :data="latestFileTree"
                :props="fileTreeProps"
                default-expand-all
                highlight-current
                node-key="id"
                :expand-on-click-node="false"
                @node-click="handleNodeClick"
                :indent="50"
                class="el-tree">
                    <template slot-scope="{ node }">
                        <el-popover v-if="node.isLeaf"
                            placement="right"
                            title="文件信息"
                            width="200"
                            trigger="hover">
                            <span slot="reference" class="tree-node" :style="getStyle(node.data)">{{ node.label }}</span>
                            <div>
                                <div>函数数量: {{ node.data.fileInfo.funcNum }}</div>
                                <div>全局变量数: {{ node.data.fileInfo.globalVariableNum }}</div>
                                <div>文件大小: {{ node.data.fileInfo.fileSize }}</div>
                                <div>出度: {{ node.data.fileInfo.outDegree }}</div>
                                <div>入度: {{ node.data.fileInfo.inDegree }}</div>
                                <div>注释行数: {{ node.data.fileInfo.annotationLine }}</div>
                            </div>
                        </el-popover>
                        <span v-else class="tree-node" :style="getStyle(node.data)">{{ node.label }}</span>
                    </template>
                </el-tree>
            </div>
            <div class="tree">
                <div>项目名: {{ selectedVersion }}</div>
                <el-tree 
                ref="menuTree"
                :data="selectedFileTree"
                :props="fileTreeProps"
                default-expand-all
                highlight-current
                node-key="id"
                :expand-on-click-node="false"
                @node-click="handleNodeClick"
                :indent="50"
                class="el-tree">
                    <template slot-scope="{ node }">
                        <el-popover v-if="node.isLeaf"
                            placement="right"
                            title="文件信息"
                            width="200"
                            trigger="click">
                            <span slot="reference" class="tree-node" :style="getStyle(node.data)">{{ node.label }}</span>
                            <div>
                                <div>函数数量: {{ node.data.fileInfo.funcNum }}</div>
                                <div>全局变量数: {{ node.data.fileInfo.globalVariableNum }}</div>
                                <div>文件大小: {{ node.data.fileInfo.fileSize }}</div>
                                <div>出度: {{ node.data.fileInfo.outDegree }}</div>
                                <div>入度: {{ node.data.fileInfo.inDegree }}</div>
                                <div>注释行数: {{ node.data.fileInfo.annotationLine }}</div>
                            </div>
                        </el-popover>
                        <span v-else class="tree-node" :style="getStyle(node.data)">{{ node.label }}</span>
                    </template>
                </el-tree>
            </div>
        </div>
        <div style="margin-top: 1vh;">
            说明: <span style="color: red;">红色</span>为删除文件，<span style="color: green;">绿色</span>为新增文件，<span style="color: blue;">蓝色</span>为修改文件，<span style="font-weight: bold;">黑色</span>为无修改文件
        </div>
    </div>
</template>

<script>
import Cache from "@/utils/cache"
export default {
    props: ["typeName"],
    watch: {
        typeName(newVal) {
            this.typeName = newVal
            this.getData()
        }
    },
    data(){
        return {
            selectedFileTree: [],
            latestFileTree: [],
            fileTreeProps: {
                label: 'label',
                children: 'children'
            },
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
            selectedVersion: null,
            latestVersion: null,
        }
    },
    mounted(){
        this.getData()
    },
    methods:{
        getData(){
            let data = Cache.getCache("change_information_detection_data")
            this.selectedVersion = data[this.typeName].systemLevel.versionSelected.name
            this.latestVersion = data[this.typeName].systemLevel.versionLatest.name
            this.selectedFileTree = data[this.typeName].fileLevel.selectedFileTree
            this.latestFileTree = data[this.typeName].fileLevel.latestFileTree
            // console.log(this.selectedFileTree);
        },
        getStyle(node){
            let style = {
                "color": "black"
            }
            if(node.type == "file" && node.status == 1){
                style.color = "red"
            }
            else if(node.type == "file" && node.status == 2){
                style.color = "green"
            }
            else if(node.type == "file" && node.status == 3){
                style.color = "blue"
            }
            return style
        },
        handleNodeClick(e){
            this.selectedNode = e
            // console.log("selectedNode", this.selectedNode)
            this.isLeaf = e.isLeaf
        }
    }
}
</script>

<style scoped>
.container{
    height: 72vh;
    width: 100%;
    display: flex;
}
.tree{
    height: 100%;
    width: 50%;
    overflow: auto;
    padding-left: 5%;
}
.el-tree{
    width: 100%;
    margin-top: 2%;
}
.tree-node {
    margin-left: 1%;
}
</style>
