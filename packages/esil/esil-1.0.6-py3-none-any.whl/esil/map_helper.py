import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import cartopy.mpl.geoaxes
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import geopandas as gpd
import numpy as np
from esil.panelayout_helper import get_layout_col_row,PaneLayout
import math
#for wrf_out data

# 自定义函数，根据数据的大小选择保留不同位数的小数
def format_data(x):
    if abs(x) > 1000:
        return '{:.0f}'.format(x)  # 大于1000的数据保留0位小数
    elif abs(x) >1 :
        return '{:.2f}'.format(x)  # 大于1的数据保留2位小数
    elif abs(x) < 0.001:
        return '{:.2e}'.format(x)  # 小于0.001的数据保留2位小数，采用科学技术法
    else:
        return '{:.3f}'.format(x)  # 大于0.001小于1的数据保留3位小数

def get_multiple_data(dict_data,dataset_name, variable_name, grid_x, grid_y,grid_concentration,file_name=''):   
    '''
    description: 
    param {dictionary} dict_data,key=dataset_name,value=variable_name,grid_x,grid_y,grid_concentration,file_name,默认为None，会创建一个新的字典
    param {str} dataset_name，数据集名称
    param {str} variable_name, 变量名
    param {numpy array(2D)} grid_x，经度坐标
    param {numpy array(2D)} grid_y，纬度坐标
    param {numpy array(2D)} grid_concentration，浓度值
    param {str} file_name, 数据集所在文件名，default=''
    return {dictionary} dict_data
    '''
    if dict_data is None:
        dict_data = {}
    if dataset_name in dict_data:
        print(f"dataset_name {dataset_name} already exists in dict_data")   
    dict_data[dataset_name] = {
        "file_name": file_name,
        "variable_name": variable_name,
        "grid_x": grid_x,
        "grid_y": grid_y,
        "grid_concentration": grid_concentration
    }    
    return dict_data

