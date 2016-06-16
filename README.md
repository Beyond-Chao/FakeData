# FakeData
a method to generates fake data for you on both iOS and Andriod platform
### 背景
前段时间，公司项目有一个新的需求模块，功能还算简单，几天差不多就写好了，涉及到与后台数据交互的部分没法继续写了，然后去问了问后台的同学，叫他们给个排期，大概什么时候可以联调，然而他们也不清楚，可能后台那边处理的逻辑挺多。所以回来各种google，看有什么办法能够做到移动端与后端分离，这是对那天小小成果的记录，也在我们团队中分享了下，都觉得挺好，可以在一定程度上提高开发效率。
### 部门的解耦
我们都在强调好的代码应该是各个模块具有较低的耦合性，这样不管是日后需求的更改还是模块的复用都有很大好处，不至于牵一发而动全身，也无需重复造轮子，这是高质量代码和高效率的体现。在移动开发过程中，部门间的解耦，也是值得思考的问题。作为前端和移动端往往和后台服务端的耦合性很高，因为需要后端给我们吐数据，没数据、没法活、都是静态的死的页面，而这些静态页面的搭建相对来说还是很快的。
在后台没有开发完成之前我们能够做哪些：

1. 在本地为一些视图添加一套假数据，比如label、button、imageView，撑起一个功能模块
2. 完善一些交互逻辑，gesture，消息机制，比如协议、通知、target-action。。。
3. 完善UI设计师或交互设计师提出的动画功能
4. 甚至还可以建立一些模型类、定义一些接口，类似这种**#define HXD_BOX_LIST @"box/list" // 店长零食盒列表接口**
5. 还可以自定义一些方法来通过特定的接口获取一些数据。当然现在什么数据也没有，可能还会报网络错误。

4和5能够实施的前提是我们和后台已经约定好需要哪些接口、字段类型、返回的json结构，日后的开发肯定会略微改动的，这不影响，关键是让每次改动和调整实时的告知大家，让负责的开发人员周知。

至此我们能够做的都做了，我们只能等待后台接口，如果后台开发人员不是很给力，那我们的开发进度迟迟不能推进，这样留给我们联调、测试、修复bug的时间很有限，最后只能加班、熬夜、甚至通宵上线、这样的产品是很脆弱的。

