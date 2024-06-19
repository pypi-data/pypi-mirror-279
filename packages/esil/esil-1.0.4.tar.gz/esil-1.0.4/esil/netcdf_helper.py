import netCDF4 as nc
import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime

def extract_variables_data(input_file, output_file, variables,dimension_name=None):
    '''
    @description: Extract variables data from input NetCDF file and save them to output NetCDF file.if dimension_name is not None, the specified dimension will be reduced to size 1.
    @param input_file: Input NetCDF file path.
    @param output_file: Output NetCDF file path.
    @param variables: List of variables to extract.
    @param dimension_name: Name of the dimension to reduce.
    '''
    # Open the input NetCDF file
    with nc.Dataset(input_file, 'r') as src:
        # Create the output NetCDF file
        with nc.Dataset(output_file, 'w') as dst:
            # Copy global attributes
            dst.setncatts(src.__dict__)            
            # Copy dimensions, except bottom_top which will be reduced to size 1
            for name, dimension in src.dimensions.items():
                if dimension_name is not None and name == dimension_name:                   
                    dst.createDimension(name, 1)
                else:
                    dst.createDimension(name, len(dimension) if not dimension.isunlimited() else None)               
            # Copy variables
            for name, variable in src.variables.items():
                if name in variables:
                    # Create the variable in the destination file
                    out_var = dst.createVariable(name, variable.datatype, variable.dimensions)
                    out_var.setncatts(variable.__dict__)                    
                    # Copy the data, slicing the first layer for bottom_top dimension
                    data = variable[:]
                    if dimension_name in variable.dimensions:
                        if dimension_name is not None:
                            index = variable.dimensions.index(dimension_name)
                            data = np.take(data, indices=0, axis=index)#indices=0: 获取索引为0的元素，即返回数组中索引为0的元素或子数组。                        
                    out_var[:] = data


def process_24hours_data_to_bj_time(date,output_folder,source_folder,layer_name,variables=[],input_file_prefix="",input_file_suffix="nc",output_file_suffix="CH4_ANFlux.bj.nc"): 
    '''
    @description: 将24小时数据(1个含24小时文件)合并到北京时间，并提取第一层数据
    @param {date: datetime.datetime, 日期}
    @param {output_folder: str, 输出文件夹}
    @param {source_folder: str, 数据源文件夹}
    @param {layer_name: str, 层名称}
    @param {variables: list, 需要提取的变量}
    @param {input_file_prefix: str, 文件前缀}
    @param {input_file_suffix: str, 文件后缀}
    @param {output_file_suffix: str, 输出文件后缀}
    @return: None
    '''
    import os
    import shutil
    from datetime import timedelta
    output_file = os.path.join(output_folder, f"{date.strftime('%Y%m%d%H')}.all_layers.{output_file_suffix}.nc") if len(variables) > 0 else os.path.join(output_folder, f"{date.strftime('%Y%m%d%H')}.{output_file_suffix}.nc")    
    current_date_file = os.path.join(source_folder, f"{input_file_prefix}.{date.strftime('%Y%m%d')}.{input_file_suffix}")
    if not  os.path.exists(current_date_file):
        print(f"File {current_date_file} not exists, skip it.")
        return
    shutil.copy(current_date_file,output_file)
    if date.strftime('%Y%m%d') != '20220101':#第一天不做处理
        previous_date = date - timedelta(days=1)
        previous_date_file=os.path.join(source_folder, f"{input_file_prefix}.{previous_date.strftime('%Y%m%d')}.{input_file_suffix}") 
        if not os.path.exists(previous_date_file):
            print(f"File {previous_date_file} not exists, skip it.{current_date_file} failed to process.")
            return       
        # shutil.copy(current_date_file,output_file)
        split_hours=8
        with nc.Dataset(output_file, 'r+') as src_dataset:
            for variable_name, variable in src_dataset.variables.items():
                if variable.dtype == 'S1':  # 字符串类型
                    continue
                previous_8h_data = nc.Dataset(previous_date_file, 'r')[variable_name][-split_hours:, :, :, :]  # 后一天的数据 
                current_16h_data =nc.Dataset(current_date_file, 'r')[variable_name][:(24-split_hours), :, :, :] # 当前文件的数据
                # 创建新的数据数组，长度为24小时
                new_data = np.zeros((24, *current_16h_data.shape[1:])) #*表示解包，即将一个可迭代对象（如列表、元组等）解包成单独的元素           
                # 填补前9小时数据
                new_data[:split_hours, :, :, :] = previous_8h_data            
                # 填补后面的15小时数据
                new_data[split_hours:, :, :, :] = current_16h_data            
                # 写回当前文件   
                variable[:] = new_data  
    if os.path.exists(output_file) and len(variables) > 0:     
        extract_variables_data(output_file, os.path.join(output_folder, f"{date.strftime('%Y%m%d%H')}.{output_file_suffix}"), variables,dimension_name=layer_name)
        os.remove(output_file)