def show_multi_maps(dict_data,unit='',cmap='jet', show_lonlat=False,projection=None, boundary_file='',x_title='Longitude', y_title='Latitude',show_minmax=True,
                    default_min_value=-1,default_max_value=-1,panel_layout=None, show_original_grid=False,sharex=True, sharey=True, show_sup_title=False,is_wrf_out_data=False
                    ,points_data=None,fig_size=None,showplot=True,show_grid_line=True,value_format=None):
    '''
    description: 
    @param {dictionary} dict_data,key=dataset_name,value=variable_name,grid_x,grid_y,grid_concentration,file_name,默认为None，会创建一个新的字典
    param {str} dataset_name，数据集名称
    param {str} variable_name, 变量名
    param {numpy array(2D)} grid_x，经度坐标
    param {numpy array(2D)} grid_y，纬度坐标
    param {numpy array(2D)} grid_concentration，浓度值
    param {str} file_name, 数据集所在文件名，default=
    @param {str} unit, 单位
    @param {str} cmap, 颜色映射, default='jet'
    @param {str} projection, 地图投影, default='', 为空时使用PlateCarree投影
    @param {str} boundary_file, 行政边界文件, default='', 为空时不加载行政边界数据
    @param {str} x_title, x轴标题, default='Longitude'
    @param {str} y_title, y轴标题, default='Latitude'
    @param {bool} show_minmax, 是否显示最小最大值, default=True
    @param {float} default_min_value, 最小值, default=-1
    @param {float} default_max_value, 最大值, default=-1
    @param {str} panel_layout, 子图布局, default=None, 为空时自动计算布局
    @param {bool} show_original_grid, 是否显示原始网格, default=False
    @param {bool} sharex, 是否共享x轴, default=True
    @param {bool} sharey, 是否共享y轴, default=True
    @param {bool} show_sup_title, 是否显示共享XY轴标题, default=False
    @param {bool} show_lonlat, 是否显示经纬度
    @param {bool} showplot, 是否显示图形, default=True
    @param {bool} points_data, 是否显示点数据, default=None,示例：{'lon':df_monitor['lon'],'lat':df_monitor['lat'],'value':df_monitor['Monitor_Conc']}
    @param {bool} is_wrf_out_data, 是否是wrf输出数据, default=False
    @param {tuple} fig_size, 图形大小, default=None,示例：width,height=(6,6)
    @param {bool} show_grid_line, 是否显示网格线, default=True
    @param {str} value_format, 数值格式, default=None,示例：'.2f':保留2位小数；'.2e' ：采用科学计数法显示，并保留2位小数
    @return {None or matplotlib.figure} fig
    '''
    # print("")
    # 设置中文字体为系统中已安装的字体，如SimSun（宋体）、SimHei（黑体）
    #plt.rcParams['font.sans-serif'] = ['SimSun']  # 设置中文字体为宋体
    # 设置字体为 Times New Roman
    #plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
    # 创建可视化图
    data_types=dict_data.keys()
    case_num=len(data_types)  
    plot_columns,plot_rows=get_layout_col_row(case_num, panel_layout=panel_layout)
    if projection==None:
        projection = ccrs.PlateCarree()    
    origin_projection = ccrs.PlateCarree()  if is_wrf_out_data else projection 
    width,height =6,6 
    first_key = next(iter(dict_data))    
    height =math.ceil(width*dict_data[first_key]["grid_y"].shape[0]/dict_data[first_key]["grid_x"].shape[0]) if not isinstance( dict_data[first_key]["grid_y"] ,list) else width
    if fig_size!=None:       
        width,height=fig_size
    fig, axs = plt.subplots(plot_rows, plot_columns, figsize=(width * plot_columns, height* plot_rows),
                            subplot_kw={'projection': projection},sharex=sharex, sharey=sharey) 
    if boundary_file:
        reader = Reader(boundary_file)  
    if isinstance(axs, cartopy.mpl.geoaxes.GeoAxesSubplot):
        axs = np.array([axs])
    if show_sup_title==False and plot_rows>1:
        y_titles = [y_title] *plot_rows
        for ax, row in zip(axs[:,0], y_titles):
            ax.set_ylabel(row, rotation=90, size=10)
    # cols = ["LR","SVR","GBRT","DNN"]
    # for ax, col in zip(axs[0,:], cols,):
    #     ax.set_xlabel(col,size=10)
    axs = axs.ravel()  
    # all_grids=np.array([value["grid_concentration"] for data_type,value in dict_data.items()])
    # vmax_all=np.nanpercentile(all_grids,99.5)
    # vmin_all=np.nanpercentile(all_grids,0.5)  
    
    for ax,data_type in zip(axs,data_types):
        dic_sub_data = dict_data[data_type]
        file_name, variable_name, x, y, grid_concentration = dic_sub_data["file_name"], dic_sub_data["variable_name"], dic_sub_data["grid_x"], dic_sub_data["grid_y"], dic_sub_data["grid_concentration"]
        min_value, max_value, mean_value, total_value = np.nanmin(grid_concentration), np.nanmax(grid_concentration), np.nanmean(grid_concentration), np.nansum(grid_concentration)
        ax.text(0.5, 1.07, f'{data_type} {variable_name}', transform=ax.transAxes, fontsize=14, fontweight='bold',ha='center')

        vmax = np.nanpercentile(grid_concentration,99.5) if default_max_value == -1 else default_max_value #np.nanmax(grid_concentration)
        vmin =  np.nanpercentile(grid_concentration,0.5)  if default_min_value == -1 else default_min_value#np.nanmin(grid_concentration)
        if show_original_grid:
            contour = ax.pcolormesh(x, y, grid_concentration, cmap=cmap, vmin=vmin, vmax=vmax,transform=origin_projection)
            # # 绘制填色图
            # contour = ax.imshow(grid_concentration, origin='lower')
        else:
            contour = ax.contourf(x, y, grid_concentration, cmap=cmap,transform=origin_projection, vmin=vmin, vmax=vmax)
        if points_data is not None:  
            ax.scatter(x=points_data["lon"],y=points_data["lat"],s=50,c=points_data["value"],cmap=cmap,transform=origin_projection,vmin=vmin, vmax=vmax, edgecolor='black')      
        # 加载行政边界数据（示例使用shapefile文件）
        if boundary_file:                            
            geometries = reader.geometries()
            enshicity = cfeature.ShapelyFeature(geometries, origin_projection, edgecolor='k',facecolor='none')  # facecolor='none',设置面和线
            #enshicity = cfeature.ShapelyFeature(geometries, ccrs.PlateCarree(), edgecolor='k',facecolor='none')  # facecolor='none',设置面和线
            ax.add_feature(enshicity, linewidth=0.3)  # 添加市界细节  
        else:
            # 添加地图特征
            ax.add_feature(cfeature.COASTLINE, facecolor='none')# '-' 或 'solid'：实线# '--' 或 'dashed'：虚线# ':' 或 'dotted'：点线# '-.' 或 'dashdot'：点划线            
            ax.add_feature(cfeature.BORDERS, linestyle='solid', facecolor='none')
            ax.add_feature(cfeature.LAND, edgecolor='black',facecolor='none')  # facecolor='none'表示边界线围起来区域不填充颜色，只绘制边界线；
            ax.add_feature(cfeature.OCEAN, edgecolor='black', facecolor='none')
        min_longitude ,max_longitude,min_latitude,max_latitude=  round(x.min(),1),round(x.max(),1), round(y.min(),1), round(y.max(),1)       
        mean_or_total='Total' if 'ton' in unit else 'Mean'
        value=total_value if 'ton' in unit else mean_value 
        if is_wrf_out_data:            
            mesh = ax.gridlines(draw_labels=True, linestyle='--', linewidth=0.6, alpha=0.5, x_inline=False, y_inline=False, color='k',visible=show_grid_line)
            mesh.top_labels=False
            mesh.right_labels=False
            mesh.xformatter = LONGITUDE_FORMATTER
            mesh.yformatter = LATITUDE_FORMATTER  
            interval_x =math.ceil((max_longitude - min_longitude) / 10)
            interval_y =math.ceil((max_latitude - min_latitude) / 10)
            mesh.xlocator = mticker.FixedLocator(np.arange(min_longitude,max_longitude,interval_x))
            mesh.ylocator = mticker.FixedLocator(np.arange(min_latitude,max_latitude,interval_y))
            mesh.xlabel_style={'size':10}
            mesh.ylabel_style={'size':10}  
            if show_minmax:                   
                if value_format is not None:
                    # min_max_info= 'Min= {:.2f}, Max= {:.2f}, {:}={:.2f}'.format(min_value, max_value,mean_or_total,value)
                    min_max_info='Min= {}, Max= {}, {}={}'.format(format(min_value, value_format),format(max_value, value_format),mean_or_total,format(value, value_format))
                else:
                    if (mean_value<1000 and mean_value>0.001):                    
                        min_max_info= 'Min= {:.2f}, Max= {:.2f}, {:}={:.2f}'.format(min_value, max_value,mean_or_total,value)
                    else:
                        min_max_info= 'Min= {:.1e}, Max= {:.1e}, {:}={:.1e}'.format(min_value, max_value,mean_or_total,value)              
                ax.text(0.5, 1.02,min_max_info ,transform=ax.transAxes, fontsize=10, fontweight='bold',ha='center') 
        else :                   
            # 设置y轴范围
            ax.set_ylim(min_latitude, max_latitude)
            #print(min(y), max(y))
            # 设置 x 和 y 轴的 ticks 范围
            x_ticks,y_ticks = [],[]
            if max_longitude > 180 and show_lonlat:
                x_ticks = [-180, -120, -60, 0, 60, 120, 180]
            else:
                interval_x =round(float((max_longitude - min_longitude) / 7),2)
                x_ticks =np.round(np.arange(min_longitude, max_longitude + 0.1, interval_x),1)

            interval_y =round(float((max_latitude - min_latitude) / 7),2)
            y_ticks =np.round(np.arange(min_latitude, max_latitude + 0.1, interval_y),1)
            ax.set_xticks(x_ticks)  # 设置 x 轴的 ticks 范围
            ax.set_yticks(y_ticks)  # 设置 y 轴的 ticks 范围         
            # min_value, max_value, mean_value, total_value = np.nanmin(grid_concentration), np.nanmax(grid_concentration), np.nanmean(grid_concentration), np.nansum(grid_concentration)        
            if show_minmax:      
                if value_format is None: 
                    if unit=='ton':  
                        ax.set_xlabel(f"{ '' if show_sup_title else  x_title}\n" + 'Min= {:.2f}, Max= {:.2f}, Total={:.2f}'.format(min_value, max_value,value))
                    else:
                        #min_value, max_value, mean_value 采用科学计数法表示，保留1位小数           
                        ax.set_xlabel(f"{'' if show_sup_title else  x_title}\n"+'Min= {:.1e}, Max= {:.1e}, Mean={:.1e}'.format(min_value, max_value,value))
                else:                    
                    min_max_info='Min= {}, Max= {}, {}={}'.format(format(min_value, value_format),format(max_value, value_format),mean_or_total,format(value, value_format))
                    ax.set_xlabel(f"{'' if show_sup_title else  x_title}\n"+min_max_info)
            else:
                plt.xlabel(x_title)    

    if show_sup_title:
        fig.supxlabel(f'{x_title}',y=0.08,fontsize=15,fontweight="normal")#标签相对于图形的x位置，范围为0到1，默认为0.01，距离底部的距离为0.01，表示留出一小段空白。1表示距离顶部的距离为0
        fig.supylabel(f'{y_title}',x=0.08,fontsize=15,fontweight="normal")  
    plt.subplots_adjust(hspace=0.3)  # 调整子图之间的垂直间距
    # 添加颜色条
    cbar = plt.colorbar(contour, fraction=0.02, pad=0.04, label=f'{unit})',
                        ax=axs, orientation='vertical', shrink=0.7)  # 设置图例高度与图像高度相同, orientation='vertical', shrink=0.7

    cbar.set_label(f'({unit})', fontweight='bold')  # 设置标签字体加粗
   
    if showplot:       
        # 显示图形
        plt.show()
        return fig
    else:
        return fig

