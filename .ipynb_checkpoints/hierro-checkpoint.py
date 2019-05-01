""" Imports """

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


""" Core Functions """

def create_hierro(turbines, panels, base_filepath='data/df_base_hierro.csv'):
    df_base_hierro = pd.read_csv(base_filepath)
    
    ## Setting assets
    turbine_size = 2.3 # MW
    panel_size = 3 # kW

    current_wind = 5 * turbine_size # MW installed
    current_solar = panel_size # kW installed

    new_wind = turbines * turbine_size # MW installed
    new_solar = panels * panel_size # kW installed 

    df_base_hierro['5_wind_turbines'] = df_base_hierro['5_wind_turbines'] * (new_wind/current_wind)
    df_base_hierro['1_solar_panel'] = df_base_hierro['1_solar_panel'] * (new_solar/current_solar)

    new_wind_col = f'wind_{new_wind}MW'
    new_solar_col = f'solar_{new_solar/1000}MW'
    df_base_hierro = df_base_hierro.rename(columns={'1_solar_panel':new_solar_col, '5_wind_turbines':new_wind_col})

    df_base_hierro['delta'] = df_base_hierro['demand'] - ( df_base_hierro[new_wind_col]+df_base_hierro[new_solar_col] )

    return df_base_hierro

def calc_imbalance(df_hierro, delta_col='delta', _print=True):
    gen_shortcoming = df_hierro[df_hierro.delta>=0][delta_col].sum()
    gen_excess = np.abs(df_hierro[df_hierro.delta<0][delta_col].sum())

    if _print == True:
        print(f'Generation shortcoming: {round(gen_shortcoming/(6*1000), 1):,} GWh')
        print(f'Generation excess: {round(gen_excess/(6*1000), 1):,} GWh')
        print('')
        
    return gen_shortcoming, gen_excess



""" Plotting Helper Functions """

def plot_sys_dist(df_hierro, title=None, battery_capacity=None, ax=None, **kwargs):
    if ax == None:
        fig = plt.figure()
        ax = plt.subplot()

    if battery_capacity != None:
        sns.distplot(df_hierro['new_delta'], ax=ax, **kwargs)

    else:
        sns.distplot(df_hierro['delta'], ax=ax, **kwargs)

    if title != None:
        plt.title(title)
        
    plt.ylabel('Frequency Density')
    plt.xlabel('Demand Delta (MW)')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    return ax

def plot_dem_and_gen(df_hierro):
    fig = plt.figure()
    ax = plt.subplot()

    df_hierro.drop(columns='delta').plot(ax=ax)

    plt.ylabel('Demand/Generation (MW)')
    plt.xlabel('')
    plt.legend(bbox_to_anchor=(1, 1), frameon=False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
def plot_dem_delta(df_hierro):
    fig = plt.figure()
    ax = plt.subplot()

    df_hierro['delta'].plot(label='Delta')
    pd.Series(np.zeros(df_hierro.shape[0]), df_hierro.index).plot(style='k--')

    plt.ylabel('Demand Delta (MW)')
    plt.xlabel('')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)