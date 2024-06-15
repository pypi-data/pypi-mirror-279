import setuptools
from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
import os
import sys
import glob
import shutil

class CustomInstallCommand(install):
    def run(self):
        # copy data
        os.makedirs('C:/ProgramData/Peridyno/data/font', exist_ok=True)
        base_dir = os.getcwd()
        source_path = os.path.join(base_dir, 'src/font')
        destination_path = 'C:/ProgramData/Peridyno/data/font'
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

        # copy cufft
        cuda_path = os.getenv('CUDA_PATH')
        # 如果CUDA_PATH环境变量没有被设置，则退出脚本
        if cuda_path is None:
            print("CUDA_PATH 环境变量未设置")
            exit()
        cuda_path_bin = cuda_path + '\\bin'
        cuda_path_lib = cuda_path + '\\lib\\x64'
        python_install_path = sys.prefix
        cufft_file_dll = [f for f in os.listdir(cuda_path_bin) if 'cufft' in f]
        cufft_file_lib = [f for f in os.listdir(cuda_path_lib) if 'cufft' in f]
        for file in cufft_file_dll:
            shutil.copy(os.path.join(cuda_path_bin, file), python_install_path)
            print(os.path.join(cuda_path_bin, file))

        for file in cufft_file_lib:
            shutil.copy(os.path.join(cuda_path_lib, file), python_install_path)
            print(os.path.join(cuda_path_lib, file))
        install.run(self)
 
 
setuptools.setup(
    name="PyPeridyno",
    version="0.9.2",
    author="unibeam",
    author_email="xiaowei@iscas.ac.cn",
    description="A python package for Peridyno",
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url="https://peridyno.com/",
    packages=find_packages(),
    # package_dir={'PyPeridyno':'src'}
    package_data={
        'PyPeridyno':['*.dll', '*.pyd', '*.lib', '*.exe'],
    },
    data_files=[
        ('.', [f for pattern in ['src/*.dll', 'src/*.pyd', 'src/*.lib', 'src/*.exe', 'src/*.exp'] for f in glob.glob(pattern)])
    ],
    install_requires=[  # 如果需要其他依赖，请列出
        # 'dependency1',
        # 'dependency2',
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    cmdclass={
        'install':CustomInstallCommand,
    },
    python_requires='>=3.6',
)