def show_delta_maps(dict_data,unit='',cmap='jet', show_lonlat=False,projection=None, boundary_file='',x_title='Longitude', y_title='Latitude',show_minmax=True,
                    default_min_value=-1,default_max_value=-1,panel_layout=None, show_original_grid=False,sharex=True, sharey=True, show_sup_title=False,is_wrf_out_data=False
                    ,points_data=None,delta_map_settings=None,show_dependenct_colorbar=False,showplot=True):
    '''
    description: 
    @param {dictionary} dict_data,key=dataset_name,value=variable_name,grid_x,grid_y,grid_concentration,file_name,默认为None，会创建一个新的字典
    param {str} dataset_name，数据集名称
    param {str} variable_name, 变量名
    param {numpy array(2D)} grid_x，经度坐标
    param {numpy array(2D)} grid_y，纬度坐标
    param {numpy array(2D)} grid_concentration，浓度值
    param {str} file_name, 数据集所在文件名，default=
    @param {str} unit, 单位
    @param {str} cmap, 颜色映射, default='jet'
    @param {str} projection, 地图投影, default='', 为空时使用PlateCarree投影
    @param {str} boundary_file, 行政边界文件, default='', 为空时不加载行政边界数据
    @param {str} x_title, x轴标题, default='Longitude'
    @param {str} y_title, y轴标题, default='Latitude'
    @param {bool} show_minmax, 是否显示最小最大值, default=True
    @param {float} default_min_value, 最小值, default=-1
    @param {float} default_max_value, 最大值, default=-1
    @param {str} panel_layout, 子图布局, default=None, 为空时自动计算布局
    @param {bool} show_original_grid, 是否显示原始网格, default=False
    @param {bool} sharex, 是否共享x轴, default=True
    @param {bool} sharey, 是否共享y轴, default=True
    @param {bool} show_sup_title, 是否显示共享XY轴标题, default=False
    @param {bool} show_lonlat, 是否显示经纬度
    @param {bool} showplot, 是否显示图形, default=True
    @param {bool} points_data, 是否显示点数据, default=None,示例：{'lon':df_monitor['lon'],'lat':df_monitor['lat'],'value':df_monitor['Monitor_Conc']}
    @param {bool} is_wrf_out_data, 是否是wrf输出数据, default=False
    @param {numpy array(2D)} delta_map_settings, 差值图的参数设定，default=None,示例：{'cmap':'coolwarm','default_min_value':-1,'default_max_value':-1}
    @return {None or matplotlib.figure} fig
    '''
    # print("")
    # 设置中文字体为系统中已安装的字体，如SimSun（宋体）、SimHei（黑体）
    #plt.rcParams['font.sans-serif'] = ['Arial']  # 设置中文字体为宋体
    # 设置字体为 Times New Roman
    #plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
    # 创建可视化图
    data_types=dict_data.keys()
    case_num=len(data_types)  
    plot_columns,plot_rows=get_layout_col_row(case_num, panel_layout=panel_layout)
    if projection==None:
        projection = ccrs.PlateCarree()    
    origin_projection = ccrs.PlateCarree()  if is_wrf_out_data else projection 
    width = 6
    first_key = next(iter(dict_data))    
    height =math.ceil(width*dict_data[first_key]["grid_y"].shape[0]/dict_data[first_key]["grid_x"].shape[0]) if not isinstance( dict_data[first_key]["grid_y"] ,list) else width
    fig, axs = plt.subplots(plot_rows, plot_columns, figsize=(width * plot_columns, height* plot_rows),
                            subplot_kw={'projection': projection},sharex=sharex, sharey=sharey) 
    if boundary_file:
        reader = Reader(boundary_file)  
    if isinstance(axs, cartopy.mpl.geoaxes.GeoAxesSubplot):
        axs = np.array([axs])
    if show_sup_title==False and plot_rows>1:
        y_titles = [y_title] *plot_rows
        for ax, row in zip(axs[:,0], y_titles):
            ax.set_ylabel(row, rotation=90, size=10)
    # cols = ["LR","SVR","GBRT","DNN"]
    # for ax, col in zip(axs[0,:], cols,):
    #     ax.set_xlabel(col,size=10)
    axs = axs.ravel()  
    for ax,data_type in zip(axs,data_types):
        dic_sub_data = dict_data[data_type]
        file_name, variable_name, x, y, grid_concentration = dic_sub_data["file_name"], dic_sub_data["variable_name"], dic_sub_data["grid_x"], dic_sub_data["grid_y"], dic_sub_data["grid_concentration"]
        min_value, max_value, mean_value, total_value = np.nanmin(grid_concentration), np.nanmax(grid_concentration), np.nanmean(grid_concentration), np.nansum(grid_concentration)
        ax.text(0.5, 1.07, f'{data_type} {variable_name}', transform=ax.transAxes, fontsize=14, fontweight='bold',ha='center')

        vmax = np.nanpercentile(grid_concentration,99.5) if default_max_value == -1 else default_max_value
        vmin = np.nanpercentile(grid_concentration,0.5) if default_min_value == -1 else default_min_value
        if 'delta' in str.lower(data_type) or 'delta' in str.lower(file_name):
            cmap_delta,default_delta_vmin,default_delta_vmax= delta_map_settings["cmap"],delta_map_settings["default_min_value"],delta_map_settings["default_max_value"]
            vmax_delta =np.nanpercentile(grid_concentration,99.5) if default_delta_vmax == -1 else default_delta_vmax
            vmin_delta =np.nanpercentile(grid_concentration,0.5) if default_delta_vmin == -1 else default_delta_vmin           
            max_value_delta=np.max([abs(vmax_delta),abs(vmin_delta)])            
            vmin_delta,vmax_delta=-max_value_delta,max_value_delta
            if show_original_grid:                
                contour = ax.pcolormesh(x, y, grid_concentration, cmap=cmap_delta, vmin=vmin_delta, vmax=vmax_delta,transform=origin_projection)           
            else:
                contour = ax.contourf(x, y, grid_concentration, cmap=cmap_delta,transform=origin_projection,  vmin=vmin_delta, vmax=vmax_delta)
            # 添加colorbar到当前子图
            cbar = plt.colorbar(contour, ax=ax,shrink=0.6)
            cbar.set_label(f'({unit})', fontweight='bold')  # 设置标签字体加粗
        else:
            if show_original_grid:
                contour = ax.pcolormesh(x, y, grid_concentration, cmap=cmap, vmin=vmin, vmax=vmax,transform=origin_projection)              
            else:
                contour = ax.contourf(x, y, grid_concentration, cmap=cmap,transform=origin_projection, vmin=vmin, vmax=vmax)
            if show_dependenct_colorbar:
                cbar = plt.colorbar(contour, ax=ax,shrink=0.6)
                cbar.set_label(f'({unit})', fontweight='bold')  # 设置标签字体加粗
        if points_data is not None:  
            ax.scatter(x=points_data["lon"],y=points_data["lat"],s=50,c=points_data["value"],cmap=cmap,transform=origin_projection,vmin=vmin, vmax=vmax, edgecolor='black')      
        # 加载行政边界数据（示例使用shapefile文件）
        if boundary_file:                            
            geometries = reader.geometries()
            enshicity = cfeature.ShapelyFeature(geometries, origin_projection, edgecolor='k',facecolor='none')  # facecolor='none',设置面和线
            #enshicity = cfeature.ShapelyFeature(geometries, ccrs.PlateCarree(), edgecolor='k',facecolor='none')  # facecolor='none',设置面和线
            ax.add_feature(enshicity, linewidth=0.3)  # 添加市界细节  
        else:
            # 添加地图特征
            ax.add_feature(cfeature.COASTLINE, facecolor='none')# '-' 或 'solid'：实线# '--' 或 'dashed'：虚线# ':' 或 'dotted'：点线# '-.' 或 'dashdot'：点划线            
            ax.add_feature(cfeature.BORDERS, linestyle='solid', facecolor='none')
            ax.add_feature(cfeature.LAND, edgecolor='black',facecolor='none')  # facecolor='none'表示边界线围起来区域不填充颜色，只绘制边界线；
            ax.add_feature(cfeature.OCEAN, edgecolor='black', facecolor='none')
        min_longitude ,max_longitude,min_latitude,max_latitude=  round(x.min(),1),round(x.max(),1), round(y.min(),1), round(y.max(),1)       
        if is_wrf_out_data:            
            mesh = ax.gridlines(draw_labels=True, linestyle='--', linewidth=0.6, alpha=0.5, x_inline=False, y_inline=False, color='k')
            mesh.top_labels=False
            mesh.right_labels=False
            mesh.xformatter = LONGITUDE_FORMATTER
            mesh.yformatter = LATITUDE_FORMATTER  
            # mesh.xlocator = mticker.FixedLocator(np.arange(min_longitude,max_longitude,1))
            # mesh.ylocator = mticker.FixedLocator(np.arange(min_latitude,max_latitude,1))
            interval_x =math.ceil((max_longitude - min_longitude) / 10)
            interval_y =math.ceil((max_latitude - min_latitude) / 10)
            mesh.xlocator = mticker.FixedLocator(np.arange(min_longitude,max_longitude,interval_x))
            mesh.ylocator = mticker.FixedLocator(np.arange(min_latitude,max_latitude,interval_y))
            mesh.xlabel_style={'size':10}
            mesh.ylabel_style={'size':10}  
            if show_minmax:
                mean_or_total='Total' if 'ton' in unit else 'Mean'
                value=total_value if 'ton' in unit else mean_value            
                if (abs(mean_value)<2000 and abs(mean_value)>0.001):
                    min_max_info= 'Min= {:.2f}, Max= {:.2f}, {:}={:.2f}'.format(min_value, max_value,mean_or_total,value)
                else:
                    min_max_info= 'Min= {:.1e}, Max= {:.1e}, {:}={:.1e}'.format(min_value, max_value,mean_or_total,value)              
                ax.text(0.5, 1.02,min_max_info ,transform=ax.transAxes, fontsize=9,ha='center') #, fontweight='bold'
        else :                   
            # 设置y轴范围
            ax.set_ylim(min_latitude, max_latitude)
            #print(min(y), max(y))
            # 设置 x 和 y 轴的 ticks 范围
            x_ticks,y_ticks = [],[]
            if max_longitude > 180 and show_lonlat:
                x_ticks = [-180, -120, -60, 0, 60, 120, 180]
            else:
                interval_x =round(float((max_longitude - min_longitude) / 7),2)
                x_ticks =np.round(np.arange(min_longitude, max_longitude + 0.1, interval_x),1)

            interval_y =round(float((max_latitude - min_latitude) / 7),2)
            y_ticks =np.round(np.arange(min_latitude, max_latitude + 0.1, interval_y),1)
            ax.set_xticks(x_ticks)  # 设置 x 轴的 ticks 范围
            ax.set_yticks(y_ticks)  # 设置 y 轴的 ticks 范围         
            # min_value, max_value, mean_value, total_value = np.nanmin(grid_concentration), np.nanmax(grid_concentration), np.nanmean(grid_concentration), np.nansum(grid_concentration)        
            if show_minmax:                
                if unit=='ton':              
                    ax.set_xlabel(f"{ '' if show_sup_title else  x_title}\n" + 'Min= {:.2f}, Max= {:.2f}, Total={:.2f}'.format(min_value, max_value,total_value))
                else:
                    #min_value, max_value, mean_value 采用科学计数法表示，保留1位小数           
                    ax.set_xlabel(f"{'' if show_sup_title else  x_title}\n"+'Min= {:.1e}, Max= {:.1e}, Mean={:.1e}'.format(min_value, max_value,mean_value))
            else:
                plt.xlabel(x_title)    

    if show_sup_title:
        fig.supxlabel(f'{x_title}',y=0.08,fontsize=15,fontweight="normal")#标签相对于图形的x位置，范围为0到1，默认为0.01，距离底部的距离为0.01，表示留出一小段空白。1表示距离顶部的距离为0
        fig.supylabel(f'{y_title}',x=0.08,fontsize=15,fontweight="normal")  
    plt.subplots_adjust(hspace=0.3)  # 调整子图之间的垂直间距
    if not show_dependenct_colorbar and 'delta' not in data_type:
        # 添加颜色条
        cbar = plt.colorbar(contour, fraction=0.02, pad=0.04, label=f'{unit})',
                            ax=axs, orientation='vertical', shrink=0.7)  # 设置图例高度与图像高度相同, orientation='vertical', shrink=0.7

        cbar.set_label(f'({unit})', fontweight='bold')  # 设置标签字体加粗
   
    if showplot:       
        # 显示图形
        plt.show()
        return fig
    else:
        return fig

