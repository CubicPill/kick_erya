# kick_erya
一个刷尔雅网课的脚本

## Usage

### config.json 设置
在 ```config_sample.json``` 填入账号和密码, ```init_url``` 填入要刷的课程主页任意一个章节的 url
```school_id``` 请填入自己学校对应的 id (获取方式见下方)
最后将 ```config_sample.json``` 改名为 ```config.json```

### 获取 school_id
以深圳大学为例

首先打开选择学校页面, 找到自己的学校
![](https://raw.githubusercontent.com/CubicPill/kick_erya/master/images/school-id-1.png

右键点击超链接, 弹出菜单内选择 "审查元素" 选项 (Chrome 浏览器, 其他浏览器可能稍有不同)
![](https://raw.githubusercontent.com/CubicPill/kick_erya/master/images/school-id-2.png)

在弹出的窗口内找到 ```id="xxx"``` 一项, 里面的数字就是 ```school_id```, 填入配置文件即可
![](https://raw.githubusercontent.com/CubicPill/kick_erya/master/images/school-id-3.png)

## TODOs

- 章节测验页面的解析和提交
- 任务点完成检测
- 验证码检测
- 登陆错误信息提示