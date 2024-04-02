import pandas as pd
import numpy as np

from datetime import date, timedelta
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

import matplotlib.pyplot as plt

# Correct Name for the districts:

districts = {"Mogadishu": "Banadir", "Tieglo": "Tayeeglow", "Hudur": "Xudur", "WanlaWeyne": "Wanla Weyn", "Bondhere": "Banadir", "Bardera": "Banadir", "Garbahare": "Garbahaare",  "Afgoye": "Afgooye", 
             "Galkayo": "Gaalkacyo", "Brava": "Baraawe", "BurHakaba": "Buur Hakaba", "RabDhure": "Rab Dhuure", "BuloBurti": "Bulo Burto", "ElBur": "Ceel Buur",  "Badhadhe": "Badhaadhe", "BeletWeyne": "Belet Weyne", 
             "BeletHawa": "Belet Xaawo", "QansahDere": "Qansax Dheere",  "Qoryoley": "Qoryooley", "Adado": "Cadaado",  "Dolo": "Doolow", "Balad": "Balcad", "Dinsor": "Diinsoor", "Jamame": "Jamaame", "Baydhaba": "Baidoa",
             "KutumWarey": "Kurtunwaarey", "Buale": "Bu\'aale",  "Harardhere": "Xarardheere", "BanderBeila": "Bandarbeyla", "AdanYabal": "Adan Yabaal", "Jariban": "Jariiban", "ElDer": "Ceel Dheer", "ElWaq": "Ceel Waaq",  
             "Buhodle": "Buuhoodle", "LasQoray": "Laasqoray", "LasAnod": "Laas Caanood", "Erigabo": "Ceerigaabo", "Kandala": "Qandala", "ElAfwein": "Ceel Afweyn", "Sablaledisctrict": "Sablaale", "Burao": "Burco", 
             "Kismaayo": "Kismayo", "Baydhaba": "Baidoa", "Abdiaziz": "Banadir", "Daynile": "Banadir", "Dharkenley": "Banadir", "Hamar Weyne": "Banadir", "Hamar Jabjab": "Banadir", "Hawl Wadaag": "Banadir", 
             "Heliwa": "Banadir", "Hodan": "Banadir", "Karan": "Banadir", "Kaxda": "Banadir", "Mogadishu City": "Banadir", "Shangaani": "Banadir", "Shibis": "Banadir", "Waaberi": "Banadir", "Wadajir": "Banadir", 
             "Wardhigley": "Banadir", "Yaqshid": "Banadir","Heliwa": "Banadir","Hodan": "Banadir", "Karan": "Banadir", "Kismaayo": "Kismayo", "Baydhaba": "Baidoa", "Mogadishu": "Banadir", "Bulo_burto": "Bulo Burto", 
             "Ceel_waaq": "Ceel Waaq", "Rab_dhuure": "Rab Dhuure", "Ceel_barde": "Ceel Barde", "Qansax_dheere": "Qansax Dheere", "Belet_weyne": "Belet Weyne", "Ceel_dheer": "Ceel Dheer", "Ceel_buur": "Ceel Buur", 
             "Ceel_afweyn": "Ceel Afweyn", "Adan_yabaal": "Adan Yabaal", "Wanla_weyn": "Wanla Weyn", "Buur_hakaba": "Buur Hakaba", "Belet_xaawo": "Belet Xaawo", "Laas_caanood": "Laas Caanood", "Beletweyne": "Belet Weyne", 
             "Dinsoor": "Diinsoor", "Buloburto": "Bulo Burto", "Buale": "Bu'aale", "Garowe": "'Garoowe'", "Marka (Shabelle Hoose)": "Marka", "Lasanod": "Laas Caanood", "Afgoi": "Afgooye", "Beled Weyn": "Belet Weyne", 
             "Borao": "Burco", "Dhusamareb": "Dhuusamarreeb", "El Barde": "Ceel Barde", "El Dhere": "Ceel Dheer", "Elwak": "Ceel Waaq", "Galkayo": "Gaalkacyo", "Hara Dhere": "Xarardheere", "Hargeisa": "Hargeysa", 
             "Lugh": "Luuq", "Qansah Dere": "Qansax Dheere", "Wanle Weyne": "Wanla Weyn", "Zeilac/Lawayacado": "Zeylac", 'CeerigaaboDistrict': 'Ceerigaabo', 'GaldogobDistrict': 'Galdogob','ElBarde': 'Ceel Barde', 
             'Kismaayo': 'Kismayo', 'Garbahaare':'Garbahaarey', 'Hudun':'Xudun','Gardo': 'Qardho', 'Baydhaba': 'Baidoa', 'Odweine': 'Owdweyne','Alula':'Caluula', 'Abudwaq':'Cabudwaaq', 'CeerigaaboDistrict': 'Ceerigaabo', 
             'GaldogobDistrict': 'Galdogob','ElBarde': 'Ceel Barde', 'Kismaayo': 'Kismayo', 'Garbahaare': 'Garbahaarey','Hudun':'Xudun','Gardo': 'Qardho', 'Baydhaba': 'Baidoa', 'Odweine': 'Owdweyne','Alula':'Caluula', 
             'Abudwaq':'Cabudwaaq', "Bulo_burto": "Bulo Burto", "Ceel_waaq": "Ceel Waaq", "Rab_dhuure": "Rab Dhuure",  "Ceel_barde": "Ceel Barde", "Qansax_dheere": "Qansax Dheere", "Baydhaba": "Baidoa", "Belet_weyne": 
             "Belet Weyne", "Ceel_dheer": "Ceel Dheer", "Ceel_buur": "Ceel Buur", "Ceel_afweyn": "Ceel Afweyn",  "Ceel_afweyn": "Ceel Afweyn", "Adan_yabaal": "Adan Yabaal","Wanla_weyn": "Wanla Weyn", 'Harardere': 'Xarardheere',
             "Buur_hakaba": "Buur Hakaba", "Belet_xaawo": "Belet Xaawo", "Laas_caanood": "Laas Caanood",  'Adanyabal': 'Adan Yabaal', 'Abudwak': 'Caabudwaaq','Erigavo': 'Ceerigaabo', 'Merka': 'Marka', 'Beletwein': 'Beledweyne',
             'Mogadishu, Bakara': 'Banadir', 'Beled Hawa': 'Belet Xaawo', 'Caabudwaaq':'Cabudwaaq','Garoowee': 'Garoowe', 'Qorioley':'Qoryooley', 'Togwajale': 'Gebiley', 'Doblei': 'Afmadow','Garooowee': 'Garoowe',
             'Caabudwaaq': 'Cabudwaaq', "'Garoowe'": 'Garoowe', 'Badhan(PL)': 'Badhan','Dhahar(PL)': 'Dhahar',  'Laasqoray(PL)': 'Laasqoray', 'Lasqoray(SL)': 'Laasqoray', 'Boondheere': 'Banadir', 'Bardaale': 'Gebiley', 
             'Aw Dheegle': 'Banadir', 'Cabdulcasiis': 'Banadir','Dayniile': 'Banadir', 'Goldogob':'Galdogob', 'Haliwaa': 'Banadir', 'Kaaraan': 'Banadir', 'Odweyne': 'Owdweyne', 'Odweyne':'Owdweyne','Wardhiigley': 'Banadir',
             'Xamar Jabjab': 'Banadir', 'Xamar Weyne': 'Banadir', 'Yaaqshiid': 'Banadir', "Beletweyne":"BeletWeyne", "Dinsoor":"Diinsoor", "Buloburto":"BuloBurto", "Buale":"Bu'aale", "Garowe":"Garoowe", 
             "Marka(ShabelleHoose)":"Marka", "Lasanod":"LaasCaanood", "Adanyabal":"AdanYabaal", "Afgoi":"Afgooye", "Bardera":"Baardheere", "BeledHawa":"Baardheere","BeledHawa":"BeletXaawo", "BeledWeyn":"BeletWeyne", 
             "Borao":"Burco", "Dhusamareb":"Dhuusamarreeb", "ElBarde":"CeelBarde", "ElDhere":"CeelDheer", "Elwak":"CeelWaaq", "Galkayo":"Gaalkacyo", "HaraDhere":"Xarardheere", "Hargeisa":"Hargeysa", "Hudur":"Xudur",
             "Lugh":"Luuq","Merka":"Marka", 'Erigavo':'Ceerigaabo', 'Abudwak': 'Cabudwaaq', "QansahDere":"QansaxDheere", "WanleWeyne":"WanlaWeyn", "Zeilac/Lawayacado":"Zeylac", 'AdanYabaal': 'Adan Yabaal', 'Lasqoray': 'Laasqoray',
             'Beled Hawa':'Belet Xaawo',  'Burao':'Burco',"Beled Weyn":"BeletWeyne",'CeelWaaq': 'Ceel Waaq', 'Dinsor':'Diinsoor', 'Doblei': 'Doolow','El Barde':'Ceel Barde', 'El Dhere':'Ceel Dheer',  'Gedwaine': 'Geedweyne',
             'Hara Dhere': 'Xarardheere', 'Jamame':'Jamaame', 'LaasCaanood':'Laas Caanood','Mogadishu, Bakara': 'Banadir','Qansah Dere': 'Qansax Dheere','Wanle Weyne':'Wanla Weyn', 'BeletWeyne':'Belet Weyne',
             'Togwajale':'Gebiley','Baydhaba':'Baidoa','Kismaayo': 'Kismayo', 'Ceel Dheere': 'Ceel Dheer', 'Ceel Bur': 'Ceel Buur', 'Garbaharey': 'Garbahaarey', 'Harardheere': 'Xarardheere','Belet Hawa':'Belet Xaawo', 'Belet Xaawa': 'Belet Xaawo', 
             'Dhusa Marreeb': 'Dhuusamarreeb', 'Wanla Weyne': 'Wanla Weyn', 'Bossaasso':'Bossaso', 'Bulo Burti':'Bulo Burto', "Bu'Aale": "Bu'aale", 'Ceel Bur': 'Ceel Buur', 'Ceel Afweyne': 'Ceel Afweyn',  'Diinsor': 'Diinsoor',  
             'Garbaharey':'Garbahaarey', 'Tayeglow': 'Tayeeglow', 'Adan Yabal': 'Adan Yabaal', 'Bandar Beyla': 'Bandarbeyla', 'Bendar Beyla':'Bandarbeyla', 'Wajid': 'Waajid', 'Boroma':'Borama', 'Brawa': 'Baraawe', 'Dusamared': 'Dhuusamareeb'}