def show_single_map(grid_x, grid_y, grid_concentration, title='', x_title='Longitude', y_title='Latitude', unit='', boundary_file='',cmap='jet',figsize=None, show_minmax=True,default_min_value=-1,default_max_value=-1, show_original_grid=False,showplot=True):
    '''
     :param grid_x:list of ndarrays, 通常np.meshgrid后结果
     :param grid_y:list of ndarrays, 通常np.meshgrid后结果
     :param grid_concentration:list of ndarrays，需要展示的网格化数据
     :param title:标题名称
     :param x_title:x轴标题
     :param y_title:y轴标题
     :param unit:数据单位
     :param boundary_file:边界线路径，如设定路径，则会在现有数据基础上追加边界线
     :param show_minmax:是否显示最大最小值，默认显示
     :param showplot:是否绘图，默认绘图；False将返回fig,用于保存
     :return:showplot=True，直接绘图，没有返回值。showplot=False,返回图表数据变量，可直接调用fig.savefig(output_file, dpi=600)进行保存图片。
    '''
    # 创建可视化图
    fig = plt.figure(figsize=figsize)#figsize=(10, 5)
    # 创建一个地图投影
    ax = plt.axes(projection=ccrs.PlateCarree())
    title_text = ax.text(0.5, 1.05, f'{title} ', transform=ax.transAxes, fontsize=12, ha='center')

    # 添加地图特征
    ax.add_feature(cfeature.COASTLINE, facecolor='none')
    # '-' 或 'solid'：实线    #'--' 或 'dashed'：虚线    #':' 或 'dotted'：点线    #'-.' 或 'dashdot'：点划线
    ax.add_feature(cfeature.BORDERS, linestyle='solid', facecolor='none')
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='none')  # facecolor='none'表示边界线围起来区域不填充颜色，只绘制边界线；
    ax.add_feature(cfeature.OCEAN, edgecolor='black', facecolor='none')

    max_value = np.nanmax(grid_concentration) if default_max_value==-1 else default_max_value
    min_value = np.nanmin(grid_concentration) if default_min_value==-1 else default_min_value
    
    # data_subset.lon 和 data_subset.lat 是一维数组，data_subset 是对应的二维浓度数据
    # contour = ax.contourf(data_subset.lon, data_subset.lat, data_subset, cmap='jet', transform=ccrs.PlateCarree())#展示选定范围cmap='viridis',coolwarm
    # contour = ax.contourf(grid_x, grid_y, grid_concentration, cmap='viridis')  # 使用插值后的数据绘制等高线填充图
    if show_original_grid:
        contour =ax.pcolormesh(grid_x, grid_y, grid_concentration,cmap=cmap,vmin=min_value, vmax=max_value)
    else:        
        contour = ax.contourf(grid_x, grid_y, grid_concentration, cmap=cmap,
                              transform=ccrs.PlateCarree(), vmin=min_value, vmax=max_value)  # 展示选定范围cmap='viridis',coolwarm
    
    # 加载行政边界数据（示例使用shapefile文件）
    if boundary_file:
        boundaries = gpd.read_file(boundary_file)
        boundaries.boundary.plot(color='black', linewidth=0.8, ax=plt.gca())  # 添加行政边界线

    # 添加颜色条
    if unit:unit=f'({unit})'
    cbar = plt.colorbar(contour, fraction=0.02, pad=0.04, label=f'{unit}',
                        ax=ax)  # 设置图例高度与图像高度相同, orientation='vertical', shrink=0.7

    # 设置y轴范围
    ax.set_ylim(grid_y.min(), grid_y.max())#max(values) 是 Python 内置的函数，用于找到给定可迭代对象（例如列表、元组等）中的最大值。values.max() 是 NumPy 数组对象的方法，用于计算 NumPy 数组中元素的最大值。
    max_longitude=grid_x.max()
    min_longitude=grid_x.min()
    max_latitude=grid_y.max()
    min_latitude =grid_y.min()
    # 设置 x 和 y 轴的 ticks 范围
    x_ticks = [-180, -120, -60, 0, 60, 120, 180]
    y_ticks = [-90, -60, -30, 0, 30, 60, 90]
    if max_longitude > 180:
        x_ticks = [-180, -120, -60, 0, 60, 120, 180]
    else:
        interval_x = int((max_longitude - min_longitude) / 7)
        x_ticks = np.arange(min_longitude, max_longitude + 0.1*interval_x, interval_x)

    interval_y = int((max_latitude - min_latitude) / 7)
    y_ticks = np.arange(min_latitude, max_latitude + 0.1*interval_y, interval_y)
    ax.set_xticks(x_ticks)  # 设置 x 轴的 ticks 范围
    ax.set_yticks(y_ticks)  # 设置 y 轴的 ticks 范围

    # 添加标题和标签
    plt.ylabel(y_title)
    # 在x轴标题下方添加一行显示最大值和最小值
    if show_minmax:
        plt.xlabel(x_title+f"\nMin= {format_data(min_value)}, Max= {format_data(np.nanmax(grid_concentration))}, Total= {format_data(np.nansum(grid_concentration))}")
        print(title+f"\nMin= {format_data(min_value)}, Max= {format_data(np.nanmax(grid_concentration))}, Total= {format_data(np.nansum(grid_concentration))}")
    else:
        plt.xlabel(x_title)
    if showplot:
        # 显示图形
        plt.show()
    else:
        return fig

