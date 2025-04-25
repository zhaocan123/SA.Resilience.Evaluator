var graph = {
    "data": [
        {
            "name": "handler",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:52:handler",
            "file": "exec.c:52",
            "category": 0,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 0
        },
        {
            "name": "close_fds",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:59:close_fds",
            "file": "exec.c:59",
            "category": 1,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 1
        },
        {
            "name": "exec_setup",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:91:exec_setup",
            "file": "exec.c:91",
            "category": 1,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 1,
            "inDegree": 1
        },
        {
            "name": "exec_cmnd",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:261:exec_cmnd",
            "file": "exec.c:261",
            "category": 0,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 1,
            "inDegree": 1
        },
        {
            "name": "sudo_terminated",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:315:sudo_terminated",
            "file": "exec.c:315",
            "category": 0,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 1
        },
        {
            "name": "sudo_needs_pty",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:363:sudo_needs_pty",
            "file": "exec.c:363",
            "category": 0,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 1
        },
        {
            "name": "fd_matches_tty",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:385:fd_matches_tty",
            "file": "exec.c:385",
            "category": 2,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 0
        },
        {
            "name": "direct_exec_allowed",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:407:direct_exec_allowed",
            "file": "exec.c:407",
            "category": 3,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 1
        },
        {
            "name": "sudo_execute",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
            "file": "exec.c:432",
            "category": 2,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 4,
            "inDegree": 0
        },
        {
            "name": "terminate_command",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:523:terminate_command",
            "file": "exec.c:523",
            "category": 0,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 0
        },
        {
            "name": "free_exec_closure",
            "id": "/temp_grad/upload/sudo/code/src/exec.c:559:free_exec_closure",
            "file": "exec.c:559",
            "category": 0,
            "symbolSize": 45,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            },
            "outDegree": 0,
            "inDegree": 0
        }
    ],
    "links": [
        {
            "source": "/temp_grad/upload/sudo/code/src/exec.c:91:exec_setup",
            "target": "/temp_grad/upload/sudo/code/src/exec.c:59:close_fds",
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
            "source": "/temp_grad/upload/sudo/code/src/exec.c:261:exec_cmnd",
            "target": "/temp_grad/upload/sudo/code/src/exec.c:91:exec_setup",
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
            "source": "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
            "target": "/temp_grad/upload/sudo/code/src/exec.c:363:sudo_needs_pty",
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
            "source": "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
            "target": "/temp_grad/upload/sudo/code/src/exec.c:407:direct_exec_allowed",
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
            "source": "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
            "target": "/temp_grad/upload/sudo/code/src/exec.c:315:sudo_terminated",
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
            "source": "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
            "target": "/temp_grad/upload/sudo/code/src/exec.c:261:exec_cmnd",
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
    ],
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
        },
        
    ],
    "maxOutFunc": "exec.c:432:sudo_execute()(4)",
    "minOutFunc": "exec.c:52:handler()(0)",
    "avgOut": 0.5454545454545454,
    "maxInFunc": "exec.c:59:close_fds()(1)",
    "minInFunc": "exec.c:52:handler()(0)",
    "avgIn": 0.5454545454545454,
    "maxCallPath": [
        "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
        "/temp_grad/upload/sudo/code/src/exec.c:261:exec_cmnd",
        "/temp_grad/upload/sudo/code/src/exec.c:91:exec_setup",
        "/temp_grad/upload/sudo/code/src/exec.c:59:close_fds"
    ],
    "minCallPath": [
        "/temp_grad/upload/sudo/code/src/exec.c:432:sudo_execute",
        "/temp_grad/upload/sudo/code/src/exec.c:315:sudo_terminated"
    ],
    "avgCallPath": 2.5
}