import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
from matplotlib.pyplot import figure
import matplotlib as mpl
import json

from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr
from tigramite.independence_tests.robust_parcorr import RobustParCorr
from sklearn.linear_model import LinearRegression

import statsmodels.api as sm

# Functions:
def pcmci_graph_bootstrap(DATA, cond_ind_test, tau_min,  tau_max, alpha_level, pc_alpha, mask_threshold, boot_samples):
    
    labels = list(DATA.columns)
    labels = [label.split(' w')[0] for label in labels]
    var_names = labels
    all_data_array = np.array(DATA, dtype = float)
    data_mask = np.zeros(all_data_array.shape)
    T = all_data_array.shape[0]

    for t in range(1, T):
        if all_data_array[t,0] < mask_threshold: 
            data_mask[t, 0] = True

    T, N = all_data_array.shape

    datatime = np.arange(T)
    dataframe = pp.DataFrame(all_data_array, datatime = np.arange(len(all_data_array)), var_names=var_names, mask=data_mask)

    N = len(var_names)

    # Nothing can cause precipitation: masking precipitation links
    link_assumptions = {j:{(i, -tau):'o?o' for i in range(N) for tau in range(tau_min,tau_max + 1) if (i, -tau) != (j, 0)} 
                                for j in range(N)}

    link_assumptions[1] = {(i, -tau):'-?>' for i in range(N) for tau in range(tau_min,tau_max + 1)
                        if ((i, -tau) not in [(1,0),(1,2),(1,3),(1,4),(1,5)] and i not in [0,1, 2, 3, 4, 5])} 
                            
    lvTmp = np.linspace(0.1,0.8,(256)-1)
    cmTmp = mpl.cm.OrRd(lvTmp)
    newCmap = mcol.ListedColormap(cmTmp)

    pcmci = PCMCI(dataframe=dataframe, cond_ind_test=cond_ind_test, verbosity=0) 

    boot_blocklength = 1
    # Call bootstrap for the chosen method (here 'run_pcmciplus') and pass method arguments  
    results = pcmci.run_bootstrap_of(
            method='run_pcmci', 
            method_args={'tau_min': tau_min,'tau_max':tau_max, 'alpha_level':alpha_level, 'pc_alpha': pc_alpha, 'link_assumptions':link_assumptions}, 
            boot_samples=boot_samples,
            boot_blocklength=boot_blocklength,
            seed=123)

    # Output graph, link frequencies (confidence measure), and mean test statistic values (val_mat)
    boot_linkfreq = results['summary_results']['link_frequency']
    boot_graph = results['summary_results']['most_frequent_links']
    val_mat = results['summary_results']['val_matrix_mean']

    # Plot causal graph
    tp.plot_graph(
        val_matrix=val_mat,
        graph=boot_graph,
        var_names=var_names,
        link_width = boot_linkfreq,
        link_colorbar_label='cross-MCI',
        node_colorbar_label='auto-MCI',
        label_fontsize = 20,
        figsize=(18,12), node_label_size = 30, node_size  =0.5, link_label_fontsize =20, arrow_linewidth=10,cmap_edges = 'RdBu_r', cmap_nodes = newCmap, 
        vmin_nodes = 0, vmax_nodes = 1, node_ticks = 0.5, edge_ticks = 0.5, show_colorbar =  True, node_aspect = None, curved_radius  = 0.2, 
        ); 

    plt.show()

    return results