def plot_cmaq_concentration_maps(dic_grid_values, model_property,unit='',cmap='jet', show_lonlat=False, boundary_file='',x_title='Longitude', y_title='Latitude',show_minmax=True,default_min_value=-1,default_max_value=-1, panel_layout=PaneLayout.SquareColPreferred, show_original_grid=False, showplot=True):
    '''
    @description: 绘制CMAQ浓度图
    @param {type} dic_grid_values: 字典，包含不同时间的不同变量的网格化数据
    @param {type} model_property: 模型属性对象，包含模型的属性信息，如行数、列数、经纬度范围等
    @param {type} unit: 单位
    @param {type} cmap: 颜色映射
    @param {type} show_lonlat: 是否显示经纬度
    @param {type} boundary_file: 边界文件路径
    @param {type} x_title: x轴标题
    @param {type} y_title: y轴标题
    @param {type} show_minmax: 是否显示最大最小值
    @param {type} default_min_value: 默认最小值
    @param {type} default_max_value: 默认最大值
    @param {type} panel_layout: 子图布局
    @param {type} show_original_grid: 是否显示原始网格
    @param {type} showplot: 是否显示图形
    @return: fig
    '''
    cols,rows = model_property.cols,model_property.rows
    x,y = [],[]
    # x_lable,y_lable='Longitude','Latitude'
    projection = ccrs.PlateCarree()
    if show_lonlat:
        lon_start, lat_start, lon_end, lat_end = model_property.lon_start,model_property.lat_start,model_property.lon_end,model_property.lat_end
        x = np.linspace(lon_start, lon_end, cols)
        y = np.linspace(lat_start, lat_end, rows)
    else:
        x = np.linspace(1, cols, cols)
        y = np.linspace(1, rows, rows)
        # x_lable, y_lable = 'Column', 'Row'
        # 创建 Lambert 投影对象
        #projection = ccrs.LambertConformal(central_longitude=112, central_latitude=30,standard_parallels=(25, 40))
        projection =model_property.projection #ccrs.CRS(model_property.proj4_string)# ccrs.Projection(model_property.proj4_string)

    # Define the latitude and longitude ranges you want to display
    min_longitude = x.min()
    max_longitude = x.max()
    min_latitude = y.min()
    max_latitude = y.max()
    # 定义要显示的经纬度范围
    lon_range = slice(min_longitude, max_longitude)  # 替换为您的经度范围
    lat_range = slice(min_latitude, max_latitude)  # 替换为您的纬度范围
    # 设置中文字体为系统中已安装的字体，如SimSun（宋体）、SimHei（黑体）
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 设置中文字体为宋体
    # 设置字体为 Times New Roman
    plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
    # 创建可视化图
    case_list = list(dic_grid_values.keys())
    plot_rows = len(case_list)
    plot_columns = len(dic_grid_values[case_list[0]])    
    
    # fig, axs = plt.figure(1,columns,figsize=(12, 5))
    fig, axs = plt.subplots(plot_rows, plot_columns, figsize=(6 * plot_columns, 6 * plot_rows),
                            subplot_kw={'projection': projection})

    if boundary_file:
        reader = Reader(boundary_file)
        #geometries = reader.geometries()
    row_index = 0
    for date, dic_data in dic_grid_values.items():
        col_index = 0
        for variable_name, data in dic_data.items():
            if plot_rows>1 and plot_columns>1:
                ax = axs[row_index, col_index]
            elif plot_rows==1 and plot_columns>1:
                ax = axs[col_index]
            else:
                ax = axs[row_index]               
       
            # Use .sel() to select the specific latitude and longitude range
            #data_subset =data# data.sel(lon=slice(min_longitude, max_longitude), lat=slice(min_latitude, max_latitude))
            # 创建一个地图投影
            # ax = plt.axes(projection=ccrs.PlateCarree())
            title_text = ax.text(0.5, 1.05, f'{date}-{variable_name} ', transform=ax.transAxes, fontsize=16, fontweight='bold',ha='center')

            vmax = np.nanmax(data) if default_max_value == -1 else default_max_value
            vmin = np.nanmin(data) if default_min_value == -1 else default_min_value
            if show_original_grid:
                contour = ax.pcolormesh(x, y, data, cmap=cmap, vmin=vmin, vmax=vmax,transform=projection)
            else:
                contour = ax.contourf(x, y, data, cmap=cmap,
                                      transform=projection, vmin=vmin, vmax=vmax)
                
            #contour = ax.contourf(x, y, data, cmap='jet',                                  transform=projection)  # 展示选定范围cmap='viridis',coolwarm
            # 加载行政边界数据（示例使用shapefile文件）
            if boundary_file:
                #reader = Reader(boundary_file)
                geometries = reader.geometries()
                enshicity = cfeature.ShapelyFeature(geometries, projection, edgecolor='k',
                                                 facecolor='none')  # facecolor='none',设置面和线
                ax.add_feature(enshicity, linewidth=0.3)  # 添加市界细节
            else:
                # 添加地图特征
                ax.add_feature(cfeature.COASTLINE, facecolor='none')
                # '-' 或 'solid'：实线            # '--' 或 'dashed'：虚线            # ':' 或 'dotted'：点线            # '-.' 或 'dashdot'：点划线
                ax.add_feature(cfeature.BORDERS, linestyle='solid', facecolor='none')
                ax.add_feature(cfeature.LAND, edgecolor='black',
                               facecolor='none')  # facecolor='none'表示边界线围起来区域不填充颜色，只绘制边界线；
                ax.add_feature(cfeature.OCEAN, edgecolor='black', facecolor='none')
            # 设置y轴范围
            ax.set_ylim(min(y), max(y))
            #print(min(y), max(y))
            # 设置 x 和 y 轴的 ticks 范围
            x_ticks,y_ticks = [],[]
            if max_longitude > 180 and show_lonlat:
                x_ticks = [-180, -120, -60, 0, 60, 120, 180]
            else:
                interval_x =round(float((max_longitude - min_longitude) / 7),2)
                x_ticks =np.round(np.arange(min_longitude, max_longitude + 0.1, interval_x),2)

            interval_y =round(float((max_latitude - min_latitude) / 7),2)
            y_ticks =np.round(np.arange(min_latitude, max_latitude + 0.1, interval_y),2)
            ax.set_xticks(x_ticks)  # 设置 x 轴的 ticks 范围
            ax.set_yticks(y_ticks)  # 设置 y 轴的 ticks 范围
            # 在x轴标题下方添加一行显示最大值和最小值
            max_value = data.max().values
            min_value = data.min().values
            
            if show_minmax:                
                if unit=='ton':
                    ax.set_xlabel(f'{x_title}' + '\n\nMin= {:.2f}, Max= {:.2f}, Total={:.2f}'.format(min_value, max_value,np.nansum(data.values)))
                else:
                    #min_value, max_value, mean_value 采用科学计数法表示，保留1位小数
                    ax.set_xlabel(f'{x_title}'+'\n\nMin= {:.1e}, Max= {:.1e}, Mean={:.1e}'.format(min_value, max_value,np.nanmean(data.values)))
            else:
                plt.xlabel(x_title)
            #ax.set_xlabel(f'{x_title}'+'\n\nMin= {:.2f}, Max= {:.2f}'.format(min_value, max_value), fontweight='bold')
            # 添加标题和标签
            if col_index == 0:
                ax.set_ylabel(f'{y_title}', fontweight='bold')
            col_index = col_index + 1
        row_index = row_index + 1
    # 添加颜色条
    cbar = plt.colorbar(contour, fraction=0.02, pad=0.04, label=f'{unit})',
                        ax=axs, orientation='vertical', shrink=0.7)  # 设置图例高度与图像高度相同, orientation='vertical', shrink=0.7

    cbar.set_label(f'({unit})', fontweight='bold')  # 设置标签字体加粗
    if showplot:
        # 显示图形
        plt.show()
        return fig
    else:
        return fig
    
