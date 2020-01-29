# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
