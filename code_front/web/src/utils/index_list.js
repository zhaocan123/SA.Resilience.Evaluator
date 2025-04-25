export default {
  data: [{
    id: 11, // 第一个数字无意义, 第2个数字代表第一级的第几个, 第3个数字代表第二级的第几个, 以此类推
    label: '功能性',
    selected: false,
    des: "用于评估产品或系统在指定情况下使用时，提供满足明确和隐含要求的功能的程度。",
    val: 0.0,
    children: [
      {
        id: 111,
        label: '功能完备性',
        des: "用于评估功能集对所有指定的任务或用户目标的覆盖程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1111,
            label: '功能覆盖率',
            des: "所指定功能的实现比例多少？",
            type: 1,
            val: 0.0,
            equation: "`X=1-A/B`",
            factors: [
              "`A=缺少的功能数量`",
              "`B=指定的功能数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 112,
        label: '功能正确性',
        des: "用于评估产品或系统提供具有所需精度的正确结果的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1121,
            label: '功能正确性',
            des: "可提供正确结果的功能比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=1-A/B`",
            factors: [
              "`A=功能不正确的数量`",
              "`B=考虑的功能数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 113,
        label: '功能适合性',
        des: "用于评估功能促使指定的任务和目标实现的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1131,
            label: '使用目标的功能适合性',
            des: "用户要求的功能中提供了合适结果以实现特定使用目标的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=1-A/B`",
            factors: [
              "`A=为实现特定使用目标所需的功能中缺少或不正确功能的数量`",
              "`B=为实现特定使用目标所需的功能数量`"
            ],
            selected: false
          },
          {
            id: 1132,
            label: '系统的功能适合性',
            des: "用户要求达到的目标功能中，能给出合适结果的功能比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{A_i}{n}`",
            factors: [
              "`A_i=使用目标i的适合性得分，即第i个特定使用目标“使用目标的功能适合性”的测量值`",
              "`n=使用目标的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 114,
        label: '功能性的依从性',
        des: "用于评估产品或系统遵循与功能性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1141,
            label: '功能性的依从性',
            des: "遵循与产品或系统的功能性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与功能性的依从性相关的项数`",
              "`B=与功能性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },

    ],
  },
  {
    id: 12,
    label: '性能效率',
    des: "用于评估在指定条件下使用的资源数量的性能。",
    val: 0.0,
    selected: false,
    children: [
      {
        id: 121,
        label: '时间特性',
        des: "用于评估产品或系统执行其功能时,其响应时间、处理时间及吞吐率满足需求的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1211,
            label: '平均响应时间',
            des: "系统响应一个用户任务或系统任务的平均时间是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i)}{n}`",
            factors: [
              "`A_i=第i次测量时系统响应一个特定用户任务或系统任务花费的时间`",
              "`n=测得的响应次数`"
            ],
            selected: false
          },
          {
            id: 1212,
            label: '响应时间的充分性',
            des: "系统响应时间满足规定目标的程度如何？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=“平均响应时间”测度中所测量的平均响应时间`",
              "`n=规定的任务响应时间`"
            ],
            selected: false
          },
          {
            id: 1213,
            label: '平均周转时间',
            des: "完成一个作业或一个异步进程的平均时间是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(B_i-A_i)}{n}`",
            factors: [
              "`A_i=作业或异步进程i的开始时刻`",
              "`B_i=作业或异步进程i的完成时刻`",
              "`n=测量的次数`"
            ],
            selected: false
          },
          {
            id: 1214,
            label: '周转时间充分性',
            des: "周转时间满足规定目标的程度如何？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=“平均周转时间”测度中所测量的平均周转时间`",
              "`B=规定的作业或异步进程的周转时间`"
            ],
            selected: false
          },
          {
            id: 1215,
            label: '平均吞吐量',
            des: "单位时间内完成作业的平均数量是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i / B_i)}{n}`",
            factors: [
              "`A_i=第i次观察时间内完成的作业数量`",
              "`B_i=第i次观察时间的周期`",
              "`n=观察的次数`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 122,
        label: '资源利用性',
        des: "用于评估产品或系统执行其功能时,所使用资源数量和类型满足需求的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1221,
            label: '处理器平均占用率',
            des: "执行一组给定的任务，处理器所需要的时间与运行时间的平均比率是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i / B_i)}{n}`",
            factors: [
              "`A_i=第i次观察中，处理器执行一组给定任务所用的时间`",
              "`B_i=第i次观察中，执行任务的运行时间`",
              "`n=观察次数`"
            ],
            selected: false
          },
          {
            id: 1222,
            label: '内存平均占用率',
            des: "执行一组给定的任务所需要的内存与可用内存的平均比率是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i / B_i)}{n}`",
            factors: [
              "`A_i=第i次样本处理中执行一组给定任务所占用的实际内存大小`",
              "`B_i=第i次样本处理期间可用于执行任务的内存大小`",
              "`n=处理的样本数`"
            ],
            selected: false
          },
          {
            id: 1223,
            label: 'I/O设备平均占用率',
            des: "执行一组给定的任务所占用的I/O设备的时间与I/O操作时间的平均比率是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i / B_i)}{n}`",
            factors: [
              "`A_i=第i次观察中，执行一组给定任务所占用I//O设备的持续时间`",
              "`B_i=第i次观察中，执行任务所需I//O运行的持续时间`",
              "`n=观察次数`"
            ],
            selected: false
          },
          {
            id: 1224,
            label: '带宽占用率',
            des: "执行一组给定任务时使用可用带宽的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=执行一组给定任务时测得的实际传输带宽`",
              "`B=执行一组任务时可用带宽容量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 123,
        label: '容量',
        des: "用于评估产品或系统参数的最大限量满足需求的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1231,
            label: '事务处理容量',
            des: "单位时间内处理事务的数量是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=观察时间内完成事务的数量`",
              "`B=观察时间`"
            ],
            selected: false
          },
          {
            id: 1232,
            label: '用户访问量',
            des: "某一时刻，可同时访问系统的用户数量是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{A_i}{n}`",
            factors: [
              "`A_i=第i次观察中，同时访问系统的最大用户数量`",
              "`n=观察次数`"
            ],
            selected: false
          },
          {
            id: 1233,
            label: '用户访问增长的充分性',
            des: "单位时间内可成功添加用户的数量是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=观察时间内成功增加的用户数量`",
              "`B=观察时间`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 124,
        label: '性能效率的依从性',
        des: "用于评估产品或系统遵循与性能效率相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1241,
            label: '性能效率的依从性',
            des: "遵循与产品或系统的效率相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与效率依从性相关的项数`",
              "`B=与性能效率的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  },
  {
    id: 13,
    label: '兼容性',
    des: "用于评估在共享相同的硬件或软件环境的条件下，产品、系统或组件能够与其他产品、系统或组件交换信息和/或执行其所需的功能的程度。",
    val: 0.0,
    selected: false,
    children: [
      {
        id: 131,
        label: '共存性',
        des: "用于评估与其他产品共享通用的环境和资源的条件下，产品能够有效执行其所需的功能并且不会对其他产品造成负面影响的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1311,
            label: '与其他产品的共存性',
            des: "规定的其他软件产品可以与该软件产品共享环境，而不会对质量特性或功能产生负面影响的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=与该产品可共存的其他规定的软件产品数量`",
              "`B=在运行环境中，该产品需要与其他软件产品共存的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 132,
        label: '互操作性',
        des: "用于评估两个或多个系统、产品或组件能够交换信息并使用已交换的信息的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1321,
            label: '数据格式可交换性',
            des: "与其他软件或系统交换规定的数据格式的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=与其他软件或系统可交换数据格式的数量`",
              "`B=需要交换的数据格式数量`"
            ],
            selected: false
          },
          {
            id: 1322,
            label: '数据交换协议充分性',
            des: "支持规定的数据交换协议的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际支持数据交换协议的数量`",
              "`B=规定支持的数据交换协议数量`"
            ],
            selected: false
          },
          {
            id: 1323,
            label: '外部接口充分性',
            des: "支持规定的外部接口（与其他软件和系统的接口）的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=有效的外部接口数量`",
              "`B=规定的外部接口数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 133,
        label: '兼容性的依从性',
        des: "用于评估产品或系统遵循与兼容性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1331,
            label: '兼容性的依从性',
            des: "遵循与产品或系统的兼容性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与兼容性的依从性相关的项数`",
              "`B=与兼容性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  },
  {
    id: 14,
    label: '易用性',
    des: "用于评估在指定使用周境中，产品或系统在有效性、效率和满意度特性方面，为了达到所指定的目标可被特定用户使用的程度。",
    val: 0.0,
    selected: false,
    children: [
      {
        id: 141,
        label: '可辨识性',
        des: "用于评估用户能够辨识产品或系统是否适合他们的要求的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1411,
            label: '描述的完整性',
            des: "在产品描述或用户文档中描述使用场景的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在产品描述或用户文档中所描述的使用场景数量`",
              "`B=产品的使用场景数量`"
            ],
            selected: false
          },
          {
            id: 1412,
            label: '演示覆盖率',
            des: "有多少比例的任务具有让用户辨识其适合性的演示能力？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=具有演示功能的任务的数量`",
              "`B=期望能从演示功能中获益的任务数量`"
            ],
            selected: false
          },
          {
            id: 1413,
            label: '入口点的自描述性',
            des: "网站的引导页中能说明该网站目的的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=能说明网站目的的引导页数量`",
              "`B=网站中引导页的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 142,
        label: '易学性',
        des: "用于评估在指定使用周境中，产品或系统在有效性、效率、抗风险和满意度特性方面，为了学习使用该产品或系统这一指定目标，可为指定用户使用的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1421,
            label: '用户指导完整性',
            des: "在用户文档和/或帮助机制中有多少比例的功能，能充分描述并能使用户使用这些功能？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在用户文档和//或帮助机制中按要求描述的功能数量`",
              "`B=要求实现的功能总数量`"
            ],
            selected: false
          },
          {
            id: 1422,
            label: '输入字段的默认值',
            des: "在具有默认值的输入字段中，可以自动填充默认值的输入字段比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=运行过程中自动填充默认值的输入字段数量`",
              "`B=具有默认值的输入字段的数量`"
            ],
            selected: false
          },
          {
            id: 1423,
            label: '差错信息的易理解性',
            des: "差错信息中能够给出差错发生的原因以及解决方法的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=给出差错发生原因及可能解决方法的差错信息数量`",
              "`B=差错信息的数量`"
            ],
            selected: false
          },
          {
            id: 1424,
            label: '用户界面的自解释性',
            des: "呈现给用户的信息元素和步骤中有多大比例能帮助新用户在没有先前学习或训练或寻求外部帮助的情况下完成常规任务？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=以用户可以理解的方式所呈现信息元素和步骤的数量`",
              "`B=对于新用户来说完成常规任务所需信息元素和步骤的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 143,
        label: '易操作性',
        des: "用于评估产品或系统具有易于操作和控制的属性的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1431,
            label: '操作一致性',
            des: "交互式任务在多大程度上具有在任务内和类似任务中一致的行为和外观？",
            type: 1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=不一致的特定交互式任务数量`",
              "`B=需要一致的交互任务的数量`"
            ],
            selected: false
          },
          {
            id: 1432,
            label: '消息的明确性',
            des: "系统能给用户传达正确结果或指令消息的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=传达给用户正确结果或指令的消息数量`",
              "`B=实现的消息数量`"
            ],
            selected: false
          },
          {
            id: 1433,
            label: '功能的易定制性',
            des: "为使用方便，用户能够定制功能和操作规程的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=为用户使用方便而提供的可被定制的功能和操作规程的数量`",
              "`B=用户能够受益于定制的功能和操作规程的数量`"
            ],
            selected: false
          },
          {
            id: 1434,
            label: '用户界面的易定制性',
            des: "在外观上可以定制的用户界面元素的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=以定制的用户界面元素数量`",
              "`B=期望能够受益于定制的用户界面元素数量`"
            ],
            selected: false
          },
          {
            id: 1435,
            label: '监视能力',
            des: "在运营过程中，功能状态可被监视的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=具有状态监视能力的功能数量`",
              "`B=期望受益于监视能力的功能数量`"
            ],
            selected: false
          },
          {
            id: 1436,
            label: '撤销操作能力',
            des: "具有重要结果的任务中可提供重新确认选项或撤销操作的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=提供撤销操作或重新确认的任务数量`",
              "`B=用户能够从重新确认或撒销操作中获益的任务数量`"
            ],
            selected: false
          },
          {
            id: 1437,
            label: '信息分类的易理解性',
            des: "软件在多大程度上按目标用户所熟悉并方便用户工作的类别管理信息？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=对于预期用户来说，熟悉和方便的信息结构数量`",
              "`B=使用的信息结构数量`"
            ],
            selected: false
          },
          {
            id: 1438,
            label: '外观一致性',
            des: "具有相似项的用户界而中拥有相似外观的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=具有相似项但外观不同的用户界面的数量`",
              "`B=具有相似项的用户界面的数量`"
            ],
            selected: false
          },
          {
            id: 1439,
            label: '输入设备的支持性',
            des: "通过所有适当的输入方法（例如键盘、鼠标或语音）启动任务的程度如何？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=可由所有适当的输入方法启动任务的数量`",
              "`B=系统支持的任务数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 144,
        label: '用户差错防御性',
        des: "用于评估产品或系统预防用户犯错的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1441,
            label: '抵御误操作',
            des: "有多少比例的用户操作和输入可以防止导致系统故障？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际操作中可以防止导致系统故障的用户操作和输入的数量`",
              "`B=可以防止导致系统故障的用户操作和输入的数量`"
            ],
            selected: false
          },
          {
            id: 1442,
            label: '用户输入差错纠正率',
            des: "系统在多大程度上为检测到的用户输入差错提供正确值，并给出原因？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=系统提供建议的修改值的输入差错数量`",
              "`B=检测到的输入差错数量`"
            ],
            selected: false
          },
          {
            id: 1443,
            label: '用户差错易恢复性',
            des: "系统可纠正或恢复用户差错的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=由系统恢复的用户差错数量，这些用户差错是经设计并测试的`",
              "`B=操作过程中可能发生的用户差错数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 145,
        label: '用户界面舒适性',
        des: "用于评估用户界面提供令人愉悦和满意的交互的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1451,
            label: '用户界面外观舒适性',
            des: "用户界面和整体设计在外观舒适上令人愉悦的程度如何？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在外观舒适性上令人愉悦的显示界面数量`",
              "`B=显示界面数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 146,
        label: '易访问性',
        des: "用于评估在指定使用周境中，为了达到指定的目标，产品或系统被具有最广泛的特征和能力的个体所使用的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1461,
            label: '特殊群体的易访问性',
            des: "特殊群体用户成功使用系统的程度如何（如适用，使用辅助技术）？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=特殊群体用户成功使用的功能数量`",
              "`B=实现的功能数量`"
            ],
            selected: false
          },
          {
            id: 1462,
            label: '支持的语种充分性',
            des: "能支持多少种不同的语种？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际支持的语种数量`",
              "`B=需要支持的语种数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 147,
        label: '易用性的依从性',
        des: "用于评估产品或系统遵循与易用性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1471,
            label: '易用性的依从性',
            des: "遵循与产品或系统的易用性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与易用性的依从性相关的项数`",
              "`B=与易用性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  },
  {
    id: 15,
    label: '可靠性',
    des: "用于评估系统、产品或组件在指定条件下、指定时间内执行指定功能的程度。",
    val: 0.0,
    selected: false,
    children: [
      {
        id: 151,
        label: '成熟性',
        des: "用于评估系统、产品或组件在正常运行时满足可靠性要求的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1511,
            label: '故障修复率',
            des: "检测到与可靠性相关的故障中已被修复的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=设计//编码//测试阶段修复的与可靠性相关故障数`",
              "`B=设计//编码//测试阶段检测到的与可靠性相关的故障数`"
            ],
            selected: false
          },
          {
            id: 1512,
            label: '平均失效间隔时间(MTBF)',
            des: "在系统/软件运行过程中平均失效间隔时间是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=运行时间`",
              "`B=实际发生的系统//软件失效次数`"
            ],
            selected: false
          },
          {
            id: 1513,
            label: '周期失效率',
            des: "在一个预定义的周期内发生失效的数量是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在观察时间内检测到的失效数量`",
              "`B=观察持续周期数`"
            ],
            selected: false
          },
          {
            id: 1514,
            label: '测试覆盖率',
            des: "实际执行的系统或软件能力、运行场景或功能与预期的系统或软件能力、运行场景或功能的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际所执行的系统或软件能力、运行场景或功能的数量`",
              "`B=预期包含的系统或软件能力、运行场景或功能的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 152,
        label: '可用性',
        des: "用于评估系统、产品或组件在需要使用时能够进行操作和访问的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1521,
            label: '系统可用性',
            des: "在计划的系统运行时间中，系统实际可用时间的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际提供的系统运行时间`",
              "`B=操作计划中规定的系统运行时间`"
            ],
            selected: false
          },
          {
            id: 1522,
            label: '平均宕机时间',
            des: "失效发生时，系统不可用的时间是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=总的宕机时间`",
              "`B=观察到的宕机数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 153,
        label: '容错性',
        des: "用于评估当存在硬件或软件故障时，系统、产品或组件的运行符合预期的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1531,
            label: '避免失效率',
            des: "能控制多少种故障模式（以测试用例为单位）以避免关键或严重的失效？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=避免发生关键和严重失效的次数(以测试用例为单位计算的数量)`",
              "`B=测试中执行的故障模式(几乎导致失效)的测试用例数量`"
            ],
            selected: false
          },
          {
            id: 1532,
            label: '组件的冗余度',
            des: "为避免系统失效而安装冗余组件比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=AB`",
            factors: [
              "`A=冗余安装系统组件的数量`",
              "`B=系统组件数量`"
            ],
            selected: false
          },
          {
            id: 1533,
            label: '平均故障通告时间',
            des: "系统报告故障的发生的快慢程度如何？",
            type: -1,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i-B_i)}{n}`",
            factors: [
              "`A_i=系统报告故障i的时刻`",
              "`B_i=故障i被检测到的时刻`",
              "`n=检测到的故障数`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 154,
        label: '易恢复性',
        des: "用于评估发生中断或失效时，产品或系统能够恢复直接受影响的数据并重建期望的系统状态的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1541,
            label: '平均恢复时间',
            des: "软件/系统从失效中恢复需要多长时间？",
            type: 1,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{A_i}{n}`",
            factors: [
              "`A_i=由于第i次失效而重新启动，并恢复宕机的软件//系统所花费的总时间`",
              "`n=发生失效的次数`"
            ],
            selected: false
          },
          {
            id: 1542,
            label: '数据备份完整性',
            des: "定期备份数据项的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际定期备份数据项的数量`",
              "`B=需要备份的数据项的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 155,
        label: '可靠性的依从性',
        des: "用于评估产品或系统遵循与可靠性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1551,
            label: '可靠性的依从性',
            des: "遵循与产品或系统的可靠性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与可靠性的依从性相关的项数`",
              "`B=与可靠性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  },
  {
    id: 16,
    label: '信息安全性',
    des: "用于评估产品或系统保护信息和数据的程度，以使用户、其他产品或系统具有与其授权类型和授权等级一致的数据访问度。",
    val: 0.0,
    selected: false,
    children: [
      {
        id: 161,
        label: '保密性',
        des: "用于评估产品或系统确保数据只有在被授权时才能被访问的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1611,
            label: '访问控制性',
            des: "保密数据项避免未经授权访问的比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=未经授权可访问的保密数据项的数量`",
              "`B=需要访问控制的保密数据项的数量`"
            ],
            selected: false
          },
          {
            id: 1612,
            label: '数据加密正确性',
            des: "按照需求规格说明中的要求，实现数据项加密/解密的正确程度如何？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=正确加密//解密的数据项数量`",
              "`B=需要加密//解密的数据项数量`"
            ],
            selected: false
          },
          {
            id: 1613,
            label: '加密算法的强度',
            des: "加密算法经过严格审查的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=使用时遭到破坏或存在不可接受风险的加密算法的数量`",
              "`B=所使用的加密算法的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 162,
        label: '完整性',
        des: "用于评估系统、产品或组件防止未授权访问、篡改计算机程序或数据的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1621,
            label: '数据完整性',
            des: "防止因未经授权访问而造成的数据破坏或篡改的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=因未经授权访问而破坏或篡改数据项的数量`",
              "`B=需要避免数据破坏或篡改的数据项数量`"
            ],
            selected: false
          },
          {
            id: 1622,
            label: '内部数据抗讹误性',
            des: "采取数据抗讹误性方法的程度如何？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际用于数据抗讹误性方法的数量`",
              "`B=可用及推荐的用于数据抗讹误性方法的数量`"
            ],
            selected: false
          },
          {
            id: 1623,
            label: '缓冲区溢出防止率',
            des: "为防止缓冲区溢出，在软件模块中，对带有用户输入的内存访问已经进行了边界值检查的比例是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在带有用户输入的内存访问中，经过边界值检查的访问数量`",
              "`B=软件模块中带有用户输入的内存访问数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 163,
        label: '抗抵赖性',
        des: "用于评估活动或事件发生后可以被证实且不可被否认的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1631,
            label: '数字签名使用率',
            des: "使用数字签名，处理需要抗抵赖性事务的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际使用数字签名确保抗抵赖性事务的数量`",
              "`B=使用数字签名要求抗抵赖性事务的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 164,
        label: '可核查性',
        des: "用于评估实体的活动可以被唯一地追溯到该实体的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1641,
            label: '用户审计跟踪的完整性',
            des: "对用户访问系统或数据的审计跟踪的完整程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=所有日志中记录的访问次数`",
              "`B=对系统或数据的访问次数`"
            ],
            selected: false
          },
          {
            id: 1642,
            label: '系统日志保留满足度',
            des: "系统日志存储在稳定存储器中的时间占要求的存储时间的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=系统日志实际存储在稳定存储器中的时间`",
              "`B=要求系统日志存储在稳定存储器中的时间`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 165,
        label: '真实性',
        des: "用于评估对象或资源的身份标识能够被证实符合其声明的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1651,
            label: '鉴别机制的充分性',
            des: "系统对主体身份的鉴别程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=提供鉴别机制的数量(例如用户ID//密码或IC卡)`",
              "`B=规定的鉴别机制数量`"
            ],
            selected: false
          },
          {
            id: 1652,
            label: '鉴别规则的符合性',
            des: "建立所需的鉴别规则的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=已实现的鉴别规则的数量`",
              "`B=规定的鉴别规则的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 166,
        label: '信息安全性的依从性',
        des: "用于评估产品或系统遵循与信息安全性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1661,
            label: '信息安全性的依从性',
            des: "遵循与产品或系统的信息安全性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与信息安全性的依从性相关的项数`",
              "`B=与信息安全性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  },
  {
    id: 17,
    label: '维护性',
    des: "用于评估产品或系统能够被预期的维护人员修改的有效性和效率的程度。",
    val: 0.0,
    selected: false,

    children: [
      {
        id: 171,
        label: '模块化',
        des: "用于评估由多个独立组件组成的系统或计算机程序，其中一个组件的变更对其他组件的影响最小的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1711,
            label: '组件间的耦合度',
            des: "系统或计算机程序中组件间存在的依赖关系的强弱程度如何，以及有多少组件不受其他组件更改的影响？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=所实现的对其他组件没有产生影响的组件数量`",
              "`B=需要独立的组件数量`"
            ],
            selected: false
          },
          {
            id: 1712,
            label: '圈复杂度的充分性',
            des: "具有可接受的圈复杂度的软件模块数量是多少？",
            type: -1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=圈复杂度的得分超过规定阈值的软件模块数量`",
              "`B=已实现的软件模块数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 172,
        label: '可重用性',
        des: "用于评估资产能够被用于多个系统，或其他资产建设的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1721,
            label: '资产的可重用性',
            des: "系统中可重复使用资产的数量是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=为可重复使用而设计和实现的资产的数量`",
              "`B=系统中资产的数量`"
            ],
            selected: false
          },
          {
            id: 1722,
            label: '编码规则符合性',
            des: "符合所要求编码规则的模块的数量是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=符合特定系统编码规则的软件模块数量`",
              "`B=已实现的软件模块数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 173,
        label: '易分析性',
        des: "用于评估预期变更（变更产品或系统的一个或多个部分）对产品或系统的影响、诊断产品或系统的缺陷或失效原因、识别待修改部分的有效性和效率的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1731,
            label: '系统日志完整性',
            des: "系统将其操作记录在日志中的程度如何，以便它们可以追踪？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=实际记录在系统中的日志条数`",
              "`B=操作期间审计跟踪所需的日志条数`"
            ],
            selected: false
          },
          {
            id: 1732,
            label: '诊断功能有效性',
            des: "满足原因分析需求的诊断功能比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=对原因分析有效的诊断功能数量`",
              "`B=已实现的诊断功能数量`"
            ],
            selected: false
          },
          {
            id: 1733,
            label: '诊断功能充分性',
            des: "所需诊断功能的实现比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=已实现的诊断功能数量`",
              "`B=需要实现的诊断功能数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 174,
        label: '易修改性',
        des: "用于评估产品或系统可以被有效地、高效地修改，且不会引入缺陷或降低现有产品质量的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1741,
            label: '修改的效率',
            des: "与预期时间相比，修改的效率如何？",
            type: 1,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i / B_i)}{n}`",
            factors: [
              "`A_i=对一个指定类型的修改i所消耗的总工作时间`",
              "`B_i=对一个指定类型的修改i所消耗的预期时间`",
              "`n=测量的修改数量`"
            ],
            selected: false
          },
          {
            id: 1742,
            label: '修改的正确性',
            des: "已正确实施的修改所占比例是多少？",
            type: 1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=在实施后的规定时间内，导致事故或失效发生的修改数量`",
              "`B=实施的修改数量`"
            ],
            selected: false
          },
          {
            id: 1743,
            label: '修改的能力',
            des: "在指定的持续时间内进行所需修改的程度如何？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在指定的持续时间内实际做出修改的项目数`",
              "`B=在指定的持续时间内要求修改的项目数`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 175,
        label: '易测试性',
        des: "用于评估能够为系统、产品或组件建立测试准则，并通过测试执行来确定测试准则是否被满足有效性和效率的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1751,
            label: '测试功能的完整性',
            des: "已实现的测试功能完整性程度如何？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=按照规定已实现的测试功能数量`",
              "`B=需要的测试功能的数量`"
            ],
            selected: false
          },
          {
            id: 1752,
            label: '测试独立性',
            des: "软件测试独立性的程度如何？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在依赖其他系统测试时，能被桩模拟的测试数量`",
              "`B=依赖其他系统的测试数量`"
            ],
            selected: false
          },
          {
            id: 1753,
            label: '测试的重启动性',
            des: "维护后，能否容易地从重启动点运行测试？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在逐步检测的期望点，维护方能够暂停并重启执行中的测试运行的事例数`",
              "`B=执行中的测试运行能被暂停的事例数`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 176,
        label: '维护性的依从性',
        des: "用于评估产品或系统遵循与维护性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1761,
            label: '维护性的依从性',
            des: "遵循与产品或系统的维护性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与维护性的依从性相关的项数`",
              "`B=与维护性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  },
  {
    id: 18,
    label: '可移植性',
    des: "用于评估系统、产品或组件能够从一种硬件、软件或者其他运行（或使用）环境迁移到另一种环境的有效性和效率的程度。",
    "name": "可移植性",
    val: 0.0,
    selected: false,
    children: [
      {
        id: 181,
        label: '适应性',
        des: "用于评估产品或系统能够有效地、高效地适应不同的或演变的硬件、软件或者其他运营（或使用）环境的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1811,
            label: '硬件环境的适应性',
            des: "软件或系统是否能够适应不同的硬件环境？",
            type: 1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=测试期间未完成或结果没有达到要求的功能数量`",
              "`B=不同硬件环境中需要测试的功能数量`"
            ],
            selected: false
          },
          {
            id: 1812,
            label: '系统软件环境的适应性',
            des: "软件或系统是否能够适应不同的系统软件环境？",
            type: 1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=测试期间未完成或结果没有达到要求的功能数量`",
              "`B=不同系统软件环境下需要测试的功能数量`"
            ],
            selected: false
          },
          {
            id: 1813,
            label: '运营环境的适应性',
            des: "软件或系统是否能够适应不同的运营环境？",
            type: -1,
            val: 0.0,
            equation: "`X=1 - A/B`",
            factors: [
              "`A=在带有用户环境的运营测试中，测试期间没有完成或结果没有达到要求的功能数量`",
              "`B=在不同运营环境中测试的功能数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 182,
        label: '易安装性',
        des: "用于评估在指定环境中，产品或系统能够成功地安装和/或卸载的有效性和效率的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1821,
            label: '安装的时间效率',
            des: "与预期安装时间相比，实际安装的效率如何？",
            type: 0,
            val: 0.0,
            equation: "`X=\\sum_{i=1}^{n} \\frac{(A_i / B_i)}{n}`",
            factors: [
              "`A_i=第i次安装所消耗的总工作时间`",
              "`B_i=第i次安装的预期时间`",
              "`n=测量的安装次数`"
            ],
            selected: false
          },
          {
            id: 1822,
            label: '安装的灵活性',
            des: "为使用方便，用户或维护方是否可以自定义安装规程？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=用户成功自定义安装规程的数量`",
              "`B=为使用方便，用户尝试自定义安装规程的数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 183,
        label: '易替换性',
        des: "用于评估在相同的环境中，产品能够替换另一个相同用途的指定软件产品的程度。",
        val: 0.0,
        selected: false,
        children: [
          {
            id: 1831,
            label: '使用相似性',
            des: "原软件产品被替换后，本软件产品的用户功能中有多少功能可以在没有额外学习或变通的情况下执行？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=替换原软件产品后，本软件产品在没有任何额外的学习或变通的情况下，能够执行的用户功能数量`",
              "`B=替换原软件产品后，本软件产品中用户功能的数量`"
            ],
            selected: false
          },
          {
            id: 1832,
            label: '产品质量等价性',
            des: "原软件产品被替换后，满足要求的质量测度的比例是多少？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=优于或等于被替换产品的新产品质量测度数量`",
              "`B=被替换软件产品中的质量测度数量`"
            ],
            selected: false
          },
          {
            id: 1833,
            label: '功能的包容性',
            des: "原软件产品被替换后，类似功能能否容易被使用？",
            type: 0,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=结果与被替换软件产品相似的产品功能数量`",
              "`B=被替换软件产品中需要使用的功能数量`"
            ],
            selected: false
          },
          {
            id: 1834,
            label: '数据复用/导入能力',
            des: "原软件产品被替换后，相同的数据能否继续使用？",
            type: -1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=能像被替换软件产品一样继续使用的数据数量`",
              "`B=被替换软件产品中需要维续使用的数据数量`"
            ],
            selected: false
          }
        ]
      },
      {
        id: 184,
        label: '可移植性的依从性',
        des: "用于评估产品或系统遵循与可移植性相关的标准、约定或法规以及类似规定的程度。",
        val: 0.0,
        selected: false,
        isLeaf: false,
        children: [
          {
            id: 1841,
            label: '可移植性的依从性',
            des: "遵循与产品或系统的可移植性相关的标准、约定或法规以及类似规定的程度如何？",
            type: 1,
            val: 0.0,
            equation: "`X=A/B`",
            factors: [
              "`A=在评价中已证实的正确实现的与可移植性的依从性相关的项数`",
              "`B=与可移植性的依从性相关的项数`"
            ],
            selected: false
          }
        ]
      },
    ]
  }
  ]
}