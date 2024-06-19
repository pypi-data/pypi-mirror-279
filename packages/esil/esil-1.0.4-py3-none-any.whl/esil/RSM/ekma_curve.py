import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm

def plot_ekma_curve(x, y, values, colors_num=10, title='', x_title='VOCs', y_title='NOx', legend_title='O3', cmap='jet',
                    figsize=None, showplot=True):
    '''
    :param x: numpy 1D array
    :param y: numpy 1D array
    :param values: numpy 2D array,shape[len(x), len(y)]
    :param colors_num: 颜色个数
    :param title: 标题，default：''
    :param x_title: x轴标题,default:'VOCs'
    :param y_title: y轴标题,default:'NOx'
    :param legend_title: 图例标题,default:'O3'
    :param cmap: `matplotlib.colors.Colormap` or str or None, default: jet
        If a `.Colormap` instance, it will be returned. Otherwise, the name of
        a colormap known to Matplotlib, which will be resampled by *lut*. The
        value of None, means :rc:`image.cmap`.
    :param figsize: (float, float), default: :rc:`figure.figsize`
        Width, height in inches.
    :param showplot: 是否绘图，默认绘图；False将返回fig,用于保存
    :return: showplot=True，直接绘图，没有返回值。showplot=False,返回图表数据变量，可直接调用fig.savefig(output_file, dpi=600)进行保存图片。
    '''
    # 创建网格点
    # x_grid, NOx_grid = np.meshgrid(x, y)
    # 设定颜色分界点
    cmap_jet = plt.cm.get_cmap(cmap, colors_num)
    ticks = np.linspace(values.min(), values.max(), colors_num + 1)
    # boundaries = np.linspace(values.min(), values.max(), colors_num + 1)
    norm = BoundaryNorm(ticks, cmap_jet.N)
    # 绘制Ekman曲线
    fig = plt.figure(figsize=figsize)
    contour = plt.contourf(x, y, values, levels=ticks, cmap=cmap_jet, norm=norm)
    contour_lines = plt.contour(x, y, values, levels=contour.levels, colors='black',
                                linestyles='solid', linewidths=1)
    plt.clabel(contour_lines, inline=True, fontsize=8)
    cbar = plt.colorbar(contour, label=legend_title, ticks=ticks, boundaries=ticks)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    # plt.grid(True)
    if showplot:
        # 显示图形
        plt.show()
    else:
        return fig

