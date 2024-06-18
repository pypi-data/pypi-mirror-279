# 列表并行

列表并行是一个用于并行处理列表任务的工具。它提供了一种简单而高效的方式来执行并行任务，针对给定的列表进行处理。

## 功能

- 并行执行任务：利用多线程或多进程的方式，并行处理给定的列表任务。
- 灵活的任务定义：可以自定义任务函数，根据具体需求对列表中的每个元素进行处理。
- 可配置的并行度：可以根据系统资源和任务复杂度，灵活地调整并行度。
- 进度跟踪和错误处理：提供进度跟踪功能，以及错误处理和日志记录，方便调试和排查问题。

## 安装

列表并行可以通过以下步骤进行安装：

1. 从源码安装：

```shell
git clone https://github.com/timekettle/mjob.git 
cd mjob
python -m pip install ./
```

2. 从pypi安装

```shell
pip install mjob
```

## 使用示例
1. 首先自行准备`test.list`(要处理的文件列表)
```shell
# 文件夹结构
data
├── 001.txt
├── 002.txt
├── 003
│   └── 003.txt
└── 004
    └── 004.txt

# 生成文件列表
find data -name "*.txt" >test.list
```
2. 指定不同的`task`，为文件列表执行不同的操作
```shell
# 查看参数说明
mjob --help

# 通过给定的test.list文件，快速复制到包含 data_new 的新目录中
mjob --task copy \
--file_list test.list \
--old_dir data \
--new_dir data_new \
--nj 4

# 通过给定的test.list文件，创建软连接到包含 data_new 的新目录中
mjob --task link \
--file_list test.list \
--old_dir data \
--new_dir data_new \
--nj 4

# 通过给定的test.list音频文件列表，快速音频重采样到16k，保存到到包含 data_new 的新目录中
mjob --task resample \
--file_list test.list \
--old_dir data \
--new_dir data_new \
--nj 4

# 通过给定的test.list文件，快速删除文件
mjob --task delete \
--file_list test.list \
--nj 4

# 通过给定的test.list文件，快速展示所有文件
mjob --task show \
--file_list test.list \
--nj 4

# 通过给定的test.list文件，快速执行命令（确保命令的合法性）
mjob --task run \
--file_list test.list \
--nj 4

# 以上任务默认使用多进程方式运行，添加 --thread 参数使用多线程方式运行
mjob --task copy \
--file_list test.list \
--old_dir data \
--new_dir data_new \
--nj 4 \
--thread
```

## 贡献

如果你发现了任何问题或有改进的建议，欢迎提出issue或提交pull request。我们非常欢迎贡献者为该项目做出贡献。