def pcmci_graph_robustness_bootstrap(DATA, cond_ind_test, tau_min,  tau_max, alpha_list, alpha_level, mask_threshold, boot_samples):

    i = 0
   
    fig, ax = plt.subplots(2, 3, figsize=(60, 30), facecolor='w')
    ax = ax.flatten()

    for alpha in alpha_list:
        
        pc_alpha = alpha

        labels = list(DATA.columns)
        labels = [label.split(' w')[0] for label in labels]
        var_names = labels
        all_data_array = np.array(DATA, dtype = float)
        data_mask = np.zeros(all_data_array.shape)
        T = all_data_array.shape[0]

        for t in range(1, T):
            if all_data_array[t,0] < mask_threshold: 
                data_mask[t, 0] = True

        T, N = all_data_array.shape
        # print data_mask[:100, 0]
        datatime = np.arange(T)
        dataframe = pp.DataFrame(all_data_array, datatime = np.arange(len(all_data_array)), var_names=var_names, mask=data_mask)

        N = len(var_names)

        # Nothing can cause precipitation: masking precipitation links
        link_assumptions = {j:{(i, -tau):'o?o' for i in range(N) for tau in range(1,tau_max + 1) if (i, -tau) != (j, 0)} 
                                    for j in range(N)}

        link_assumptions[1] = {(i, -tau):'-?>' for i in range(N) for tau in range(1,tau_max + 1)
                            if ((i, -tau) not in [(1,0),(1,2),(1,3),(1,4),(1,5)] and i not in [0,1, 2, 3, 4, 5])} 
                                
        lvTmp = np.linspace(0.1,0.8,(256)-1)
        cmTmp = mpl.cm.OrRd(lvTmp)
        newCmap = mcol.ListedColormap(cmTmp)

        pcmci = PCMCI(dataframe=dataframe, cond_ind_test=cond_ind_test, verbosity=0) 
        boot_blocklength = 1
        # Call bootstrap for the chosen method (here 'run_pcmciplus') and pass method arguments  
        results = pcmci.run_bootstrap_of(
                method='run_pcmci', 
                method_args={'tau_min': tau_min,'tau_max':tau_max, 'pc_alpha':pc_alpha, 'alpha_level':alpha_level, 'link_assumptions':link_assumptions}, 
                boot_samples=boot_samples,
                boot_blocklength=boot_blocklength,
                seed=123)


        # Output graph, link frequencies (confidence measure), and mean test statistic values (val_mat)
        boot_linkfreq = results['summary_results']['link_frequency']
        boot_graph = results['summary_results']['most_frequent_links']
        val_mat = results['summary_results']['val_matrix_mean']

        # Plot graph
        axs = ax[i]
        
        i = i + 1
        
        axs.set_title('\u03B1 = ' + str(alpha), fontsize=50)
        axs.set_facecolor(color = 'w')
        axs.set_facecolor(color = (0.94117647, 0.97254902, 1.))
        axs.patch.set_alpha(0.2)

        # Plot causal graph
        tp.plot_graph(
            val_matrix=val_mat,
            graph=boot_graph,
            var_names=var_names,
            link_width = boot_linkfreq,
            link_colorbar_label='cross-MCI',
            node_colorbar_label='auto-MCI',
            label_fontsize = 30,
            fig_ax = (fig,axs),
            figsize=(10,4), node_label_size = 50, node_size  =0.55, link_label_fontsize =40, arrow_linewidth=15,cmap_edges = 'RdBu_r', cmap_nodes = newCmap, 
            vmin_nodes = 0, vmax_nodes = 1, node_ticks = 0.5, edge_ticks = 0.5, show_colorbar =  False, node_aspect = None, curved_radius  = 0.2, 
            ); 
        plt.tight_layout()

    plt.show()