def process_24files_data_to_bj_time(date,time_steps, output_folder,source_folder,layer_name,variables=[],input_file_prefix="",input_file_suffix="nc",input_date_str_format='%Y_%m_%d_%H',
                 output_file_suffix="ch4.conc.bj.nc", skip_file_length_validation=False):
    '''
    @description: 将24小时数据(24个小时文件)合并到北京时间，并提取第一层数据
    @param {date: datetime.datetime, 日期}
    @param {time_steps: list, 时间步长}
    @param {output_folder: str, 输出文件夹}
    @param {source_folder: str, 数据源文件夹}
    @param {layer_name: str, 层名称}
    @param {variables: list, 需要提取的变量}
    @param {input_file_prefix: str, 文件前缀}
    @param {input_file_suffix: str, 文件后缀}
    @param {input_date_str_format: str, 输入文件日期格式}
    @param {output_file_suffix: str, 输出文件后缀}
    @param {skip_file_length_validation: bool, 是否跳过文件长度验证}
    @return: None
    '''
    import os
    import subprocess
    from datetime import timedelta
    nccopy_command = 'nccopy'
    
    # 找到所有文件
    existing_files = []
    for time_step in time_steps:
        current_date = date + timedelta(hours=int(time_step))        
        file = os.path.join(source_folder, f"{input_file_prefix}{current_date.strftime(input_date_str_format)}.{input_file_suffix}")
        if os.path.exists(file) and os.path.getsize(file) > 0:            
            existing_files.append(file)
        else:
            print(f"File {file} not found or empty.")
    if not skip_file_length_validation:    
        if  len(existing_files) != 24:
            print(f"Not all 24 files found for date {date.strftime(input_date_str_format)}")
            if date.strftime('%Y-%m-%d') != '2022-01-01': 
                return
    
    existing_extracted_files=[]
    for source_file in existing_files:
        base_dir=os.path.dirname(source_file) 
        target_file_name=os.path.basename(source_file)     
        target_file = os.path.join(base_dir, f'{"extract"}.{target_file_name}')
        variable_names = ','.join(variables)
        command = [nccopy_command, '-V', variable_names, source_file, target_file]
        subprocess.run(command)
        if os.path.exists(target_file):
            target_file_1st_layer = os.path.join(output_folder, f'{target_file_name}.1layer')
            extract_variables_data(target_file, target_file_1st_layer, variables,dimension_name=layer_name)
            if os.path.exists(target_file_1st_layer):
                existing_extracted_files.append(target_file_1st_layer)
                os.remove(target_file)           
    # 打开多个文件并合并它们
    datasets = [xr.open_dataset(file) for file in existing_extracted_files]
    # 合并数据集
    combined_dataset = xr.concat(datasets, dim='Time')
    output_file = os.path.join(output_folder, f"{date.strftime('%Y%m%d%H')}.{output_file_suffix}")
    
    # 将合并后的数据集保存为一天 24 小时的 NetCDF 文件
    combined_dataset.to_netcdf(output_file)    
    # 关闭数据集
    combined_dataset.close()
    for file in existing_extracted_files:
        os.remove(file)        

     
