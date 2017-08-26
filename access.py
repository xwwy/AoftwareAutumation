#!/usr/bin/env python
#! _*_ coding:utf-8 _*_

"""
给定安装目录和敏感文件的名字，自动扫描目录下所有文件的权限并进行判断，
敏感文件用逗号分割，也可以不填写

"""
import os
import sys
import stat

class store_all(object):
    """
    将扫描出的所有文件，文件夹进行存储
    """
    def __init__(self):
        self.name = []
        self.named = []
        self.folder = []
        self.folderd = []
        self.all_files = {}
        self.all_folders = {}

    def pushfile(self, files):
        self.name.append(files)

    def pushfolder(self, dirf):
        self.folder.append(dirf)

    def chmod(self):
        for files in self.name:
            chmod_name = oct(os.stat(files).st_mode)[-3:]
            self.named.append(chmod_name)
        for folders in self.folder:
            chmod_folder = oct(os.stat(folders).st_mode)[-3:]
            self.folderd.append(chmod_folder)

        for index in xrange(len(self.name)):
            self.all_files[self.name[index]] = self.named[index]
        for index in xrange(len(self.folder)):
            self.all_folders[self.folder[index]] = self.folderd[index]

store = store_all()

def compare(chmod1, chmod2):
    """
    判断权限是否符合要求
    """
    for index in range(3):
        if int(chmod1[index]) > int(chmod2[index]):
            return False
    return True

def find_all(direction):
    """
    扫描给定目录下所有文件
    """
    all_files = os.walk(direction)
    for root, dirs, name in all_files:
        for files in name:
            store.pushfile(root + os.path.sep + files)
        if dirs:
            for dirf in dirs:
                store.pushfolder(root + os.path.sep + dirf)
    store.chmod()

def check_x(log):
    print u"开始检查所有可执行文件…………"
    log.write("开始检查所有可执行文件…………\n")
    num = 0
    for files in store.all_files:
        if os.access(files, os.X_OK):
            if not compare(store.all_files[files], '750'):
                num = num + 1
                try:
                    print u"可执行文件{file}的权限是{auth}，大于要求的权限750".format(
                        file=files.decode('ascii'),
                        auth=store.all_files[files]
                        )
                    log.write("可执行文件{file}的权限是{auth}，大于要求的权限750\n".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    )
                except UnicodeDecodeError:
                    print u"可执行文件{file}的权限是{auth}，大于要求的权限750".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    log.write("可执行文件{file}的权限是{auth}，大于要求的权限750\n".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    )
    if num:
        print u"可执行文件权限检查完毕，共{}个文件的权限大于750\n".format(num) 
        log.write("可执行文件权限检查完毕，共{}个文件的权限大于750\n\n".format(num))
    else:
        print u"可执行文件权限检查完毕, 没有大于要求权限的文件\n"
        log.write("可执行文件权限检查完毕, 没有大于要求权限的文件\n\n")

def check_nx(log):
    print u"开始检查所有不可执行文件…………"
    log.write("开始检查所有不可执行文件…………\n")
    num = 0
    for files in store.all_files:
        if not os.access(files, os.X_OK):
            if not compare(store.all_files[files], '640'):
                num = num + 1
                try:
                    print u"不可执行文件{file}的权限是{auth}，大于要求的权限750".format(
                        file=files.decode('ascii'),
                        auth=store.all_files[files]
                    )
                    log.write("不可执行文件{file}的权限是{auth}，大于要求的权限750\n".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    )
                except UnicodeDecodeError:
                    print u"不可执行文件{file}的权限是{auth}，大于要求的权限750".format(
                        file=files,
                        auth=store.all_files[files]
                    )
                    log.write("不可执行文件{file}的权限是{auth}，大于要求的权限750\n".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    )
    if num:
        print u"不可执行文件权限检查完毕，共{}个文件的权限大于640\n".format(num)
        log.write("不可执行文件权限检查完毕，共{}个文件的权限大于640\n\n".format(num))
    else:
        print u"不可执行文件权限检查完毕, 没有大于要求权限的文件\n"
        log.write("不可执行文件权限检查完毕, 没有大于要求权限的文件\n\n")