def get_bc_whole_domain_data(bc_file,variable_name,time_name='TSTEP',layer_name='LAY',specified_time_step=None,specified_layer_step=None,show_lonlat=False):
    '''
    @description: 获取boundary condition文件中的全域数据
    @param {str} boundary_file, 行政边界文件
    @param {str} variable_name, 变量名
    @param {time_name} time_name, 时间变量名, default='TSTEP'
    @param {layer_name} layer_name, 层变量名, default='LAY'
    @param {int} specified_time_step, 指定时间步长索引, default=None，为None时获取所有时间步长
    @param {int} specified_layer_step, 指定层步长索引, default=None, 为None时获取所有层步长
    @param {bool} show_lonlat, 是否返回经纬度信息，默认为False
    @return {tuple} grid,x,y,projection,unit: 网格数据， x,y坐标,投影,单位
    '''
    from esil.RSM.Model_Property import model_attribute  
    import xarray as xr
    model = model_attribute(bc_file)
    ds = xr.open_dataset(bc_file, decode_times=False)
    if hasattr(ds[variable_name], 'units'):
        unit = ds[variable_name].units.strip()
    time_step_count = ds[time_name].size
    layer_count = ds[layer_name].size
    if specified_time_step is not None:
        time_step_count = 1
    if specified_layer_step is not None:
        layer_count = 1
    grid = np.full((time_step_count,layer_count,model.rows,model.cols), np.nan)
    dict_grid_index = {}
    for time_index in range(ds[time_name].size):
        if specified_time_step is not None and time_index != specified_time_step:
            continue        
        print(f"Processing time_index={time_index}")
        for layer_index in range(ds[layer_name].size): 
            if specified_layer_step is not None and layer_index != specified_layer_step:
                continue           
            for row_index,y in enumerate(model.y_coords):
                for col_index,x in enumerate(model.x_coords):                   
                    if dict_grid_index.get((row_index,col_index)) is None:   
                        idx = np.where((model.x_coords_bc == x) & (model.y_coords_bc == y))    # 搜索给定经纬度的索引                 
                        dict_grid_index[(row_index,col_index)] = idx
                    else:
                        idx = dict_grid_index.get((row_index,col_index))
                    if idx[0].size > 0:                        
                        # target_concentration = ds[variable_name][time_index,layer_index,:].values[idx]
                        grid[time_index,layer_index,row_index,col_index] = ds[variable_name][time_index,layer_index,:].values[idx]
                        #print(f'row_index={row_index},col_index={col_index},idx={idx}')
    x,y=model.get_xy_coordinates(show_lonlat=show_lonlat)                
    return grid,x,y,model.projection,unit