def correct_districts(df_district):
    return df_district.replace(districts)


regions = {'Banaadir': 'Banadir'}

def correct_regions(df_region):
    return df_region.replace(regions)



# Market Data Cleaning: CHOOSE BEST MARKET IN SHAPEFILE

def aggregate_best_market(market_dataframe, agg_level):

    # Good Market Prices
    features = ['Red Sorghum Price', 'Wheat Flour Price', 'Sugar Price', 'Vegetable Oil Price', 'Camel Milk Price', 
                'Tea Leaves Price','Salt Price', 'Cowpeas Price', 
            'Water Drum Price', 'Cattle Price', 'Camel Price', 'Goat Price', 'SomaliShillingToUSD', 'SomalilandShToUSD']
    
    # Prepare the search
    market_dataframe = market_dataframe[['Date', 'Market', agg_level] + features].drop_duplicates(subset = ['Market', 'Date']).copy()

    market_dataframe.rename(columns = {'RedSorghum1kg': 'Red Sorghum Price', 'WheatFlour1kg': 'Wheat Flour Price', 'Cowpeas': 'Cowpeas Price',
                             'Sugar': 'Sugar Price', 'TeaLeaves': 'Tea Leaves Price', 'Salt': 'Salt Price', 'VegetableOil1litre': 'Vegetable Oil Price',
                             'GoatLocalQuality': 'Goat Price', 'CattleLocalQuality': 'Cattle Price', 'CamelLocalQuality': 'Camel Price',
                             'FreshCamelMilk1litre': 'Camel Milk Price', 'WaterDrum': 'Water Drum Price'}, inplace=True)

    # market_dataframe = market_dataframe[market_dataframe.District == 'Banadir']

    ord_enc = OrdinalEncoder()

    # Initialize an empty DataFrame to store the results
    final_dataframe = pd.DataFrame()


    for zone in np.unique(market_dataframe[agg_level]):    

        # print(zone)
        this_zone = market_dataframe[market_dataframe[agg_level] == zone].fillna(0)
        this_zone = this_zone[this_zone.Date >= '2009']
        zone_markets = np.unique(this_zone.Market)

        # For each district save the best feature column
        best_market_data = this_zone[this_zone['Market'] == zone_markets[0]][['Date', agg_level, 'Market']].reset_index(drop=True)

        # print('Markets in ' + agg_level + ' = ', zone_markets)
        # print('-----------------------------------------------')

        # Iterate through the features:

        for feature in this_zone.columns[5:]:
            ord_variance = np.array([])

            # Iterate through markets
            for market in zone_markets:

                # Select market and ordinal encode values and then calculate variance
                check_market = this_zone[this_zone['Market'] == market]
                market_enc = ord_enc.fit_transform(np.unique(np.array(check_market[feature])).reshape(-1, 1)).astype(int)
                variance = np.var(market_enc.flatten())

                # print(feature)
                # print(market)
                # print(this_zone[this_zone['Market'] == market]['Market Type'].iloc[0])
                # print('Ordinal Variance =', variance)

                ord_variance = np.append(ord_variance, variance)

            # Select the feature that has the maximum variance among markets
            max_index = np.argmax(ord_variance)
            market_best_feature = zone_markets[max_index]

            # print(market_best_feature)

            # Append the best feature to the district data
            best_market_feature = this_zone[(this_zone['Market'] == market_best_feature)][feature].reset_index(drop=True)
            best_market_data = pd.concat([best_market_data, best_market_feature], axis=1)

            # print('selected:', feature, 'in', market_best_feature, 'for:', zone)
            # print('-------------------------------------------------')

        # Concatenate district data to the final dataframe
        final_dataframe = pd.concat([final_dataframe, best_market_data], axis=0).reset_index(drop=True)

    final_dataframe = final_dataframe.replace(0, np.nan)
    
    return final_dataframe