def readNetCDF(nc_path, pollutant,timeStepIndex=0,layerStepIndex=0):
    '''
    :param nc_path: netcdf文件路径
    :param pollutant: 读取文件中变量
    :param timeStepIndex: 时间维度索引
    :param layerStepIndex: 层数维度索引
    :return: 读取 NetCDF 文件中的变量返回行列的数据框
    '''
    nc_data = nc.Dataset(nc_path)
    nc_data = nc_data.variables[pollutant][:][timeStepIndex,layerStepIndex]
    pd_data = pd.DataFrame(nc_data)
    # 关闭 NetCDF 文件
    #nc_data.close()
    return pd_data

def readNetCDFAsFlatten(nc_path, pollutant,timeStepIndex=0,layerStepIndex=0):
    '''
    :param nc_path: netcdf文件路径
    :param pollutant: 读取文件中变量
    :param timeStepIndex: 时间维度索引
    :param layerStepIndex: 层数维度索引
    :return: 读取 NetCDF 文件中的变量并将其展平成一维数组
    '''
    nc_data = nc.Dataset(nc_path)
    nc_data = nc_data.variables[pollutant][:][timeStepIndex, layerStepIndex]
    # 将多维数组展平成一维数组
    data_flattened = nc_data.flatten()
    # 关闭 NetCDF 文件
    #nc_data.close()
    return data_flattened

def createNETCDF(template_path,output_path,input_values,template_variable_index=0):
    '''
    :param template_path: netcdf模板文件路径
    :param output_path: 要生成的netcdf文件路径
    :param input_values:
    :param template_variable_index:
    :return:
    '''
    tempalate_dataset = nc.Dataset(template_path)  # 读取该ACONC文件基本信息
    col = tempalate_dataset.variables[template_variable_index].shape[0]  # 获取变量的列数量
    row = tempalate_dataset.variables[template_variable_index].shape[1]  # 获取变量的行数量
    variable_data = np.zeros((col, row))  # 创建与需要修改的变量同维度的全0矩阵
    k = 0  # 为保证CSV顺序与矩阵顺序相匹配，设定位置变量
    for i in range(row):
        for j in range(col):
            variable_data[j, i] = input_values[k]
            tip = f'第 {j} 列，第 {i} 行,第 {k} 个网格值'
            print(tip)
            k += 1
    with nc.Dataset(output_path, 'a') as ncfile:
        ncfile.variables[tempalate_dataset.variables[template_variable_index].name][:] = variable_data

def get_extent_data(nc_file,variable_name,x_name='lon',y_name='lat', extent=[]):
    '''
    :param nc_file: netcdf 文件路径
    :param variable_name: netcdf文件中要读取变量名称
    :param x_name: netcdf文件中x坐标方向的维度变量名称
    :param y_name: netcdf文件中y坐标方向的维度变量名称
    :param extent: 要提取的数据范围，默认为空，表示提取全域所有数据，如指定范围则按min_longitude，max_longitude，min_latitude，max_latitude顺序进行指定；
        如
        Guangdong Domain 的extent=[109.25,117.75,19,27]；
        China Domain的 extent = [70.25, 136.25, 4.75, 55.25];
        注意：截取后 data_subset.lon 和 data_subset.lat 是一维数组，data_subset 是对应的二维浓度数据
    :return: 返回提取后的数据
    '''

    # 打开NetCDF文件
    ds = xr.open_dataset(nc_file, decode_times=False)
    data = ds[variable_name]
    # 获取变量的单位信息
    unit = data.attrs.get('units')
    # Define the latitude and longitude ranges you want to display
    # min_longitude = ds[x_name].data.min()
    # max_longitude = ds[x_name].data.max()
    # min_latitude = ds[y_name].data.min()
    # max_latitude = ds[y_name].data.max()
    #考虑到有些数据经纬度并不一定是按数值大小进行排序，比如维度它是从90到-90，此时如果算最大值最小值的范围是-90,90，这个范围就会取不到任何数据。所以用维度的第一个数据和最后一个数值表示最小值和最大值
   
    min_longitude = ds[x_name].data[0]
    max_longitude = ds[x_name].data[-1]    
    min_latitude = ds[y_name].data[0]
    max_latitude = ds[y_name].data[-1]

    if extent:  # 不为空则用用户指定的范围       
        min_longitude = extent[0] if min_longitude<max_longitude else extent[1]
        max_longitude = extent[1] if min_longitude<max_longitude else extent[0]
        min_latitude = extent[2] if min_latitude<max_latitude else extent[3]
        max_latitude = extent[3] if min_latitude<max_latitude else extent[2]
        # min_longitude = extent[0] if(min_longitude<max_longitude and ds[x_name].data[0]<ds[x_name].data[1]) else extent[1]
        # max_longitude = extent[1] if min_longitude<max_longitude and ds[x_name].data[0]<ds[x_name].data[1] else extent[0]
        # min_latitude = extent[2] if min_latitude<max_latitude and ds[y_name].data[0]<ds[y_name].data[1] else extent[3]
        # max_latitude = extent[3] if min_latitude<max_latitude and ds[y_name].data[0]<ds[y_name].data[1] else extent[2]
    # 定义要显示的经纬度范围slice(min_longitude, max_longitude)和slice(min_latitude, max_latitude)
    # Use .sel() to select the specific latitude and longitude range
    # 根据维度名称获取维度变量    
    #data_subset = data.sel(x=slice(min_longitude, max_longitude), y=slice(min_latitude, max_latitude))
    data_subset = data.sel({x_name: slice(min_longitude, max_longitude), y_name: slice(min_latitude, max_latitude)})

    return data_subset,unit

