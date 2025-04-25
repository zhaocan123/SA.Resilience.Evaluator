<template>
    <el-breadcrumb id ="nav-top" separator-class="el-icon-arrow-right" class="nav-top">
        <el-breadcrumb-item v-if="!isCreate" :to="{name: 'home'}">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-for="(navi, index) in naviList" :key="index"
            :to="{path: navi.path}">{{ navi.meta.title }}</el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script>
export default {
    name: "NaviBar",
    data(){
        return{
            naviList: [],
            isCreate: false
        }
    },
    mounted(){
        if(this.$route.matched[0].meta.title === "选择文档"){
            let dom = document.getElementById("nav-top")
            dom.style.display = "none"
        }
        // 监听浏览器刷新并缓存数据
        const _this = this
        window.addEventListener("beforeunload", (e) => {
            let naviList = _this.naviList
            _this.$store.commit("setNaviList", naviList)
        })
        // 刷新后加载缓存中的数据
        window.addEventListener("load", (e) => {
            _this.naviList = _this.$store.state.naviList
        })
    },
    watch:{
        $route(to, from) {
            let current_project = this.$store.state.current_project
            let matched = to.matched

            const matched_list = ["create", "selectDoc", "selectDoc2"]
            this.isCreate = matched_list.indexOf(matched[0].name) != -1 ? true : false

            if(matched[0].meta.title == "首页"){
                this.naviList = []
            }
            else if(matched[0].name == "main") {
                matched[0].meta.title = current_project.name
                this.naviList = []
                for(let item of matched) {
                    this.naviList.push({
                        name: item.name,
                        path: item.path,
                        meta: item.meta
                    })   
                }
            }
            else {
                this.naviList = []
                for(let item of matched) {
                    this.naviList.push({
                        name: item.name,
                        path: item.path,
                        meta: item.meta
                    })   
                }
            }
        }
    }
}
</script>

<style>

</style>