from setuptools import setup, find_packages

with open("README.rst", encoding='utf-8') as f:
    long_description = f.read()

setup(name='matplotlib_Chinese',  # 包名
      version='0.0.4',  # 版本号
      description='matplotlib工具包的汉化版，使用方法与原版完全相同，若有汉化BUG请及时联系作者！',
      long_description=long_description,
      author='Jhonie King(王骏诚)',
      author_email='queenelsaofarendelle2022@gmail.com',
      license='MIT License',
      packages=find_packages(),  # 自动查找并包含所有子文件夹
      include_package_data=True,  # 启用包括包数据
      package_data={
          '': ['*.png', '*.jpg', '*.ttf', '*.otf', '*.txt', '*.md'],
          'matplotlib': ['*'],
          'dateutil': ['*'],
          'mpl_toolkits': ['*'],
          'PIL': ['*'],
          'fontTools': ['*'],
      },
      py_modules=['six', 'pylab'],
      keywords=['python', 'matplotlib', 'Chinese'],
      install_requires=['packaging', 'pyparsing', 'cycler', 'kiwisolver', 'numpy'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
