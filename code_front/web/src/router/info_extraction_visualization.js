import Index1 from "@/components/Index1.vue"
import Index2 from "@/components/Index2.vue"
import project_info from "@/views/info_extraction_visualization/project_info.vue"
import code_info from "@/views/info_extraction_visualization/code_info.vue"
import call_graph_build from "@/views/info_extraction_visualization/call_graph_build.vue"
import wsd_graph_build from "@/views/info_extraction_visualization/wsd_graph_build.vue"


import CFGView from "@/views/info_extraction_visualization/CFGView.vue"
import PDGView from "@/views/info_extraction_visualization/PDGView.vue"
import SDGView from "@/views/info_extraction_visualization/SDGView.vue"

import ArchitectureDependencyGraph from "@/views/info_extraction_visualization/ArchitectureDependencyGraph.vue"
import PipeFilterArchitectureGraph from "@/views/info_extraction_visualization/PipeFilterArchitectureGraph.vue"
import CallReturnStyleArchitectureGraph from "@/views/info_extraction_visualization/CallReturnStyleArchitectureGraph.vue"
import HierarchicalStyleArchitectureGraph from "@/views/info_extraction_visualization/HierarchicalStyleArchitectureGraph.vue"

import ClassView from "@/views/info_extraction_visualization/ClassView.vue"

export default {
    path: "info_extraction_visualization",
    name: "info_extraction_visualization",
    hidden: false,
    meta: {
        title: "项目信息和架构视图",
        // title: "信息提取及可视化",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "project_info",
            name: "project_info",
            hidden: false,
            meta: {
                title: "项目信息",
                // title: "项目信息提取",
                params: {}
            },
            component: project_info
        },
        // {
        //     path: "code_info",
        //     name: "code_info",
        //     hidden: false,
        //     meta: {
        //         title: "代码解析及信息提取",
        //         params: {}
        //     },
        //     component: code_info
        // },
        {
            path: "design_recovery",
            name: "design_recovery",
            hidden: false,
            meta: {
                title: "架构视图",
                // title: "设计恢复",
                params: {}
            },
            component: Index2,
            children: [
                // {
                //     path: "CFGView",
                //     name: "CFGView",
                //     hidden: false,
                //     meta: {
                //         title: "控制流图",
                //         params: {
                //             title: "CFGView",
                //         }
                //     },
                //     component: CFGView
                // },
                // {
                //     path: "PDGView",
                //     name: "PDGView",
                //     hidden: false,
                //     meta: {
                //         title: "过程依赖图",
                //         params: {
                //             title: "PDGView",
                //         }
                //     },
                //     component: PDGView
                // },
                // {
                //     path: "call_graph_build",
                //     name: "call_graph_build",
                //     hidden: false,
                //     meta: {
                //         title: "调用图",
                //         params: {}
                //     },
                //     component: call_graph_build
                // },
                {
                    path: "wsd_graph_build", // wsd_graph_build
                    name: "wsd_graph_build",
                    hidden: false,
                    meta: {
                        title: "UML架构视图",
                        params: {}
                    },
                    component: wsd_graph_build

                },
                {
                    path: "call_graph_build", // wsd_graph_build
                    name: "call_graph_build",
                    hidden: false,
                    meta: {
                        title: "调用图DEBUG",
                        params: {}
                    },
                    component: call_graph_build

                },
                {
                    path: "SDGView",
                    name: "SDGView",
                    hidden: false,
                    meta: {
                        title: "系统架构依赖图",
                        params: {
                            title: "SDGView",
                        }
                    },
                    component: SDGView,
                },
                {
                    path: "ArchitectureDependencyGraph",
                    name: "ArchitectureDependencyGraph",
                    hidden: false,
                    meta: {
                        title: "DEBUG",
                        params: {
                            title: "架构依赖图",
                        }
                    },
                    component: ArchitectureDependencyGraph,
                },
                {
                    path: "PipeFilterArchitectureGraph",
                    name: "PipeFilterArchitectureGraph",
                    hidden: false,
                    meta: {
                        title: "管道过滤器风格架构图",
                        params: {
                            title: "管道过滤器风格架构图",
                        }
                    },
                    component: PipeFilterArchitectureGraph,
                }
                    // },
                // {
                //     path: "CallReturnStyleArchitectureGraph",
                //     name: "CallReturnStyleArchitectureGraph",
                //     hidden: false,
                //     meta: {
                //         title: "调用返回风格架构图",
                //         params: {
                //             title: "调用返回风格架构图",
                //         }
                //     },
                //     component: CallReturnStyleArchitectureGraph,
                // },
                // {
                //     path: "HierarchicalStyleArchitectureGraph",
                //     name: "HierarchicalStyleArchitectureGraph",
                //     hidden: false,
                //     meta: {
                //         title: "分层风格架构图",
                //         params: {
                //             title: "分层风格架构图",
                //         }
                //     },
                //     component: HierarchicalStyleArchitectureGraph,
                // },
                // {
                //     path: "ClassView",
                //     name: "ClassView",
                //     hidden: false,
                //     meta: {
                //         title: "类图",
                //         params: {
                //             title: "类图",
                //         }
                //     },
                //     component: ClassView,
                // }
            ]
        },
    ]
}