def pcmci_graph_tau_bootstrap(DATA, cond_ind_test, tau_min,  tau_list, pc_alpha, alpha_level, mask_threshold, boot_samples):

    i = 0
   
    fig, ax = plt.subplots(2, 3, figsize=(60, 30), facecolor='w')
    ax = ax.flatten()

    for tau_max in tau_list:

        labels = list(DATA.columns)
        labels = [label.split(' w')[0] for label in labels]
        var_names = labels
        all_data_array = np.array(DATA, dtype = float)
        data_mask = np.zeros(all_data_array.shape)
        T = all_data_array.shape[0]

        for t in range(1, T):
            if all_data_array[t,0] < mask_threshold: 
                data_mask[t, 0] = True

        T, N = all_data_array.shape
        # print data_mask[:100, 0]
        datatime = np.arange(T)
        dataframe = pp.DataFrame(all_data_array, datatime = np.arange(len(all_data_array)), var_names=var_names, mask=data_mask)

        N = len(var_names)

        # Nothing can cause precipitation: masking precipitation links
        link_assumptions = {j:{(i, -tau):'o?o' for i in range(N) for tau in range(1,tau_max + 1) if (i, -tau) != (j, 0)} 
                                    for j in range(N)}

        link_assumptions[1] = {(i, -tau):'-?>' for i in range(N) for tau in range(1,tau_max + 1)
                            if ((i, -tau) not in [(1,0),(1,2),(1,3),(1,4),(1,5)] and i not in [0,1, 2, 3, 4, 5])} 
                                
        lvTmp = np.linspace(0.1,0.8,(256)-1)
        cmTmp = mpl.cm.OrRd(lvTmp)
        newCmap = mcol.ListedColormap(cmTmp)

        pcmci = PCMCI(dataframe=dataframe, cond_ind_test=cond_ind_test, verbosity=0) 
        boot_blocklength = 1
        # Call bootstrap for the chosen method (here 'run_pcmciplus') and pass method arguments  
        results = pcmci.run_bootstrap_of(
                method='run_pcmci', 
                method_args={'tau_min': tau_min,'tau_max':tau_max, 'pc_alpha':pc_alpha, 'alpha_level':alpha_level, 'link_assumptions':link_assumptions}, 
                boot_samples=boot_samples,
                boot_blocklength=boot_blocklength,
                seed=123)
        
        # save results
        # To json with numpy array handling
        # j = json.dumps({k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in results['summary_results'].items()})
        # Directly from dictionary
        # with open(f'Baidoa_tau_{tau_max}.json', 'w') as outfile:
        #     outfile.write(j)

        # Output graph, link frequencies (confidence measure), and mean test statistic values (val_mat)
        boot_linkfreq = results['summary_results']['link_frequency']
        boot_graph = results['summary_results']['most_frequent_links']
        val_mat = results['summary_results']['val_matrix_mean']

        boot_linkfreq = results['summary_results']['link_frequency']
        boot_graph = results['summary_results']['most_frequent_links']
        val_mat = results['summary_results']['val_matrix_mean']

        # Plot graph
        axs = ax[i]
        
        i = i + 1
        
        axs.set_title('tau_max = ' + str(tau_max), fontsize=50)
        axs.set_facecolor(color = 'w')
        axs.set_facecolor(color = (0.94117647, 0.97254902, 1.))
        axs.patch.set_alpha(0.2)

        # Plot causal graph
        tp.plot_graph(
            val_matrix=val_mat,
            graph=boot_graph,
            var_names=var_names,
            link_width = boot_linkfreq,
            link_colorbar_label='cross-MCI',
            node_colorbar_label='auto-MCI',
            label_fontsize = 30,
            fig_ax = (fig,axs),
            figsize=(10,4), node_label_size = 50, node_size  =0.55, link_label_fontsize =40, arrow_linewidth=15,cmap_edges = 'RdBu_r', cmap_nodes = newCmap, 
            vmin_nodes = 0, vmax_nodes = 1, node_ticks = 0.5, edge_ticks = 0.5, show_colorbar =  False, node_aspect = None, curved_radius  = 0.2, 
            ); 
        plt.tight_layout()

    plt.show()


regions = pd.read_csv('Regions.csv', usecols = ['District','Region'])