def plot_stacked_bar_on_map(data, title='', x_title='Longitude', y_title='Latitude', unit='', boundary_file='', cmap='jet', figsize=None, show_minmax=True, showplot=True):
    '''
    @description: 在地图上绘制堆叠条形图
    @param {dict} data, 数据字典，key=AreaID, value={label: value}
    @param {str} title, 标题
    @param {str} x_title, x轴标题
    @param {str} y_title, y轴标题
    @param {str} unit, 单位
    @param {str} boundary_file, 行政边界文件
    @param {str} cmap, 颜色映射
    @param {tuple} figsize, 图形尺寸
    @param {bool} show_minmax, 是否显示最小最大值
    @param {bool} showplot, 是否显示图形
    @return {matplotlib.figure.Figure} fig, 图形对象  
    '''
    # Load administrative boundary data
    gdf = gpd.read_file(boundary_file)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot administrative boundaries
    gdf.boundary.plot(ax=ax, linewidth=1.0, color='black')

    # Get centroids of each area
    gdf['centroid'] = gdf['geometry'].centroid

    # Define colors for labels
    label_color_dict = {}

    # Initialize bottom values for stacking bars
    bottom_values = {label: [0] * len(gdf) for label in data[list(data.keys())[0]]}

    # Iterate over each area to plot stacked bar charts
    for idx, row in gdf.iterrows():
        x, y = row['centroid'].x, row['centroid'].y
        key = row['AreaID']
        data_values = data.get(key, {})  # Use .get() method to handle missing keys gracefully
        if not data_values:
            continue
        for label, value in data_values.items():
            if label not in label_color_dict:
                label_color_dict[label] = next(ax._get_lines.prop_cycler)['color']
            ax.bar(key, value, color=label_color_dict[label], bottom=bottom_values[label], alpha=1)
            bottom_values[label] = [sum(x) for x in zip(bottom_values[label], [value])]

    # Create legend
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, label=label)
                      for label, color in label_color_dict.items()]
    plt.legend(handles=legend_handles, loc='upper right')

    # Set x and y axis limits
    ax.set_xlim(gdf.total_bounds[0], gdf.total_bounds[2])
    ax.set_ylim(gdf.total_bounds[1], gdf.total_bounds[3])

    # Set titles and labels
    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)

    # Show plot if specified
    if showplot:
        plt.show()
        
def plot_bar_on_map(data, title='', x_title='Longitude', y_title='Latitude', unit='', boundary_file='', cmap='jet', figsize=None, show_minmax=True, showplot=True):
    '''
    @description: 在地图上绘制条形图
    @param {dict} data, 数据字典，key=AreaID, value={label: value}
    @param {str} title, 标题
    @param {str} x_title, x轴标题
    @param {str} y_title, y轴标题
    @param {str} unit, 单位
    @param {str} boundary_file, 行政边界文件
    @param {str} cmap, 颜色映射
    @param {tuple} figsize, 图形尺寸
    @param {bool} show_minmax, 是否显示最小最大值
    @param {bool} showplot, 是否显示图形
    @return {matplotlib.figure.Figure} fig, 图形对象     
    '''
    # Load administrative boundary data
    gdf = gpd.read_file(boundary_file)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot administrative boundaries
    gdf.boundary.plot(ax=ax, linewidth=1.0, color='black')

    # Get centroids of each area
    gdf['centroid'] = gdf['geometry'].centroid

    # Define colors for labels
    label_color_dict = {}

    # Iterate over each area to plot bar charts
    for idx, row in gdf.iterrows():
        x, y = row['centroid'].x, row['centroid'].y
        key = row['AreaID']
        data_values = data.get(key, {})  # Use .get() method to handle missing keys gracefully
        if not data_values:
            continue
        for label in data_values:
            if label not in label_color_dict:
                label_color_dict[label] = next(ax._get_lines.prop_cycler)['color']

        values = list(data_values.values())  # Values for bar heights
        labels = list(data_values.keys())   # Labels for bars
        colors = [label_color_dict[label] for label in labels]

        # Plot bar chart
        ax.bar(x,labels, values, color=colors, alpha=0.7)
    
    # Create legend
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, label=label)
                      for label, color in label_color_dict.items()]
    plt.legend(handles=legend_handles, loc='upper right')

    # Set x and y axis limits
    ax.set_xlim(gdf.total_bounds[0], gdf.total_bounds[2])
    ax.set_ylim(gdf.total_bounds[1], gdf.total_bounds[3])

    # Set titles and labels
    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)

    # Show plot if specified
    if showplot:
        plt.show()
        
def plot_pie1_on_map(data, title='', x_title='Longitude', y_title='Latitude', unit='', boundary_file='', cmap='jet', figsize=None, show_minmax=True, showplot=True):
    '''
    @description: 在地图上绘制饼图
    @param {dict} data, 数据字典，key=AreaID, value={label: value}
    @param {str} title, 标题
    @param {str} x_title, x轴标题
    @param {str} y_title, y轴标题
    @param {str} unit, 单位
    @param {str} boundary_file, 行政边界文件
    @param {str} cmap, 颜色映射
    @param {tuple} figsize, 图形尺寸
    @param {bool} show_minmax, 是否显示最小最大值
    @param {bool} showplot, 是否显示图形
    @return {matplotlib.figure.Figure} fig, 图形对象     
    '''
    # Load administrative boundary data
    
    gdf = gpd.read_file(boundary_file)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot administrative boundaries
    gdf.boundary.plot(ax=ax, linewidth=1.0, color='black')

    # Get centroids of each area
    gdf['centroid'] = gdf['geometry'].centroid

    # Define colors for labels
    label_color_dict = {}

    # Iterate over each area to plot pie charts
    for idx, row in gdf.iterrows():
        x, y = row['centroid'].x, row['centroid'].y
        key = row['AreaID']
        data_values = data.get(key, {})  # Use .get() method to handle missing keys gracefully
        if not data_values:
            continue
        for label in data_values:
            if label not in label_color_dict:
                label_color_dict[label] = next(ax._get_lines.prop_cycler)['color']

        sizes = list(data_values.values())  # Values for pie chart slices
        labels = list(data_values.keys())   # Labels for pie chart slices
        colors = [label_color_dict[label] for label in labels]

        # Plot pie chart
        ax.pie(sizes, colors=colors, labels=None, startangle=90, radius=0.1, center=(x, y))

    # Create legend
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, label=label)
                      for label, color in label_color_dict.items()]
    plt.legend(handles=legend_handles, loc='upper right')

    # Set x and y axis limits
    ax.set_xlim(gdf.total_bounds[0], gdf.total_bounds[2])
    ax.set_ylim(gdf.total_bounds[1], gdf.total_bounds[3])

    # Set titles and labels
    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)

    # Show plot if specified
    if showplot:
        plt.show()

