var graph = {
    "data": [
        {
            "name": "main",
            "id": "main",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -184,
            "y": -234,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "game",
            "id": "game",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -148,
            "y": -162,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "InitBoard",
            "id": "InitBoard",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -35,
            "y": -90,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "SetMine",
            "id": "SetMine",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -119,
            "y": -90,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "DisplayBoard",
            "id": "DisplayBoard",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -178,
            "y": -18,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "FindMine",
            "id": "FindMine",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -241,
            "y": -90,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "GetMineCount",
            "id": "GetMineCount",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -292,
            "y": -18,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        },
        {
            "name": "menu",
            "id": "menu",
            "symbolSize": [
                73.31378299120234,
                58.651026392961874
            ],
            "x": -220,
            "y": -162,
            "category": 0,
            "fixed": false,
            "symbol": "rect",
            "itemStyle": {
                "normal": {
                    "color": "lightblue"
                }
            },
            "label_opts": {}
        }
    ],
    "links": [
        {
            "source": "main",
            "target": "game",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "main",
            "target": "menu",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "game",
            "target": "InitBoard",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "game",
            "target": "SetMine",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "game",
            "target": "DisplayBoard",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "game",
            "target": "FindMine",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "FindMine",
            "target": "DisplayBoard",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        },
        {
            "source": "FindMine",
            "target": "GetMineCount",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "curveness": -0.1,
                    "type": "solid",
                    "color": "green"
                }
            },
            "labelLayout": {
                "hideOverlap": true
            }
        }
    ]
}