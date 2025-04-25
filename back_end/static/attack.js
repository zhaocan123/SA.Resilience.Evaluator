var graph = {
    "categories": [
        {
            "name": "Normal Node"
        },
        {
            "name": "Entry Node"
        },
        {
            "name": "Exit Node"
        },
        {
            "name": "Potential Attack"
        }
    ],
    "data": [
        {
            "name": "write_file()",
            "id": "Func:stdio.h:655:fputs::main.c:3:write_file",
            "file": "main.c:3",
            "category": 2,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "fprintf()",
            "id": "Func:stdio.h:350:fprintf",
            "file": "stdio.h:350",
            "category": 2,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "fputs()",
            "id": "Func:stdio.h:655:fputs",
            "file": "stdio.h:655",
            "category": 2,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "fclose()",
            "id": "Func:stdio.h:178:fclose",
            "file": "stdio.h:178",
            "category": 0,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "fopen()",
            "id": "Func:stdio.h:258:fopen",
            "file": "stdio.h:258",
            "category": 0,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "write_to_cmd()",
            "id": "Func:stdio.h:356:printf::main.c:12:write_to_cmd",
            "file": "main.c:12",
            "category": 2,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "printf()",
            "id": "Func:stdio.h:356:printf",
            "file": "stdio.h:356",
            "category": 2,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "read_from_cmd()",
            "id": "Func:stdio.h:437:scanf::main.c:16:read_from_cmd",
            "file": "main.c:16",
            "category": 1,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "scanf()",
            "id": "Func:stdio.h:437:scanf",
            "file": "stdio.h:437",
            "category": 1,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "main()",
            "id": "Func:main.c:21:main",
            "file": "main.c:21",
            "category": 1,
            "symbolSize": 45,
            "node_resilience": 0.2,
            "reliability": 0.2,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "ContentSpoofing",
            "id": "Attack:ContentSpoofing",
            "file": "activity uml",
            "category": 3,
            "symbolSize": 45,
            "fixed": false,
            "attack_nums": 6,
            "attack_prob": 0.8,
            "attack_severity": "high",
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "IdentitySpoofing",
            "id": "Attack:IdentitySpoofing",
            "file": "activity uml",
            "category": 3,
            "symbolSize": 45,
            "fixed": false,
            "attack_nums": 1,
            "attack_prob": 0.8,
            "attack_severity": "high",
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Excavation",
            "id": "Attack:Excavation",
            "file": "activity uml",
            "category": 3,
            "symbolSize": 45,
            "fixed": false,
            "attack_nums": 1,
            "attack_prob": 0.5,
            "attack_severity": "medium",
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        }
    ],
    "links": [
        {
            "source": "Attack:ContentSpoofing",
            "target": "Func:stdio.h:437:scanf",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:IdentitySpoofing",
            "target": "Func:stdio.h:437:scanf::main.c:16:read_from_cmd",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:IdentitySpoofing",
            "target": "Func:main.c:21:main",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:IdentitySpoofing",
            "target": "Func:stdio.h:350:fprintf",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:IdentitySpoofing",
            "target": "Func:stdio.h:655:fputs",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:IdentitySpoofing",
            "target": "Func:stdio.h:356:printf",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:Excavation",
            "target": "Func:stdio.h:356:printf::main.c:12:write_to_cmd",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack:Excavation",
            "target": "Func:main.c:21:main",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:stdio.h:655:fputs::main.c:3:write_file",
            "target": "Func:stdio.h:350:fprintf",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:stdio.h:655:fputs::main.c:3:write_file",
            "target": "Func:stdio.h:655:fputs",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:stdio.h:655:fputs::main.c:3:write_file",
            "target": "Func:stdio.h:178:fclose",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:stdio.h:655:fputs::main.c:3:write_file",
            "target": "Func:stdio.h:258:fopen",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:stdio.h:356:printf::main.c:12:write_to_cmd",
            "target": "Func:stdio.h:356:printf",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:stdio.h:437:scanf::main.c:16:read_from_cmd",
            "target": "Func:stdio.h:437:scanf",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:main.c:21:main",
            "target": "Func:stdio.h:655:fputs::main.c:3:write_file",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:main.c:21:main",
            "target": "Func:stdio.h:437:scanf::main.c:16:read_from_cmd",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Func:main.c:21:main",
            "target": "Func:stdio.h:356:printf::main.c:12:write_to_cmd",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.1,
                    "type": "solid",
                    "opacity": 1
                }
            }
        }
    ]
}