def plot_pie_on_map(data,title='', x_title='Longitude', y_title='Latitude', unit='', boundary_file='',cmap='jet',figsize=None, show_minmax=True, showplot=True):
    '''
    @description: 在地图上绘制饼图
    @param {dict} data, 数据字典，key=AreaID, value={label: value}
    @param {str} title, 标题
    @param {str} x_title, x轴标题
    @param {str} y_title, y轴标题
    @param {str} unit, 单位
    @param {str} boundary_file, 行政边界文件
    @param {str} cmap, 颜色映射
    @param {tuple} figsize, 图形尺寸
    @param {bool} show_minmax, 是否显示最小最大值
    @param {bool} showplot, 是否显示图形
    @return {matplotlib.figure.Figure} fig, 图形对象    
    '''    
    # 加载行政边界数据（示例使用shapefile文件）
    gdf = gpd.read_file(boundary_file)
    # 创建一个图形和子图
    fig, ax = plt.subplots(figsize=(12, 8))
    # 去除行政区域的颜色，并保留边界线
    gdf.boundary.plot(ax=ax, linewidth=1.0, color='black')
    # 获取每个区域的几何中心坐标
    gdf['centroid'] = gdf['geometry'].centroid
    # 统计所有区域数据中出现的标签和它们的颜色
    label_color_dict = {}
    # 遍历每个区域的中心坐标，绘制饼图
    for idx, row in gdf.iterrows():
        x, y = row['centroid'].x, row['centroid'].y
        key=row['AreaID']
        data_values=data[key]
        #data_values = row['data_column']  # 从数据列中获取用于绘制饼图的数据
        if not data_values:  # 如果数据为空，跳过绘制饼图
            continue
        for label in data_values:
            if label not in label_color_dict:
                label_color_dict[label] = next(ax._get_lines.prop_cycler)['color']

    # 遍历每个区域的中心坐标，绘制饼图
    for idx, row in gdf.iterrows():
        x, y = row['centroid'].x, row['centroid'].y
        key = row['AreaID']
        data_values = data[key]
        if not data_values:  # 如果数据为空，跳过绘制饼图
            continue
        sizes = [value for value in data_values.values()]  # 饼图分块的大小
        labels = [key for key in data_values.keys()]  # 饼图分块的标签
        colors = [label_color_dict[label] for label in labels]  # 使用预先定义的颜色
        ax.pie(sizes, colors=colors, labels=None, startangle=90, radius=0.1, center=(x, y))

    # 创建图例
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, label=label)
                      for label, color in label_color_dict.items()]
    plt.legend(handles=legend_handles, loc='upper right')

    # 设置 x 和 y 轴的范围
    ax.set_xlim(gdf.total_bounds[0], gdf.total_bounds[2])
    ax.set_ylim(gdf.total_bounds[1], gdf.total_bounds[3])
    # 设置标题和标签等其他绘图参数
    ax.set_title('Pie Charts on Map')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
   #ax.grid(True)

    plt.show()


if __name__=="__main__":
    import math
    import os
    from esil.file_helper import get_files
    from esil.netcdf_helper import get_extent_data
    from esil.earth_helper import get_m2
    from esil.RSM.Model_Property import model_attribute   
  

    extent =[]
    china_extent = [70.25, 136.25, 10.125, 55.25]     
    guangdong_extent=[109.5, 117.5, 19, 27]    
    #extent=guangdong_extent
    boundary_file=''    
    json_file=r'D:\Devin\MyTestDemo\PythonDemo\NetcdfReader\CO2 Visualization\100000.json' 
    unit='ton'
    unit='mol/m2/s'
    default_max_value=10*math.pow(10,6) if unit=='ton' else 30*math.pow(10,-7)
    default_min_value=0 if unit=='ton' else -30*math.pow(10,-7)    
    dict_data={}
    ###开始：绘制SCUT.GLOBAL.fluxBIO.BAYES数据的示例   
    
    # nc_file=r'E:\CO2\CarbonTracker\CT2022.flux1x1.202001.nc'   
    # variable_name = 'bio_posterior'  
    # longitude_name='lon'
    # latitude_name='lat'  
    # cmap='seismic'
    # # 获取目录中的所有文件
    # file_path=r'E:\CO2\data\emis\posterior emission\SCUT_GLOBAL_FLUX\ENKF_Conc'
    # files = get_files(file_path,recursive=False,)
    # variable_name='xco2' if 'Conc' in file_path else variable_name
    # default_min_value=-1 if 'Conc' in file_path else default_min_value
    # default_max_value=-1 if 'Conc' in file_path else default_max_value
    # for index,nc_file in enumerate(files):     
    #     temp,unit_origin=get_extent_data(nc_file, variable_name,x_name=longitude_name,y_name=latitude_name,extent=extent)
    #     x=temp[longitude_name].data #data.longitude.values
    #     y=temp[latitude_name].data      
    #     name=os.path.basename(nc_file).replace('SCUT.GLOBAL.fluxBIO.','')
    #     grid_x, grid_y=np.meshgrid(x,y)
    #     grid_area=get_m2(grid_x, grid_y) 
    #     if 'Conc'in file_path:
    #         data=temp*math.pow(10,6)# μmol/mol = ppmv
    #         cmap='jet'
    #         unit='ppm'
    #     else:
    #         data=temp*((44.0/12)/math.pow(10,6))*grid_area*12 if unit=='ton' else temp*1/44*(44.0/12)/(24*3600*30)
    #     dict_data=get_multiple_data(dict_data,name,variable_name, x, y,data,nc_file)
    #     # if index==0:
    #     #     break
      
    # show_multi_maps(dict_data,show_original_grid=True,default_max_value=default_max_value,default_min_value=default_min_value,boundary_file=boundary_file,unit=unit,cmap=cmap)   
   
    ###结束：绘制SCUT.GLOBAL.fluxBIO.BAYES数据的示例  
    
    ###开始：绘制MEIC_3km数据的示例  
    import xarray as xr
    boundary_file =r'D:\D地图\广东省\广东市界镇界from zhu\广东市界R.shp'  
    variable_name="CO2"
    emis_paths=r"E:\CO2\data\emis\priori emission\MEIC_3km"
    emis_files=get_files(emis_paths)   
    
    model=model_attribute(emis_files[0])    
    x,y=model.get_xy_coordinates(show_lonlat=True)    
    dict_data={}
    unit=''            
    for index,emis_file in enumerate(emis_files):        
        ds = xr.open_dataset(emis_file, decode_times=False)
        if hasattr(ds[variable_name], 'units'):
            unit = ds[variable_name].units.strip()  
        file_name=os.path.basename(emis_file)  
        name=file_name.replace(f"EM_{file_name}_","") 
        if 'AG' in file_name:
            continue        
        get_multiple_data(dict_data,name,variable_name, x, y,np.mean(ds[variable_name][:,0,:,:],axis=0))
        if len(dict_data)==4:
            break
        
    fig=show_multi_maps(dict_data,show_original_grid=True,projection= model.projection,default_max_value=-1,default_min_value=-1,boundary_file=boundary_file,unit=unit,cmap='jet',showplot=False) 
    fig.savefig("dd.png")
     ###结束：绘制MEIC_3km数据的示例      
   
    print("Done")
   
   