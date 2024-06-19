'''
Author: Devin
Date: 2024-06-19 12:08:34
LastEditors: Devin
LastEditTime: 2024-06-19 12:09:33
Description: 

Copyright (c) 2024 by Devin, All Rights Reserved. 
'''


import os
import matplotlib
import matplotlib.cm
import numpy as np
from .colormap import Colormap

def list_cmaps():   
    import inspect
    attributes = inspect.getmembers(Colormap, lambda _: not (inspect.isroutine(_)))
    colors = [_[0] for _ in attributes if
              not (_[0].startswith('__') and _[0].endswith('__'))]
    return colors

def show_cmaps(file_dir=None, file_name="colormaps.png"):
    '''
    @description: 显示所有colormap
    @param file_dir: 保存图片的文件夹路径
    @param file_name: 保存图片的文件名
    @return: 保存图片的路径和旋转后的图片路径
    '''
    import matplotlib.pyplot as plt  
    matplotlib.rc('text', usetex=False)
    color = list_cmaps()
    a = np.outer(np.arange(0, 1, 0.001), np.ones(10))
    plt.figure(figsize=(20, 20))
    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.01, right=0.99,wspace=0.5, hspace=0.5)
    ncmaps = len(color)
    nrows = 8
    for i, k in enumerate(color):
        plt.subplot(nrows, ncmaps // nrows + 1, i + 1)
        plt.axis('off')
        plt.imshow(a, aspect='auto', cmap=getattr(Colormap, k), origin='lower')
        plt.title(k, rotation=90, fontsize=10)
        plt.title(k, fontsize=5)
    file_path=os.path.join(file_dir, file_name) if file_dir else file_name    
    plt.savefig(file_path, dpi=300)
    # plt.savefig('colormaps.png', dpi=300)
    from PIL import Image
    # 读取图像并顺时旋转90度
    img = Image.open(file_path)
    rotated_img = img.rotate(-90, expand=True)
    file_rotated_path=os.path.join(file_dir, f"rotated_{file_name}")if file_dir else  f"rotated_{file_name}"   
    # 保存旋转后的图像
    rotated_img.save(file_rotated_path)
    plt.close()
    return file_path,file_rotated_path

if __name__ == "__main__":
    file1,file2=show_cmaps()
    file1,file2=show_cmaps("D:\\","all_color_maps.png")
    print("done")