# Aggregate PRMN data to Region, District or Livelihood:

def agg_to_shapefile(df, conflict_intersected, market_intersected,  agg_level, scale):

    # Assume 0 if no event was reported
    Weekly_IDP = df[['Date', agg_level, 'IDP_Drought', 'IDP_Conflict']].groupby([agg_level]).resample(scale, label='left', closed = 'left', on='Date').sum().drop(columns=agg_level).reset_index()
    Weekly_Conflict = conflict_intersected[['Date', agg_level, 'interaction', 'Fatalities']].groupby([agg_level]).resample(scale, label='left', closed = 'left', on='Date').sum().drop(columns=agg_level).reset_index()

    # Choose best market from the agg level:
    from Data_Aggregation_Functions import aggregate_best_market

    market_agg = aggregate_best_market(market_intersected,agg_level)


    # Market prices are given in monthly averages so we aggregate to the middle of the month
    if scale == 'W-MON':
        market_agg.Date = market_agg.Date - timedelta(15)

    Weekly_Market = market_agg.groupby([agg_level]).resample(scale, label='left', closed = 'left', on='Date').mean().reset_index()
    

    Agg_df =  Weekly_IDP.merge(Weekly_Market, how='left', on=[agg_level, 'Date']).merge(Weekly_Conflict, how='left', on=[agg_level, 'Date'])

    return Agg_df.replace(0, np.nan)


