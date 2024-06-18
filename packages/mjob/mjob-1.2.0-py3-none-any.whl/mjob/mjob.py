#!/bin/env python
# author: sirui.li@timekettle.co

import os
import argparse
from concurrent import futures
from tqdm import tqdm


def create_directory(directory):
    # 创建目录，如果目录已存在则不进行任何操作
    os.makedirs(directory, exist_ok=True)


def prepare_file_list(file_list_path, old_dir, new_dir, task):
    file_list = []
    print("Preparing the file list...")
    with open(file_list_path, 'r') as f:
        lines = [line.strip() for line in f]
        for line in tqdm(lines, total=len(lines)):
            if new_dir and task in ['resample', 'copy', 'link']:
                # 如果任务是'resample'或'copy'，则替换文件路径中的旧目录部分为新目录
                new_line = line.replace(old_dir, new_dir)
                new_path = os.path.dirname(new_line)
                create_directory(new_path)
            else:
                new_line = line
            file_list.append([line, new_line])
    return file_list


def resample_file(file_list):
    source_path, target_path = file_list[0], file_list[1]
    if os.path.exists(target_path):
        return
    # 使用sox命令对音频文件进行重新采样
    cmd = "sox -V1 {} -r 16000 -b 16 -c 1 {}".format(source_path, target_path)
    os.system(cmd)


def delete_file(file_list):
    source_path = file_list[0]
    if not os.path.exists(source_path):
        return
    # 删除文件或文件夹
    cmd = "rm -rf {}".format(source_path)
    os.system(cmd)


def copy_file(file_list):
    source_path, target_path = file_list[0], file_list[1]
    if os.path.exists(target_path):
        return
    # 复制文件
    cmd = "cp -r {} {}".format(source_path, target_path)
    os.system(cmd)

def link_file(file_list):
    source_path, target_path = file_list[0], file_list[1]
    if os.path.exists(target_path):
        return
    # 复制文件
    cmd = "ln -s {} {}".format(source_path, target_path)
    os.system(cmd)


def run_command(file_list):
    cmd = file_list[0]
    # 运行命令
    os.system(cmd)


def show_directory(file_list):
    source_path = file_list[0]
    # 显示目录内容
    cmd = "ls {}".format(source_path)
    os.system(cmd)


def main():
    '''
    脚本功能：基于给定的文件列表执行并行任务
    --task:
        重新采样：resample
        删除文件/文件夹：delete
        复制文件：copy
        运行命令：run
        显示目录：show
        软连接：link
    --file_list:
        每行一个文件路径
    --old_dir:
        需要替换的原始文件路径部分
    --new_dir:
        用指定的新路径替换--old_dir路径
    --nj:
        并行执行的进程数
    --thread:
        使用多线程方式运行
    '''
    parser = argparse.ArgumentParser(description="基于给定的文件列表执行并行任务")
    parser.add_argument('--task', '-t', type=str, required=True, choices=['resample', 'delete', 'copy', 'run', 'show', 'link'], help="任务")
    parser.add_argument('--file_list', '-f', type=str, required=True, help="文件列表路径")
    parser.add_argument('--old_dir', '-o', type=str, default='', help="原始目录路径")
    parser.add_argument('--new_dir', '-n', type=str, default='', help="新目录路径")
    parser.add_argument('--nj', type=int, default=8, help="进程数")
    parser.add_argument('--thread', action='store_true', help='使用多线程方式运行')
    args = parser.parse_args()

    task = args.task
    file_list = prepare_file_list(args.file_list, args.old_dir, args.new_dir, task)
    task_functions = {
        'resample': resample_file,
        'delete': delete_file,
        'copy': copy_file,
        'run': run_command,
        'show': show_directory,
        'link': link_file
    }

    print(f"Executing {task_functions[task]} task...")
    process_func = futures.ThreadPoolExecutor if args.thread else futures.ProcessPoolExecutor
    with process_func(max_workers=args.nj) as executor:
        list(tqdm(executor.map(task_functions[task], file_list), total=len(file_list)))


if __name__ == '__main__':
    main()