def update_netcdf_file(nc_file):
    data = nc.Dataset(nc_file, mode='r+', format="NETCDF4")
    data.variables['PM25_TOT'].units = "μg/m3"    
    # data.TSTEP = 240000
    # data.SDATE  =  data.SDATE+1
    data.close()


def generate_date_array(start_date_str, num_days):
    from datetime import datetime, timedelta
    date_format = "%Y-%m-%d %H:%M:%S"
    start_date = datetime.strptime(start_date_str, date_format)
    date_array = [start_date + timedelta(days=i) for i in range(num_days)]
    date_strings = [date.strftime(date_format) for date in date_array]
    return date_strings

def update_netcdf_file_variable(nc_file,var_name,var_value,var_unit=''):
    data = nc.Dataset(nc_file, mode='r+', format="NETCDF3_CLASSIC")   
    data.variables[var_name][:] = var_value
    if var_unit:
        data.variables[var_name].units =var_unit
    data.close()

def create_netcdf_file(output_file, data, var_name, var_unit):
 
    # 创建NetCDF文件
    ncfile = nc.Dataset('example.nc', 'w')

    # 创建维度
    time_dim = ncfile.createDimension('time', None)
    lat_dim = ncfile.createDimension('lat', 10)
    lon_dim = ncfile.createDimension('lon', 20)

    # 创建变量
    time_var = ncfile.createVariable('time', 'f4', ('time',))
    lat_var = ncfile.createVariable('lat', 'f4', ('lat',))
    lon_var = ncfile.createVariable('lon', 'f4', ('lon',))
    data_var = ncfile.createVariable('data', 'f4', ('time', 'lat', 'lon'))

    # 设置变量的属性
    time_var.units = 'days since 2000-01-01'
    lat_var.units = 'degrees_north'
    lon_var.units = 'degrees_east'
    data_var.units = 'kg/m^2'

    # 设置变量的值
    time_var[:] = [0, 1, 2, 3, 4]
    lat_var[:] = range(10)
    lon_var[:] = range(20)
    data_var[:] = 1.0

    # 关闭NetCDF文件
    ncfile.close()

def create_netcdf_file_with_dims_update(files):    
    # 打开第一个文件以获取变量和维度信息
    with nc.Dataset(files[0], 'r') as src_dataset:      
        file_format=src_dataset.file_format  
        import os
        base_name=os.path.basename(files[0])   
        dir_name=os.path.dirname(files[0]) 
        date_time = datetime.strptime(os.path.basename(dir_name), "%Y%m%d%H")
        file_name = f"{date_time.strftime('%Y%m%d')}.{base_name}.nc"          
        new_file =os.path.join(os.path.dirname(dir_name),file_name)
        # 创建新的合并文件
        with nc.Dataset(new_file, 'w',format=file_format) as dst_dataset:
            # 复制全局属性
            dst_dataset.setncatts(src_dataset.__dict__)
            # 复制维度
            for name, dimension in src_dataset.dimensions.items():
                dst_dataset.createDimension(name, len(dimension) if not dimension.isunlimited() else None)
            # 复制变量
            for name, variable in src_dataset.variables.items():
                # 创建变量
                dst_variable = dst_dataset.createVariable(name, variable.dtype, variable.dimensions)
                # 复制变量属性
                dst_variable.setncatts(variable.__dict__)
                # 创建合并数据数组
                merged_data = np.zeros(variable.shape)   
                # 合并数据
                for file in files:
                    with nc.Dataset(file, 'r') as src_new_dataset:
                        src_variable = src_new_dataset.variables[name]
                        merged_data += src_variable[:]   
                # # 计算每天的平均值             
                daily_mean_data=merged_data/len(files)
                # 将数据写入新的合并文件
                dst_variable[:] = daily_mean_data
            print(f"成功创建{file_name}")    
    
    