# Plot Choropleth maps

def plot_maps(data, map, agg_level, target):
       
    nan_counts = data.groupby(agg_level)[target].count()
    sum_counts = data.groupby(agg_level)[target].sum()

    counts_plot = map.merge(nan_counts.reset_index(), on=agg_level)
    sum_plot = map.merge(sum_counts.reset_index(), on=agg_level)

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 8))
    fig.tight_layout()

    # Plot 2
    ax[0].axis('off')
    ax[0].set_title(target + ' Count Points Data', fontdict={'fontsize': '20', 'fontweight' : '3'})
    cmap = plt.cm.get_cmap('Blues_r')
    vmin1 = min(counts_plot[target])
    vmax1 = max(counts_plot[target])
    sm1 = plt.cm.ScalarMappable(cmap=cmap.reversed(), norm=plt.Normalize(vmin=vmin1, vmax=vmax1))
    sm1.set_array([]) 
    cbar = fig.colorbar(sm1, ax=ax[0], fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=12) 
    counts_plot.plot(column=target, cmap=cmap.reversed(), linewidth=0.8, ax=ax[0], edgecolor='#007693')

    # Plot 3
    ax[1].axis('off')
    ax[1].set_title(target + ' Sum', fontdict={'fontsize': '20', 'fontweight' : '3'})
    cmap = plt.cm.get_cmap('OrRd_r')
    vmin1 = min(sum_plot[target])
    vmax1 = max(sum_plot[target])
    sm2 = plt.cm.ScalarMappable(cmap=cmap.reversed(), norm=plt.Normalize(vmin=vmin1, vmax=vmax1))
    sm2.set_array([]) 
    cbar = fig.colorbar(sm2, ax=ax[1], fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=12)
    sum_plot.plot(column=target, cmap=cmap.reversed(), linewidth=0.8, ax=ax[1], edgecolor='#007693')