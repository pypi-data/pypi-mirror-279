
from setuptools import setup, find_packages
setup(name='jobQuery',
      version='2.0.2',
      description='birds atttributes and functions',
      author='megnet',
      author_email='2290906844@qq.com',
      requires= ['numpy','matplotlib'], # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0"
      )