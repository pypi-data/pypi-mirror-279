from setuptools import setup, find_packages

setup(
    name='xiaozu',
    version='0.1',
    author='nsu.edu.Software Technology.22102.pthon.Group5',
    author_email='zhouyixin5544773@163.com',
    description='A brief description of the package',
    packages=find_packages(),
    install_requires=[
        'customtkinter',  # 确保customtkinter库已安装在目标环境中
        'tk',  # Tkinter是Python的标准库，通常不需要单独安装
    ],
    entry_points={
        'console_scripts': [
            'xiaozu=xiaozu.BlankApp:main',
        ],
    },
)
