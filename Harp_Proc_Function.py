# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:40:55 2019

@author: sibra
"""
#install Harp with 
#  conda install -c stcorp harp

def harpProc(pathlist, bb, res, dateSt, dateEnd, exp_dir, prod):
    
    import harp
    import pandas as pd
            
    pix_x = int((bb[0][1] - bb[0][0]) / res)
    pix_y = int((bb[1][1] - bb[1][0]) / res)
    
    min_x = bb[0][0]
    min_y = bb[1][0]
    
    
    if prod == 'L2__SO2___':
        ops = f'''SO2_column_number_density_validity>50;keep(latitude_bounds,
        longitude_bounds,SO2_column_number_density);bin_spatial({pix_y},{min_y},
        {res},{pix_x},{min_x},{res});derive(SO2_column_number_density[Pmolec/cm2])'''
        
        opt = 'so2_column=7km'
    
    elif prod == 'L2__NO2___':
        ops = f'''tropospheric_NO2_column_number_density_validity>75;keep(latitude_bounds,
        longitude_bounds,tropospheric_NO2_column_number_density);bin_spatial({pix_y},{min_y},
        {res},{pix_x},{min_x},{res});derive(tropospheric_NO2_column_number_density[Pmolec/cm2])'''
        
        opt = ''
        
    elif prod == 'L2__AER_AI':
        ops = f'''absorbing_aerosol_index_validity>80;keep(latitude_bounds,
        longitude_bounds,absorbing_aerosol_index);bin_spatial({pix_y},{min_y},
        {res},{pix_x},{min_x},{res});derive(absorbing_aerosol_index)'''
        
        opt = ''
    
    elif prod == 'L2__CO____':
        ops = f'''CO_column_number_density_validity>50;keep(latitude_bounds,
        longitude_bounds,CO_column_number_density);bin_spatial({pix_y},{min_y},
        {res},{pix_x},{min_x},{res});derive(CO_column_number_density)'''
        
        opt = ''
    
          
    hrp = harp.import_product(pathlist,operations = ops, options = opt, post_operations='bin()')
    
    hrp = harp.execute_operations(hrp,"squash(time, (latitude_bounds,longitude_bounds));derive(latitude {latitude});derive(longitude {longitude});exclude(longitude_bounds,latitude_bounds,longitude_bounds_weight,latitude_bounds_weight)")
    
    if dateSt != dateEnd:
        dt_st =  dateSt.strftime('%Y%m%d')
        dateEnd  = dateEnd.date() - pd.Timedelta(days=1)
        dt_end =  dateEnd.strftime('%Y%m%d')
        
        dt_shrt = f'''{dt_st}-{dt_end}'''
        
    elif dateSt == dateEnd:
        dt_shrt = dateSt.strftime('%Y%m%d')
    
    if prod == 'L2__SO2___':
        dat = hrp.SO2_column_number_density.data
    elif prod == 'L2__NO2___':
        dat = hrp.tropospheric_NO2_column_number_density.data
    elif prod == 'L2__AER_AI':
        dat = hrp.absorbing_aerosol_index.data
    elif prod == 'L2__CO____':
        dat = hrp.CO_column_number_density.data
    
    #harp.export_product(aer_exp, f'''C:/Users/Administrator/Documents/aer_export_{dt_shrt}.nc''')
    
    import xarray as xr
    import rioxarray
    
    da = xr.DataArray(data=dat, coords={'latitude':hrp.latitude.data,'longitude':hrp.longitude.data}, dims=('time', 'latitude', 'longitude'))    
            
    da.rio.to_raster(f'''{exp_dir}/{prod}_export_{dt_shrt}.tif''')
