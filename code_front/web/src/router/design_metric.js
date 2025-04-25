import Index1 from "@/components/Index1.vue"
import Index2 from "@/components/Index2.vue"
import defect_rate_calculation from "@/views/design_metric/defect_rate_calculation.vue"
import bad_ratio_detect from "@/views/design_metric/bad_ratio_detect.vue"

import evaluate_result_show from "@/views/design_metric/quality_evaluation/software/result_show.vue"
import evaluate_weight_set from "@/views/design_metric/quality_evaluation/software/weight_set.vue"
import evaluate_index_select from "@/views/design_metric/quality_evaluation/software/index_select.vue"
import evaluate_expert_index from "@/views/design_metric/quality_evaluation/design/expert_index.vue"
import evaluate_result_show1 from "@/views/design_metric/quality_evaluation/design/result_show.vue"
import call_graph_build from "@/views/info_extraction_visualization/call_graph_build.vue"
import basic_info from "@/views/attack_surface/basic_info.vue"
import attack_graph from "@/views/attack_surface/attack_graph.vue"

export default {
    path: "system_attack_info",
    name: "system_attack_info",
    hidden: false,
    meta: {
        title: "系统攻击面信息",
        params: {}
    },
    component: Index1,
    children: [
        {
            path: "basic_info",
            name: "basic_info",
            hidden: false,
            meta: {
                title: "攻击面基本信息",
            },
            component: basic_info
        },
        // {
        //     path: "defect_rate_calculation",
        //     name: "defect_rate_calculation",
        //     hidden: false,
        //     meta: {
        //         title: "缺陷率计算",
        //     },
        //     component: defect_rate_calculation
        // },
        // {
        //     path: "bad_ratio_detect",
        //     name: "bad_ratio_detect",
        //     hidden: false,
        //     meta: {
        //         title: "不可信数据元素/数据通道",
        //     },
        //     component: bad_ratio_detect
        // },
        {
            path: "attack_graph",
            name: "attack_graph",
            hidden: false,
            meta: {
                title: "攻击面可视化",
            },
            component: attack_graph
        },
        // {
        //     path: "bad_ratio_detect",
        //     name: "bad_ratio_detect",
        //     hidden: false,
        //     meta: {
        //         title: "坏味率计算",
        //     },
        //     component: bad_ratio_detect
        // },
        // {
        //     path: "metric_index_calculation",
        //     name: "metric_index_calculation",
        //     hidden: false,
        //     meta: {
        //         title: "度量指标计算",
        //     },
        //     component: metric_index_calculation
        // },
        // {
        //     path: "design_quality_metric",
        //     name: "design_quality_metric",
        //     hidden: false,
        //     meta: {
        //         title: "设计质量度量",
        //     },
        //     component: design_quality_metric
        // },
        // {
        //     path: "result_show",
        //     name: "result_show",
        //     hidden: true,
        //     meta: {
        //         title: "结果展示",
        //     },
        //     component: result_show
        // },
        // {
        //     path: "software",
        //     name: "software",
        //     hidden: false,
        //     meta: {
        //     title: "软件质量评估",
        //     params: {}
        //     },
        //     component: Index2,
        //     children: [
        //     {
        //         path: "index_select",
        //         name: "index_select",
        //         hidden: false,
        //         meta: {
        //         title: "指标选择",
        //         params: {}
        //         },
        //         component: evaluate_index_select
        //     },
        //     {
        //         path: "weight_set",
        //         name: "weight_set",
        //         hidden: false,
        //         meta: {
        //         title: "权重设置",
        //         params: {}
        //         },
        //         component: evaluate_weight_set
        //     },
        //     {
        //         path: "result_show",
        //         name: "result_show",
        //         hidden: false,
        //         meta: {
        //         title: "结果展示",
        //         params: {}
        //         },
        //         component: evaluate_result_show
        //     },
        //     ]
        // },
        // {
        //     path: "design",
        //     name: "design",
        //     hidden: false,
        //     meta: {
        //     title: "设计质量评估",
        //     params: {}
        //     },
        //     component: Index2,
        //     children: [
        //     {
        //         path: "index_select1",
        //         name: "index_select1",
        //         hidden: false,
        //         meta: {
        //         title: "评估指标",
        //         params: {}
        //         },
        //         component: evaluate_expert_index
        //     },
        //     {
        //         path: "result_show1",
        //         name: "result_show1",
        //         hidden: false,
        //         meta: {
        //         title: "结果展示",
        //         params: {}
        //         },
        //         component: evaluate_result_show1
        //     },
        //     ]
        // }
    ]
}