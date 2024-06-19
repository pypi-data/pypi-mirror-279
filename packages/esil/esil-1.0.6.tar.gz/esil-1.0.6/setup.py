'''
Author: Devin
Date: 2024-06-13 11:49:52
LastEditors: Devin
LastEditTime: 2024-06-19 00:49:37
Description: 

Copyright (c) 2024 by Devin, All Rights Reserved. 
'''
from setuptools import setup, find_packages

setup(
    name='esil',
    version='1.0.6',
    author='Devin Long',
    author_email='long.sc@qq.com',
    description='commonly used functions writted by Devin Long',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Devin-Long-7/esil',
    # packages=find_packages(),
    packages=['esil'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # include_package_data=True,# 允许包含在 MANIFEST.in 文件中指定的所有文件。
    # package_data={
    #     'esil': ['*.py'],
    #     'esil.rsm': ['RSM/*.py'],
    #     # 'devin_colors': ['color_maps/*.pkl'],  # 包含特定包中的 .pkl 文件
    # },
    
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'pandas',        
        'xarray',
        'scipy',
        'tqdm',
        'netCDF4',
        'pyproj',
        'SQLAlchemy',     
        'chardet',
        'sympy',
        'shapely',
        'pytz',
        'pykrige',
        'matplotlib<3.9,>=1.5',#Basemap 要求的 Matplotlib 版本为小于3.9且大于等于1.5
        'cartopy',        
        'geopandas',   
    ],
    #     # requests >= 9.13.0
    # install_requires =
    # numpy
    # matplotlib
    # ,
)