def data_pipeline(district, Somalia_IDP_Database, interp_market= 'quadratic', deflate = True, window = 4, date_graph1 =  '2016', date_graph2 = '2023', regions=regions):

    print(district)
    district_data = Somalia_IDP_Database[Somalia_IDP_Database.District == district]
    date_time = pd.to_datetime(district_data.Date)
    district_data = district_data.set_index(date_time).iloc[:,2:]

    # All Variables Select
    idp = district_data.iloc[:,0]; prep = district_data.iloc[:,1]; 
    vio = district_data.iloc[:,2];  market = district_data.iloc[:,3:]

    # Clean Data: remove outliers and substitute from nearest market for missing data variables
    market = market_sub(district, market, Somalia_IDP_Database)

    market = market.interpolate(method=interp_market)

    MEB = market[['Red Sorghum Price', 'Wheat Flour Price', 'Sugar Price', 'Vegetable Oil Price', 'Camel Milk Price', 'Tea Leaves Price','Salt Price', 'Cowpeas Price']]
    livestock = market[['Cattle Price' , 'Camel Price', 'Goat Price']]
    water = market['Water Drum Price']

    # Let me know if the district has all data
    MEB = MEB.dropna(axis=1, how='all')

    # Weights of MEB from FSNAU
    weights = [95, 3.75, 5, 4, 15, 0.5, 1.5, 6]
    CMB = (MEB * weights).sum(axis = 1) / np.array(weights).sum() * 100

    # Cattle, Camel, Goats weights per region:
    south_central = ['Banadir', 'Bakool', 'Bay', 'Gedo', 'Galgaduud','Hiraan', 'Middle Juba', 'Lower Juba', 'Middle Shabelle', 'Lower Shabelle']
    puntland = ['Bari', 'Mudug', 'Nugaal']          
    somaliland=['Awdal', 'Togdheer', 'Sanaag',  'Sool','Woqooyi Galbeed']


    region = regions[regions.District == district].iloc[0,1]

    # Weights of livestock prices 
    if region  in south_central:
        area = 'South Central'
        south_central_total = 1935+2347+440
        region_weights = [1935 / south_central_total, 2347 / south_central_total, 440 / south_central_total]
    if region  in puntland:
        area = 'Puntland'
        puntland_total = 200+894+630
        region_weights = [200 / puntland_total, 894 / puntland_total, 630 / puntland_total]
    if region  in somaliland:
        area = 'Somaliland'
        somaliland_total = 207+823+443
        region_weights = [207 / somaliland_total, 823 / somaliland_total, 443 / somaliland_total]

    if livestock['Cattle Price'].isnull().all():
        region_weights = region_weights[1:]

    livestock = livestock.dropna(axis=1, how='all')    

    # Weight by region capital values of livestock
    livestock_weighted = (livestock * region_weights)
    livestock_index = livestock_weighted.sum(axis = 1) / np.array(region_weights).sum() * 100
    livestock_index.replace(0, np.nan, inplace = True)

    CMB.name = 'Food Prices'
    livestock_index.name = 'Livestock Prices'
    water.name = 'Water Prices'

    date1 = district_data['IDP Drought'].first_valid_index() # First point in TS

    market_prices = pd.concat([CMB, livestock_index, water], axis = 1).shift(-2).loc[date1:]
    
    if deflate:
        if area == 'Somaliland':
            market_prices = market_prices.divide(market.SomalilandShToUSD.loc[date1:], axis = 0)
            market_prices = pd.concat([market_prices, market.SomalilandShToUSD.loc[date1:]], axis = 1)
            
        else:  
            market_prices = market_prices.divide(market.SomaliShillingToUSD.loc[date1:], axis = 0) 
            market_prices = pd.concat([market_prices, market.SomaliShillingToUSD.loc[date1:]], axis = 1)
        
    if deflate:
        from sklearn.linear_model import LinearRegression
        for commodity in market_prices:

            idx = market_prices[commodity].dropna().index
            series = market_prices[commodity].dropna()
            # fit linear model: calculate trend
            X = [i for i in range(0, len(series))]
            X = np.reshape(X, (len(X), 1))
            y = series.values
            model = LinearRegression()
            model.fit(X, y)
            trend = model.predict(X)

            # detrend
            if model.coef_ > 0:
                detrended = [y[i]-trend[i] for i in range(0, len(series))]
                market_prices.loc[idx, commodity] = detrended

    VIO = vio.copy().fillna(0).rolling(window).sum()
    IDP = idp.copy().fillna(0).rolling(window).sum()

    DATA_graph = pd.concat([IDP, prep, market_prices[['Food Prices', 'Livestock Prices', 'Water Prices']], VIO],axis=1).dropna().loc[date_graph1:date_graph2]

    return DATA_graph


