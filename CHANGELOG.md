# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0]

### UPDATED

- 修改：爬虫启动核心代码由原本 CrawlHelper 类的 get_json 方法修改为 SpiderHelper 的 crawl 方法
- 修改：爬虫列表查询核心代码由原本 SpiderListHelper 类的 get_json 方法修改为 SpiderHelper 的 list 方法
- 修改：修改查询爬虫列表响应结果格式，去除 spiders 中的 name 字段
- 修改：项目列表核心代码由原本 ProjectListHelper 类的 get_json 方法修改为 ProjectHelper 的 list 方法
- 修改：修改查询项目列表响应结果格式，去除 projects 中的 name 字段

### ADDED

- 添加：使用命令行关闭爬虫
- 添加：使用web api关闭爬虫
- 添加：对scrapy Telnet接口设置连接超时时间配置
- 添加：暂停爬虫
- 添加：恢复爬虫
- 添加：pypi发布版本，可以使用pip安装环境
- 添加：每次运行命令的时候都会初始化环境（尝试创建数据库、尝试创建运行目录），可以配置 INIT_EACH_RUN 参数关闭

## [0.1.1] - 2020-1-31

### FIXED

- 爬虫日志被关闭，现在启用

### ADDED

- 可以使用api接口启动爬虫

## [0.1.0] - 2020-1-29

### FIXED

- 修正README中命令错误，安装依赖
- 修复无法关闭服务问题

### ADDED

- 添加项目初始化脚本，用于创建数据库（目前仅支持sqlite3）
- 通过脚本启动爬虫

## [0.0.4] - 2019-12-21

### UPDATED

- 修改启动web服务的命令名称
- 修改安装方式

### FIXED

- 修复web服务无法启动的问题

### ADDED

- 将pid写入文件
- 可以使用命令关闭web服务
- 可以重启服务

## [0.0.3] - 2019-12-09

### FIXED

- 修改README格式

## [0.0.2] - 2019-12-09

### FIXED

- 修复获取settings配置失败的问题
- 控制台运行没有__main__入口的问题
- 修改接口响应数据格式

### Added

- 添加版本修改日志
- requirements.txt 中添加 Scrapy 版本
- 添加README.md，添加基本使用方式文档
- 添加CHANGELOG.md，添加版本更新日志

## [0.0.1] - 2019-12-04

### Added

- 基本架构搭建
- 添加命令行运行功能，可以使用命令行获取爬虫信息、控制爬虫运行
- 添加web访问功能，可以启动web服务，通过web接口获取爬虫信息，控制爬虫运行
- 添加爬虫列表查询
- 支持项目列表查询