def check_log(log):
    print u"开始检查所有日志文件…………"
    log.write("开始检查所有日志文件…………\n")
    num = 0
    for files in store.all_files:
        if files[-4:] == ".log":
            if not compare(store.all_files[files], '640'):
                num = num + 1
                try:
                    print u"日志文件{file}的权限是{auth}, 大于要求的权限640".format(
                        file=files.decode('ascii'),
                        auth=store.all_files[files]
                    )
                    log.write("日志文件{file}的权限是{auth}, 大于要求的权限640\n".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    )
                except UnicodeDecodeError:
                    print u"日志文件{file}的权限是{auth}, 大于要求的权限640".format(
                        file=files,
                        auth=store.all_files[files]
                    )
                    log.write("日志文件{file}的权限是{auth}, 大于要求的权限640\n".format(
                        file=files,
                        auth=store.all_files[files]
                        )
                    )
    if num:
        print u"日志文件检查完毕，共{}个文件权限大于640\n".format(num)
        log.write("日志文件检查完毕，共{}个文件权限大于640\n\n".format(num))
    else:
        print u"日志文件检查完毕，没有大于要求权限的文件\n"
        log.write("日志文件检查完毕，没有大于要求权限的文件\n\n")

def check_folder(log):
    print u"开始检查所有目录…………"
    log.write("开始检查所有目录…………\n")
    num = 0
    for folder in store.all_folders:
        if not compare(store.all_folders[folder], '750'):
                num = num + 1
                try:
                    print u"目录{file}的权限是{auth}, 大于要求的权限750".format(
                        file=folder.decode('ascii'),
                        auth=store.all_folders[folder]
                    )
                    log.write("目录{file}的权限是{auth}, 大于要求的权限750\n".format(
                        file=folder,
                        auth=store.all_folders[folder]
                        )
                    )
                except UnicodeDecodeError:
                    print u"目录{file}的权限是{auth}, 大于要求的权限750".format(
                        file=folder,
                        auth=store.all_folders[folder]
                    )
                    log.write("目录{file}的权限是{auth}, 大于要求的权限750\n".format(
                        file=folder,
                        auth=store.all_folders[folder]
                        )
                    )
    if num:
        print u"目录检查完毕，共{}个文件权限大于750\n".format(num)
        log.write("目录检查完毕，共{}个文件权限大于750\n\n".format(num))
    else:
        print u"目录检查完毕，没有大于要求权限的文件\n"
        log.write("目录检查完毕，没有大于要求权限的文件\n\n")

def check_mingan(args):
    print u"开始检查敏感文件…………"
    log.write("开始检查敏感文件…………\n")
    num = 0
    file_m = []
    if not args:
        print u"未提供敏感文件，检查结束"
        return True

    for file in store.all_files:
        if file.split(os.path.sep)[-1] in args:
            if not compare(store.all_files[file], '600'):
                num = num + 1
                file_m.append(file.split(os.path.sep)[-1])
                try:
                    print u"敏感文件{file}的权限为{auth}，大于要求的权限600".format(
                        file=file.split(os.path.sep)[-1].decode('ascii'),
                        auth=store.all_files[file]
                    )
                    log.write("敏感文件{file}的权限为{auth}，大于要求的权限600\n".format(
                        file=file.split(os.path.sep)[-1],
                        auth=store.all_files[file]
                        )
                    )
                except UnicodeDecodeError:
                    print u"敏感文件{file}的权限为{auth}，大于要求的权限600".format(
                        file=file.split(os.path.sep)[-1],
                        auth=store.all_files[file]
                    )
                    log.write("敏感文件{file}的权限为{auth}，大于要求的权限600\n".format(
                        file=file.split(os.path.sep)[-1],
                        auth=store.all_files[file]
                        )
                    )
    if not (set(args) - set(file_m)):
        if num:
            print u"敏感文件检查完毕，共{}个文件大于要求的权限\n".format(num)
            log.write("敏感文件检查完毕，共{}个文件大于要求的权限\n\n".format(num))
        else:
            print u"敏感文件检查完毕，没有大于要求的权限的文件\n"
            log.write("敏感文件检查完毕，没有大于要求的权限的文件\n\n")
    else:    
        print u"{}文件未找到，请检查一下输入的文件名称是否正确\n".format(
            list(set(args) - set(file_m))
        )
        log.write("{}文件未找到，请检查一下输入的文件名称是否正确\n\n".format(
            list(set(args) - set(file_m)))
        )

if __name__ == "__main__":
    dirs= sys.argv[1]
    try:
        names = (sys.argv[2]).split(',')    #第二个参数为敏感文件名字，非必选
    except IndexError:
        names = []
    with open((dirs + os.path.sep + 'access.log'), 'w') as log:
        os.chmod(dirs + os.path.sep + 'access.log', stat.S_IRUSR + stat.S_IWUSR + stat.S_IRGRP)
        find_all(dirs)
        check_x(log)
        check_nx(log)
        check_log(log)
        check_folder(log)
        check_mingan(names)