def market_sub(district, market_data, full_data):
    
    if district == 'Bandarbeyla':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        
    if district == 'Caluula':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    
    if district == 'Qandala':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
    
    if district == 'Laasqoray':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
    if district == 'Caynabo':
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']    
        
    if district == 'Ceel Afweyn':
        
        replace_from = full_data[full_data['District'] == 'Ceerigaabo']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price'] 
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']  
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']  
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 2e+6] = None   
    
    if district == 'Ceerigaabo':
        
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 2e+6] = None   
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price'] 
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']  
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']  
    
    if district == 'Berbera':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
    if district == 'Gebiley':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    

    if district == 'Baki':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    
    if district == 'Hargeysa':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
    if district == 'Sheikh':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    
    if district == 'Owdweyne':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    
    
    if district == 'Burco':

        replace_from = full_data[full_data['District'] == 'Ceerigaabo']
        replace_from.index = replace_from.Date 
        market_data['Salt Price'] = replace_from['Salt Price']  
    
        
    if district == 'Taleex':

        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
                
        
    if district == 'Xudun':
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']    
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']    
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']    
    
    if district == 'Bandarbeyla':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]

    if district == 'Hobyo':
        
        replace_from = full_data[full_data['District'] == 'Xarardheere']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']    
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']    
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']   
        
        
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
    
    if district == 'Cadaado':
        
        replace_from = full_data[full_data['District'] == 'Dhuusamarreeb']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        market_data['Cattle Price'] = None
        
        
    if district == 'Galdogob':
        
        replace_from = full_data[full_data['District'] == 'Burtinle']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Tea Leaves Price'] = replace_from.loc[:,'Tea Leaves Price']    
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']    
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']    
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']    
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 3e+6] = None   
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
    
    if district == 'Gaalkacyo':
        
        replace_from = full_data[full_data['District'] == 'Burtinle']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Tea Leaves Price'] = replace_from.loc[:,'Tea Leaves Price']    
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']    
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']    
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']    
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 3e+6] = None   
        

    if district == 'Burtinle':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Tea Leaves Price'] = replace_from.loc[:,'Tea Leaves Price']    
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']    
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']    
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']    
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 3e+6] = None

    
    if district == 'Eyl':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Tea Leaves Price'] = replace_from.loc[:,'Tea Leaves Price']    
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']    
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']    
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']    
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 3e+6] = None
    
    if district == 'Qardho':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
    if district == 'Iskushuban':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        
    if district == 'Buuhoodle':
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']    
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
    
    if district == 'Laas Caanood':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']    
    
    if district == 'Cabudwaaq':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
    

    if district == 'Dhuusamarreeb':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
    
    if district == 'Cadale':
        replace_from = full_data[full_data['District'] == 'Ceel Dheer']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        market_data.loc[:,'Wheat Flour Price'] = replace_from.loc[:,'Wheat Flour Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
    
    if district == 'Adan Yabaal':
        
        replace_from = full_data[full_data['District'] == 'Ceel Dheer']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
    
    if district == 'Ceel Dheer':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
    
    if district == 'Xarardheere':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        
        market_data.loc[:,'Red Sorghum Price'][market_data.index > '2020'][market_data.loc[:,'Red Sorghum Price'] > 18000] = None
    
    if district == 'Balcad':
        
        replace_from = full_data[full_data['District'] == 'Marka']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Tea Leaves Price'][market_data.loc[:,'Tea Leaves Price'] > 90000.0] = None
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        
    if district == 'Xudur':
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date 
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        market_data.loc[:,'Vegetable Oil Price'][market_data.loc[:,'Vegetable Oil Price'] > 100000.0] = None
    
    if district == 'Waajid':
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date 
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        market_data.loc[:,'Vegetable Oil Price'][market_data.loc[:,'Vegetable Oil Price'] > 100000.0] = None
    
    if district == 'Luuq':
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date 
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        market_data.loc[:,'Vegetable Oil Price'][market_data.loc[:,'Vegetable Oil Price'] > 100000.0] = None
    
    if district == 'Doolow':
        
        replace_from = full_data[full_data['District'] == 'Qansax Dheere'] 
        replace_from.index = replace_from.Date 
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    
    
    if district == 'Belet Xaawo':
        
        replace_from = full_data[full_data['District'] == 'Ceel Waaq'] 
        replace_from.index = replace_from.Date 
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        
    if district == "Badhaadhe":
        
        replace_from = full_data[full_data['District'] == 'Afmadow']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        replace_from = full_data[full_data['District'] == 'Baardheere'] 
        replace_from.index = replace_from.Date        
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
    
    if district == "Afmadow":
            
        replace_from = full_data[full_data['District'] == 'Baardheere'] 
        replace_from.index = replace_from.Date        
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
        
    if district == "Jamaame":
        
        replace_from = full_data[full_data['District'] == 'Jilib']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
                
        replace_from = full_data[full_data['District'] == 'Baraawe'] 
        replace_from.index = replace_from.Date        
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        
    
    if district == "Saakow":
        
        replace_from = full_data[full_data['District'] == 'Baardheere']
        replace_from.index = replace_from.Date
        
        replace_from.loc[:,'Goat Price'][replace_from.loc[:,'Goat Price'] > 1.6e+6]  = None
        
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
                
        replace_from = full_data[full_data['District'] == 'Diinsoor'] 
        replace_from.index = replace_from.Date
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']   
        
        
        market_data.loc[:,'Goat Price'][market_data.loc[:,'Goat Price'] > 2e+6]  = None
        
        
        
    if district == "Bu'aale":
        
        replace_from = full_data[full_data['District'] == 'Jilib']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        
        replace_from = full_data[full_data['District'] == 'Diinsoor']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        
    
    if district == 'Jilib':
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
    
    if district == 'Marka':
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        
        
    if district == 'Baraawe':
        
        replace_from = full_data[full_data['District'] == 'Jilib']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
    
    
    if district == 'Banadir':
        
        replace_from = full_data[full_data['District'] == 'Marka']
        replace_from.index = replace_from.Date
        
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        
    if district == 'Jowhar':
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn']
        replace_from.index = replace_from.Date
        
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
    
    
    if district == 'Jalalaqsi':
        
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        
    if district == 'Belet Weyne':
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
    
    if district == 'Ceel Buur':
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
    if district == 'Bulo Burto':
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
               
        
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
    
    if district == 'Ceel Barde':
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
                
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        
        
    if district == 'Rab Dhuure':
        replace_from = full_data[full_data['District'] == 'Ceel Barde']
        replace_from.index = replace_from.Date
        
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
                
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        
    
    if district == 'Tayeeglow':

        replace_from = full_data[full_data['District'] == 'Ceel Barde']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        
        market_data.loc[:,'Goat Price'][market_data['Goat Price'] > 2.2e+6] =None
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        
    
    if district == 'Kurtunwaarey':
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        market_data.loc[market_data['Vegetable Oil Price'] > 70000.0, 'Vegetable Oil Price'] = None
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
    
    if district == 'Jariiban':
        
        # Eliminate anomalies:
        market_data.loc[:,'Red Sorghum Price'][market_data['Red Sorghum Price'] > 100000] = None
        market_data.loc[:,'Tea Leaves Price'][market_data['Tea Leaves Price'] < 1000] = None
        market_data.loc[:,'Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 190000.0] = None
        
        # Replace poor quality data
        replace_from = full_data[full_data['District'] == 'Garoowe'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']     
        
    if district == 'Baidoa':
        market_data.loc[market_data['Vegetable Oil Price'] > 100000.0, 'Vegetable Oil Price'] = None
            
    if district == 'Kismayo':
        
        replace_from = full_data[full_data['District'] == 'Baraawe'] 
        replace_from.index = replace_from.Date
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        market_data.loc[:,'SomalilandShToUSD'] = np.NaN
        
        
    if district == 'Baardheere':

        replace_from = full_data[full_data['District'] == 'Diinsoor'] 
        replace_from.index = replace_from.Date
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']   
        
    if district == 'Lughaye':

        replace_from = full_data[full_data['District'] == 'Borama'] 
        replace_from.index = replace_from.Date
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price'] 
        market_data.loc[:,'Cattle Price'] = None
        
    if district == 'Zeylac':
        
        replace_from = full_data[full_data['District'] == 'Borama'] 
        replace_from.index = replace_from.Date
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price'] 
        market_data.loc[:,'Cattle Price'] = None
    
    if district == 'Qoryooley':
        replace_from = full_data[full_data['District'] == 'Wanla Weyn'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']    
        
    
    if district == 'Buur Hakaba':
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        market_data.loc[:,'Vegetable Oil Price'] = replace_from.loc[:,'Vegetable Oil Price']
        
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']
        market_data.loc[:,'Camel Price'] = replace_from.loc[:,'Camel Price']
        
    if district == 'Sablaale':
        
        replace_from = full_data[full_data['District'] == 'Baraawe'] 
        replace_from.index = replace_from.Date
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
        
    if district == 'Afgooye':
        
        replace_from = full_data[full_data['District'] == 'Balcad'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Red Sorghum Price'] = replace_from.loc[:,'Red Sorghum Price']
        market_data.loc[:,'Vegetable Oil Price'] = replace_from.loc[:,'Vegetable Oil Price']
        market_data.loc[:,'Goat Price'] = replace_from.loc[:,'Goat Price']
        market_data.loc[:,'Sugar Price'] = replace_from.loc[:,'Sugar Price']
        market_data.loc[:,'Camel Milk Price'] = replace_from.loc[:,'Camel Milk Price']
        market_data.loc[:,'Tea Leaves Price'] = replace_from.loc[:,'Tea Leaves Price']
        market_data.loc[:,'Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 100000.0] = None       
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        market_data.loc[:,'SomaliShillingToUSD'] = replace_from.loc[:,'SomaliShillingToUSD']
        market_data.loc[:,'Water Drum Price'] = replace_from.loc[:,'Water Drum Price']
        market_data.loc[:,'Cowpeas Price'] = replace_from.loc[:,'Cowpeas Price']
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:,'Cattle Price'] = replace_from.loc[:,'Cattle Price']   
        market_data.loc[:, 'Camel Price'] = replace_from.loc[:, 'Camel Price']
    
    if district == 'Garbahaarey':
        replace_from = full_data[full_data['District'] == 'Qansax Dheere'] 
        replace_from.index = replace_from.Date
        
        market_data.loc[:, market_data.columns[16:]] = replace_from.iloc[:,16:]
        
    
    # Correct for Somali Shilling
    SomalilandSH = ['Lughaye', 'Zeylac', 'Ceel Afweyn', 'Laas Caanood', 'Taleex', 'Xudun', 'Sheikh', 'Gebiley', 'Hargeysa', 'Baki', 'Gebiley', 
                    'Berbera', 'Owdweyne', 'Caynabo', 'Laasqoray', 'Ceerigaabo', 'Borama', 'Burco', 'Laas Caanood', 'Buuhoodle']
        
    if any(ext in district for ext in SomalilandSH):
        
        market_data['SomaliShillingToUSD'] = np.NaN
        
        replace_from = full_data[full_data['District'] == 'Burco'] 
        replace_from.index = replace_from.Date
        market_data['SomalilandShToUSD'] = replace_from['SomalilandShToUSD']
        
    else: 
        market_data['SomalilandShToUSD'] = np.NaN        
        
    return market_data
        


