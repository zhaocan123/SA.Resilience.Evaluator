import Index1 from "@/components/Index1.vue"

import xuqiu from "@/views/file_information/xuqiu.vue"

// 质量评估菜单
export default {
    path: "xuqiu",
    name: "xuqiu",
    hidden: false,
    meta: {
        title: "文档信息",
        params: {}
    },
    component: Index1,
    children: [
        {       
            path: "xuqiu",
            name: "xuqiu",
            hidden: false,
            meta: {
                title: "需求文档",
                params: {
                    title: "需求",
                    title1: "需求文档"
                }
            },
            component: xuqiu
        },
        {
            path: "sheji",
            name: "sheji",
            hidden: false,
            meta: {
            title: "设计文档",
            params: {
                title: "设计",
                title1: "设计文档"
            }
            },
            component: xuqiu
        },
        {
            path: "ceshi",
            name: "ceshi",
            hidden: false,
            meta: {
            title: "测试文档",
            params: {
                title: "测试",
                title1: "测试文档"
            }
            },
            component: xuqiu
        },
        {
            path: "weihu",
            name: "weihu",
            hidden: false,
            meta: {
            title: "维护文档",
            params: {
                title: "维护",
                title1: "维护文档"
            }
            },
            component: xuqiu
        },
        {
            path: "manual",
            name: "manual",
            hidden: false,
            meta: {
            title: "用户手册",
            params: {
                title: "手册",
                title1: "用户手册"

            }
            },
            component: xuqiu
        }
    ]
}