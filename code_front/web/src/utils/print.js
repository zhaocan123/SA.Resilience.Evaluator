// 打印类属性、方法定义
/* eslint-disable */
const Print = function (dom, options) {
  if (!(this instanceof Print)) return new Print(dom, options);

  this.options = this.extend({
    'noPrint': '.no-print'
  }, options);

  if ((typeof dom) === "string") {
    this.dom = document.querySelector(dom);
  } else {
    this.isDOM(dom)
    this.dom = this.isDOM(dom) ? dom : dom.$el;
  }

  this.init();
};
Print.prototype = {
  init: function () {
    var content = this.getStyle() + this.getHtml();
    this.writeIframe(content);
  },
  extend: function (obj, obj2) {
    for (var k in obj2) {
      obj[k] = obj2[k];
    }
    return obj;
  },

  getStyle: function () {
    var str = "",
      styles = document.querySelectorAll('style,link');
    for (var i = 0; i < styles.length; i++) {
      str += styles[i].outerHTML;
    }
    str += "<style>" + (this.options.noPrint ? this.options.noPrint : '.no-print') + "{display:none;}</style>";
    // 去除height：100%样式，解决分页下，样式混乱问题
    str += "<style>html,body,div{height: auto!important;}</style>";
    // 去除滚动条
    str += "<style>::-webkit-scrollbar{display: none;}</style>";
    // 去除回到顶部按钮
    str += "<style>.el-backtop{display: none;}</style>"
    return str;
  },

  getHtml: function () {
    var inputs = document.querySelectorAll('input');
    var textareas = document.querySelectorAll('textarea');
    var selects = document.querySelectorAll('select');
    var canvass = document.querySelectorAll('canvas');

    for (var k = 0; k < inputs.length; k++) {
      if (inputs[k].type == "checkbox" || inputs[k].type == "radio") {
        if (inputs[k].checked == true) {
          inputs[k].setAttribute('checked', "checked")
        } else {
          inputs[k].removeAttribute('checked')
        }
      } else if (inputs[k].type == "text") {
        inputs[k].setAttribute('value', inputs[k].value)
      } else {
        inputs[k].setAttribute('value', inputs[k].value)
      }
    }

    for (var k2 = 0; k2 < textareas.length; k2++) {
      if (textareas[k2].type == 'textarea') {
        textareas[k2].innerHTML = textareas[k2].value
      }
    }

    for (var k3 = 0; k3 < selects.length; k3++) {
      if (selects[k3].type == 'select-one') {
        var child = selects[k3].children;
        for (var i in child) {
          if (child[i].tagName == 'OPTION') {
            if (child[i].selected == true) {
              child[i].setAttribute('selected', "selected")
            } else {
              child[i].removeAttribute('selected')
            }
          }
        }
      }
    }

    //canvass echars图表转为图片
    for (var k4 = 0; k4 < canvass.length; k4++) {
      var imageURL = canvass[k4].toDataURL("image/png");
      var img = document.createElement("img");
      img.src = imageURL;
      img.setAttribute('style', 'max-width: 100%;');
      img.className = 'isNeedRemove'
      // canvass[k4].style.display = 'none'
      // canvass[k4].parentNode.style.width = '100%'
      // canvass[k4].parentNode.style.textAlign = 'center'
      canvass[k4].parentNode.insertBefore(img,canvass[k4].nextElementSibling);
    }

    // 包裹要打印的元素
    // fix: https://github.com/xyl66/vuePlugs_printjs/issues/36
    // return this.wrapperRefDom(this.dom).outerHTML;
    return this.dom.outerHTML;
  },
  // 向父级元素循环，包裹当前需要打印的元素
  // 防止根级别开头的 css 选择器不生效
  wrapperRefDom: function (refDom) {
    let prevDom = null
    let currDom = refDom
    while (currDom && currDom.tagName.toLowerCase() !== 'body') {
      if (prevDom) {
        let element = currDom.cloneNode(false)
        element.appendChild(prevDom)
        prevDom = element
      } else {
        prevDom = currDom.cloneNode(true)
      }

      currDom = currDom.parentElement
    }

    return currDom.tagName.toLowerCase() === 'body' ? currDom : prevDom
  },

  writeIframe: function (content) {
    var w, doc, iframe = document.createElement('iframe'),
      f = document.body.appendChild(iframe);
    iframe.id = "myIframe";
    //iframe.style = "position:absolute;width:0;height:0;top:-10px;left:-10px;";
    iframe.setAttribute('style', 'position:absolute;width:0;height:0;top:-10px;left:-10px;');
    w = f.contentWindow || f.contentDocument;
    doc = f.contentDocument || f.contentWindow.document;
    doc.open();
    doc.write(content);
    doc.close();
    var _this = this
    iframe.onload = function(){
      _this.toPrint(w);
      setTimeout(function () {
        document.body.removeChild(iframe)
      }, 100)
    }
  },

  toPrint: function (frameWindow) {
    try {
      setTimeout(function () {
        frameWindow.focus();
        try {
          if (!frameWindow.document.execCommand('print', false, null)) {
            frameWindow.print();
          }
        } catch (e) {
          frameWindow.print();
        }
        frameWindow.close();
      }, 10);
    } catch (err) {
      console.log('err', err);
    }
  },
  isDOM: (typeof HTMLElement === 'object') ?
    function (obj) {
      return obj instanceof HTMLElement;
    } :
    function (obj) {
      return obj && typeof obj === 'object' && obj.nodeType === 1 && typeof obj.nodeName === 'string';
    }
};
const MyPlugin = {}
MyPlugin.install = function (Vue, options) {
  // 4. 添加实例方法
  Vue.prototype.$print = Print
}
export default MyPlugin
