import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

import Home from "@/components/Home.vue";
// import New from "@/components/New.vue";
import Create from "@/components/Create.vue";
import Main from "@/components/Main.vue"
import SelectDoc from "@/components/selectDoc.vue";
import change_information_detection from "@/views/change_information_detection/change_information_detection.vue"
import design_refactor_suggestion from "@/views/design_refactor_suggestion/design_refactor_suggestion.vue"
import info_extraction_visualization from "./info_extraction_visualization"
import design_metric from "./design_metric"
import user_manual from "@/views/user_manual/user_manual.vue"
import SelectDoc2 from "@/components/selectDoc2.vue";

import pdf_change_infonation_detection from "@/views/pdf_template/pdf_change_infonation_detection.vue"
import pdf_bad_ratio_calculation from "@/views/pdf_template/pdf_bad_ratio_calculation.vue"
import pdf_design_refactor_suggestion from "@/views/pdf_template/pdf_design_refactor_suggestion.vue"
import pdf_software_eval from "@/views/pdf_template/pdf_software_eval.vue"
import pdf_design_eval from "@/views/pdf_template/pdf_design_eval.vue"
import pdf_project_info from "@/views/pdf_template/pdf_project_info.vue"

import basic_info from "@/views/attack_surface/basic_info.vue"
import resilience_result from "@/views/resilience_report/resilience_result.vue"
import StatisticInfo from "@/views/design_metric//result/statistic_information.vue";
// 配置功能页路由，会同步到菜单栏
export const router_list = [
  info_extraction_visualization,
  design_metric,
  {
    path: "resilience_result",   // 路径
    name: "resilience_result",   // 名字
    hidden: false,             // 是否显示在菜单栏
    meta: {
      title: "查看韧性评估报告",       // 菜单栏标题
      // title: "变更信息检测",       // 菜单栏标题
    },
    component: resilience_result // resilience_report // 对应的vue页面
  },
  {
    path: "design_refactor_suggestion",   // 路径
    name: "design_refactor_suggestion",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "设计重构建议",       // 菜单栏标题
    },
    component: design_refactor_suggestion // 对应的vue页面
  },
  {
    path: "pdf_change_infonation_detection",   // 路径
    name: "pdf_change_infonation_detection",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "变更信息检测pdf",       // 菜单栏标题
    },
    component: pdf_change_infonation_detection // 对应的vue页面
  },
  {
    path: "pdf_bad_ratio_calculation",   // 路径
    name: "pdf_bad_ratio_calculation",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "坏味率计算pdf",       // 菜单栏标题
    },
    component: pdf_bad_ratio_calculation // 对应的vue页面
  },
  {
    path: "pdf_design_refactor_suggestion",   // 路径
    name: "pdf_design_refactor_suggestion",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "设计重构建议pdf",       // 菜单栏标题
    },
    component: pdf_design_refactor_suggestion // 对应的vue页面
  },
  {
    path: "pdf_software_eval",   // 路径
    name: "pdf_software_eval",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "软件质量评估pdf",       // 菜单栏标题
    },
    component: pdf_software_eval // 对应的vue页面
  },
  {
    path: "pdf_design_eval",   // 路径
    name: "pdf_design_eval",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "设计质量评估pdf",       // 菜单栏标题
    },
    component: pdf_design_eval // 对应的vue页面
  },
  {
    path: "pdf_project_info",   // 路径
    name: "pdf_project_info",   // 名字
    hidden: true,             // 是否显示在菜单栏
    meta: {
      title: "项目信息pdf",       // 菜单栏标题
    },
    component: pdf_project_info // 对应的vue页面
  },
]

export const router = new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      hidden: true,

      meta: {
        title: "首页",
        noCache: true // 标识不需要缓存
      },
      component:Home
    },
    {
      path: '/user_manual',
      name: 'user_manual',
      hidden: true,
      meta: {
        title: "用户手册"
      },
      component: user_manual
    },
    // {
    //   path: '/new',
    //   name: 'new',
    //   hidden: true,
    //   meta: {
    //     title: "新建",
    //     keepAlive:true
    //   },
    //   component: New
    // },
    {
      path: '/create',
      name: 'create',
      hidden: true,
      meta: {
        title: "新建",
        keepAlive:true
      },
      component: Create
    },
    {
      path: '/selectDoc',
      name: 'selectDoc',
      hidden: true,
      meta: {
        title: "选择文档"
      },
      component: SelectDoc
    },
    {
      path: '/selectDoc2',
      name: 'selectDoc2',
      hidden: true,
      meta: {
        title: "选择文档"
      },
      component: SelectDoc2
    },
    {
      path: '/main',
      name: 'main',
      hidden: true,
      meta: {
        title: "项目"
      },
      component: Main,
      redirect: {
        name: "project_info"
      },
      children: router_list
    },
    {
      path: '*',
      hidden: true,
      redirect: '/home'
    }
  ]
})
