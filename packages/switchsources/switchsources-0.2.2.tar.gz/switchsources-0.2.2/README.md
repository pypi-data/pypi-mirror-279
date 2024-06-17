<p align="center">
  <br> 中文 | <a href="README-EN.md">English</a>
  <br>One click, Switch all<br>
  <br>轻量级，可配置，跨平台的换源工具<br>
</p>

# SwitchSources

## 安装

```
pip install switchsources
```

## 介绍

SwitchSources是一个帮助开发者切换各种软件源的工具。

## 使用

查看支持的软件
```shell
switchsources ls
```

查看当前软件源
```shell
switchsources check pip
```

切换软件源
```shell
switchsources switch pip
```

配置可选择的源地址
```shell
switchsources add pip https://pypi.tuna.tsinghua.edu.cn/simple
```

删除配置文件中的一个源(列表选择)
```shell
switchsources rs pip
```

删除指定应用下配置文件中的所有源
```shell
switchsources remove pip
```

## 规划

- [x] 支持maven, pip等常见的开源工具的换源
- [x] 支持用户自己配置源地址
- [x] 提供pip安装包
- [ ] 提供brew安装包
- [x] 支持Linux
- [x] 支持Mac
- [ ] 支持windows
- [ ] 支持国产操作系统
- [ ] 支持测速功能
- [ ] 支持自动选择最快源
- [ ] 支持从远程拉取配置文件并使用
