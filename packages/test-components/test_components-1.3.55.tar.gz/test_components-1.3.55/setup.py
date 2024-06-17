#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

# 需要将那些包导入
packages = ["test_components", "test_components.toolkit"]



# 第三方依赖
requires = [

]

setup(
    name="test_components",  # 包名称
    version="1.3.55",  # 包版本
    description="自动化接口组件封装",  # 包详细描述
    long_description="接口自动化脚本常规方法封装",  # 长描述，通常是readme，打包到PiPy需要
    author="张晓平",  # 作者名称
    author_email="123@qq.com",  # 作者邮箱
    url="http://www.example.com/~cschultz/bvote/",  # 项目官网
    packages=packages,  # 项目需要的包
    include_package_data=False,  # 是否需要导入静态数据文件
    # python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    python_requires=">=3.0",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[  # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