if __name__=="__main__":
    # nc_file=r'E:\CO2\data\emis\posterior emission\GD_9km\CONC_BG\2022010100\CONC.bg'
    # model_dir=r'E:\CO2\data\emis\posterior emission\GD_9km\CONC_BG'
    # dates=pd.date_range('2022-01-01',end='2022-12-31',freq='D')
    # from esil.file_helper import get_model_files_by_date
    # for date in dates:
    #     date_str=date.strftime('%Y%m%d')
    #     files=get_model_files_by_date(model_dir,date_str,date_str)
    #     create_netcdf_file_with_dims_update(files)        
      
    
    nc_file='E:/data/emis/CarbonMonitor_total_y2019_m06.nc'
    # start_date = "2019-06-01 00:00:00"
    # num_days = 30
    # date_array =generate_date_array(start_date, num_days)
    # date_array = np.linspace(0, 29, 30)
    # var_unit= f"days since {start_date}"   
    var_name='nday' 
    # update_netcdf_file_variable(nc_file,var_name,date_array,var_unit)
    # data = nc.Dataset(nc_file, mode='r', format="NETCDF3_CLASSIC")
    from esil.file_helper import get_files
     # 获取目录中的所有文件
    variable_name='emission'
    files = get_files(r'E:\data\emis\GRACED')
    all_data = []
    # 逐个打开每个文件并读取数据
    for file in files:
        dataset = nc.Dataset(file)
        variable_data = dataset.variables[variable_name][:]  # 替换为您要读取的变量名称
        all_data.append(variable_data)

    # 合并所有数据为一个大数组
    all_data = np.concatenate(all_data, axis=0)
    # 计算全年平均
    annual_mean = np.mean(all_data, axis=0)
    # 将结果保存到新的文件中
    new_file = "annual_mean.nc"
    new_dataset = nc.Dataset(new_file, mode="w", format="NETCDF4")
    new_dataset.createDimension("time", annual_mean.shape[0])   
    new_dataset.createVariable("annual_mean", "f4", ("time",))
    new_dataset.variables["annual_mean"] = annual_mean
    new_dataset.close()
    



    # 指定要合并的维度 
    # 使用 MFDataset 函数打开多个文件并指定要合并的维度
    # dataset =nc.MFDataset(files, aggdim=var_name)
    # f = nc.MFDataset(files)
    # var = f.variables[variable_name][:]

    nc_file=r'E:\new_CT2022.molefrac_components_glb3x2_2020-12-31.nc'
     
    from plot_map import plotmap
    nc_file= r'/NetcdfReader/CO2 Visualization/CO2-em-anthro_input4MIPs_emissions_CMIP_CEDS-2021-04-21_gn_200001-201912.nc'
    variable_name='CO2_em_anthro'
    data,unit = get_extent_data(nc_file, variable_name)
    #data=get_extent_data(nc_file,variable_name)
    # 对指定列进行求和，使用 axis 参数来指定列维度
    #sum_sector_data = np.sum(data, axis=1)
    sum_data=np.sum(data,axis=(0,1))
    x = sum_data.lon.values
    y = sum_data.lat.values
    data = sum_data.values
    grid_x, grid_y = np.meshgrid(x, y)
    fig=plotmap(grid_x, grid_y, grid_concentration=data, title=variable_name)
    if fig:
        fig.show()