总之，我们队后台的服务太过依赖了，部门耦合性太高了。有的人会说，叫后台写一些假数据给你们，但是那多接口每个都造一些造数据，那么项目就会被假数据给污染了、到时候还得一个个的删除，费时费力。再说要是后台不给力，自己手上的功能都没有写完，哪有时间精力给你造假数据啊。那么我们该如何尽可能降低对后台的依赖呢？
### 前端的解决方案
* [Rap](https://github.com/thx/RAP)

有的公司的后台接口管理平台用的就是rap，它是阿里的前端团队开源的Web接口管理工具,可以MOCK规则来自动生成随机数据。

* [MOCK](http://mockjs.com)

[Rap](https://github.com/thx/RAP)提供了```Mock插件```，暂时只支持[jQuery](https://github.com/jquery/jquery) 和 [Kissy](https://github.com/kissyteam/kissy)

在项目中需要引入一个插件代码，获取该插件代码的方式如图：
![img](https://raw.githubusercontent.com/Beyond-Chao/FakeData/master/images/pluginCode.png)

**使用方式：**

将以下代码写在[Kissy](https://github.com/kissyteam/kissy)或[jQuery](https://github.com/jquery/jquery)代码之后即可：

```
	<script type="text/javascript" src="http://{{domainName}}/rap.plugin.js?	projectId={{projectId}}&mode={{mode}}"></script>
```

* `{{projectId}}`为用户所编辑的接口在RAP中的项目ID
* `{{mode}}`为RAP路由的工作模式, 默认值为3
这样就可以拦截Ajax的请求，MOCK就可以为你生成一些符合规则的假数据了。
* `{disableLog}}`为true时会禁止向控制台输出log，仅保留必要部分，默认为false

mode不同值的具体含义如下:

* 0 - 不拦截
* 1 - 拦截全部
* 2 - 黑名单中的项不拦截
* 3 - 仅拦截白名单中的项

具体详见[Mock插件](https://github.com/thx/RAP/wiki/user_manual_cn#mock插件)

### 移动端解决方案  
移动端开发过程中除了需要使用[Rap](https://github.com/thx/RAP) 和 [MOCK](http://mockjs.com)工具外，还有一个很强大工具[Charles](https://www.charlesproxy.com)，这里我们用到一个很牛X的Map功能，Map 功能分Map Remote 和 Map Local 两种，顾名思义，Map Remote 是将指定的网络请求重定向到另一个网址请求地址，**Map Local** 是将指定的网络请求重定向到本地文件，让你可以达到轻松修改服务器返回的内容，不管后台有没有数据返回，我们都能请求到数据，这样就减少了对后台服务的依赖。现在只要保证与该请求对应的本地文件有数据，这次的网络请求就会有数据返回。一般情况返回的都是json格式的数据(XML同理)，现在我们在本地编写一个简单的json格式的文件，不妨叫boxList.json，那[Charles](https://www.charlesproxy.com)是如何映射的呢，很简单在菜单`Tools` -> `Map Local` 然后点击`Add` ，之后的操作按图说话![img](https://raw.githubusercontent.com/Beyond-Chao/FakeData/master/images/mapLocal.png)

现在映射建立好了，那如何生成一个符合项目约定的json文件呢，这个时候[Rap](https://github.com/thx/RAP) 和 [MOCK](http://mockjs.com)就派上用场了，打开[Rap可视化界面](http://rap.taobao.org/org/index.do)登录之后创建一个项目，当然要是你们公司使用的就是它，拿这些都可以省略。进入该项目，进入编辑模式编写相关接口和字段，**必须和你公司接口文档最好保持一致，比如mag、status、data，然后data里面才是真正想要的数据，这种结构最好一致、这样可以轻松过渡、对接到你公司的后台服务， 同时你们项目中封装的网络工具类也无需做任何调整。** 然后自定义一些mock规则，随机生成一些特定的数据。完成后的效果是这样。

![img](https://raw.githubusercontent.com/Beyond-Chao/FakeData/master/images/APIDetail.png)

可以通过点击上方的`Mock数据`按钮来生成json数据。如图

![img](https://raw.githubusercontent.com/Beyond-Chao/FakeData/master/images/previewContent.png)

这个json就可以copy过来放到boxList.json文件中了，至此json数据也很快获取到了。之后就可通过模拟器请求该接口，获取数据了。当然也可以通过浏览器请求了。真机上想要访问的话，得手动设置下HTTP代理，这和通过Charles抓取手机数据请求的设置一样。

**Advantage**

1. 可以完成与后端的分离，实现部门间的解耦
2. 避免本地写一些假数据对项目的侵入和污染
3. 内外网都可以访问，不用担心公司内网的限制
4. 可以轻松对接，不用更改任何东西。当和后台联调时，你只需关闭Charles的 Map Local 功能就OK了


**Disadvantage**

* 每个开发者都必须在本地保存一份与该接口对应的json文件，否则要访问其他模块，结果没有设置映射地址、本地也没有该模块接口对应的json，所以无法获取到数据，不利于团队共享。

```
opinion：
搭建一个专门的映射服务器(测服)，用来维护每个接口对应的json数据，只需维护一份供团队共享。
```


**Attention**

在用[Charles](https://www.charlesproxy.com)的时候不要打开一些翻墙代理，比如 [Lantern](https://github.com/getlantern/lantern) 或者 [shadowsocks](https://github.com/shadowsocks), 否则 [Charles](https://www.charlesproxy.com) 无法正常工作。

**Welcome**

如果你们有什么更好的制造假数据的方法可以通过Issues，与大家一起讨论。

如果该方法对你有帮助，可以在一定程度上提高开发效率，希望能顺便点一下右上角的⭐️Star ^_^，朋友的鼓励和支持是我继续分享的动力

**LearnMore**

更多接口编辑的mock规则如图![img](https://raw.githubusercontent.com/Beyond-Chao/FakeData/master/images/mockRegulation.png)
更多详细的用法可以参数[Rap](https://github.com/thx/RAP)和[Rap用户手册](https://github.com/thx/RAP/wiki/user_manual_cn)

Charles的更多用法: [Charles 从入门到精通](http://blog.devtang.com/2015/11/14/charles-introduction/)

