<template>
    <div>
        <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        text-color="black"
        active-text-color="blue"
        router
        >
            <template v-for="item in routerData">
                <el-menu-item v-if="!item.hidden && !item.children" :index="item.path" :key="item.path" @click="toView(item)" :disabled="menuDisabled"> 
                    {{item.meta.title}}
                </el-menu-item>
                <el-submenu v-if="!item.hidden && item.children" :index="item.path" :key="item.path" :disabled="menuDisabled">
                    <template slot="title">{{ item.meta.title }}</template>
                    <template v-for="its in item.children">
                        <el-menu-item v-if="!its.hidden && !its.children" :index="its.path" :key="its.path" @click="toView(its)"> 
                            <span slot="title">{{ its.meta.title }}</span>
                        </el-menu-item>
                        <el-submenu v-if="!its.hidden && its.children" :index="its.path" :key="its.path">
                            <template slot="title">{{ its.meta.title }}</template>
                            <template v-for="its1 in its.children">
                                <el-menu-item v-if="(!its1.hidden && !its1.children) && 
                                !((cDisabledList.indexOf(its1.name) != -1 && $store.state.current_project.projectType != 0) || 
                                (cPlusDisabledList.indexOf(its1.name) != -1 && $store.state.current_project.projectType == 0))" 
                                :index="its1.path" :key="its1.path" @click="toView(its1)"> 
                                    <span slot="title">{{ its1.meta.title }}</span>
                                </el-menu-item>
                            </template>
                        </el-submenu>
                    </template>
                </el-submenu>
            </template>
        </el-menu>
    </div>
</template>

<script>
    import {router_list} from "@/router"

    export default {
        name: "MenuBar",
        data() {
            return {
                cDisabledList: [
                    "SDGView",
                    "ArchitectureDependencyGraph",
                    "PipeFilterArchitectureGraph",
                    "CallReturnStyleArchitectureGraph",
                    "HierarchicalStyleArchitectureGraph"
                ],
                cPlusDisabledList: [
                    "ClassView"
                ],
                activeIndex: "",
                routerData: [],
            }
        },
        computed: {
            menuDisabled:{
                get() {
                    return this.$store.state.menuDisabled;
                },
                set(newValue) {
                    return newValue;
                },
            }
        },
        created(){
            this.getRouter()
        },
        methods: {
            getRouter(){
                this.routerData = router_list;
            },
            handleSelect(index, indexPath) {
                // console.log("index", index);
                // console.log("indexPath", indexPath);

            },
            toView(item){
                this.$router.push({
                    name: item.name,
                    // 传参给页面
                    params: item.params
                });
                this.activeIndex = item.path;
            },
        }
    }
</script>

<style scoped>

</style>
