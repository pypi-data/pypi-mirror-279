from setuptools import setup

setup(name='Mtripix',
      version='0.0.3',
      description='transforms detection data',
      author='TriplePixels',
      author_email='PIPIPINoBrain@163.com',
      requires=['numpy', 'json', 'xml'],  # 定义依赖哪些模块
      #packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      packages=['Mtripix'],  #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0"
      )