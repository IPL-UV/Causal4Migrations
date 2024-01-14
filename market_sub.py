import pandas as pd
import numpy as np 

pd.options.mode.chained_assignment = None  # default='warn'


def market_sub(district, market_data, full_data):
    

    if district == 'Bandarbeyla':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Camel Price'] = replace_from['Camel Price']
        
    if district == 'Caluula':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
    
    if district == 'Qandala':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
    
    if district == 'Laasqoray':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]

        
    if district == 'Caynabo':
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']    
        
    if district == 'Ceel Afweyn':
        
        replace_from = full_data[full_data['District'] == 'Ceerigaabo']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data['Camel Price'] = replace_from['Camel Price'] 
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']  
        market_data['Water Drum Price'] = replace_from['Water Drum Price']  
        market_data['Goat Price'][market_data['Goat Price'] > 2e+6] = None   
    
    if district == 'Ceerigaabo':
        
        market_data['Goat Price'][market_data['Goat Price'] > 2e+6] = None   
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data['Camel Price'] = replace_from['Camel Price'] 
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']  
        market_data['Water Drum Price'] = replace_from['Water Drum Price']  
    
    if district == 'Berbera':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
    if district == 'Gebiley':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
    

    if district == 'Baki':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
    
    if district == 'Hargeysa':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
    if district == 'Sheikh':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
    
    if district == 'Owdweyne':
        
        replace_from = full_data[full_data['District'] == 'Borama']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
    
    
    if district == 'Burco':

        replace_from = full_data[full_data['District'] == 'Ceerigaabo']
        replace_from.index = replace_from.Date 
        market_data['Salt Price'] = replace_from['Salt Price']  
    
        
    if district == 'Taleex':

        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:] 
                
        
    if district == 'Xudun':
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        
        market_data['Camel Price'] = replace_from['Camel Price']    
        market_data['Water Drum Price'] = replace_from['Water Drum Price']    
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']    
    
    if district == 'Bandarbeyla':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]

    if district == 'Hobyo':
        
        replace_from = full_data[full_data['District'] == 'Xarardheere']
        replace_from.index = replace_from.Date
        
        market_data['Camel Price'] = replace_from['Camel Price']    
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']    
        market_data['Water Drum Price'] = replace_from['Water Drum Price']   
        
        
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
    
    if district == 'Cadaado':
        
        replace_from = full_data[full_data['District'] == 'Dhuusamarreeb']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        market_data['Cattle Price'] = None
        
        
    if district == 'Galdogob':
        
        replace_from = full_data[full_data['District'] == 'Burtinle']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Tea Leaves Price'] = replace_from['Tea Leaves Price']    
        market_data['Camel Price'] = replace_from['Camel Price']    
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']    
        market_data['Water Drum Price'] = replace_from['Water Drum Price']    
        market_data['Goat Price'][market_data['Goat Price'] > 3e+6] = None   
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
    
    if district == 'Gaalkacyo':
        
        replace_from = full_data[full_data['District'] == 'Burtinle']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Tea Leaves Price'] = replace_from['Tea Leaves Price']    
        market_data['Camel Price'] = replace_from['Camel Price']    
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']    
        market_data['Water Drum Price'] = replace_from['Water Drum Price']    
        market_data['Goat Price'][market_data['Goat Price'] > 3e+6] = None   
        

    if district == 'Burtinle':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Tea Leaves Price'] = replace_from['Tea Leaves Price']    
        market_data['Camel Price'] = replace_from['Camel Price']    
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']    
        market_data['Water Drum Price'] = replace_from['Water Drum Price']    
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Goat Price'][market_data['Goat Price'] > 3e+6] = None

    
    if district == 'Eyl':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Tea Leaves Price'] = replace_from['Tea Leaves Price']    
        market_data['Camel Price'] = replace_from['Camel Price']    
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']    
        market_data['Water Drum Price'] = replace_from['Water Drum Price']    
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Goat Price'][market_data['Goat Price'] > 3e+6] = None
    
    if district == 'Qardho':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
    if district == 'Iskushuban':
        
        replace_from = full_data[full_data['District'] == 'Bossaso']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        
    if district == 'Buuhoodle':
        
        replace_from = full_data[full_data['District'] == 'Laas Caanood']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']    
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
    
    if district == 'Laas Caanood':
        
        replace_from = full_data[full_data['District'] == 'Garoowe']
        replace_from.index = replace_from.Date
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']    
    
    if district == 'Cabudwaaq':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
    

    if district == 'Dhuusamarreeb':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
    
    if district == 'Cadale':
        replace_from = full_data[full_data['District'] == 'Ceel Dheer']
        replace_from.index = replace_from.Date
        
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn']
        replace_from.index = replace_from.Date
        market_data['Camel Price'] = replace_from['Camel Price']
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        market_data['Wheat Flour Price'] = replace_from['Wheat Flour Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
    
    if district == 'Adan Yabaal':
        
        replace_from = full_data[full_data['District'] == 'Ceel Dheer']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
    
    if district == 'Ceel Dheer':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
    
    if district == 'Xarardheere':
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
        
        market_data['Red Sorghum Price'][market_data.index > '2020'][market_data['Red Sorghum Price'] > 18000] = None
    
    if district == 'Balcad':
        
        replace_from = full_data[full_data['District'] == 'Marka']
        replace_from.index = replace_from.Date
        
        market_data['Tea Leaves Price'][market_data['Tea Leaves Price'] > 90000.0] = None
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn']
        replace_from.index = replace_from.Date
        
        market_data['Camel Price'] = replace_from['Camel Price']
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        
    if district == 'Xudur':
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date 
        market_data = replace_from.iloc[:,16:]
        
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 100000.0] = None
    
    if district == 'Waajid':
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date 
        market_data = replace_from.iloc[:,16:]
        
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 100000.0] = None
    
    if district == 'Luuq':
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date 
        market_data = replace_from.iloc[:,16:]
        
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 100000.0] = None
    
    if district == 'Doolow':
        
        replace_from = full_data[full_data['District'] == 'Qansax Dheere'] 
        replace_from.index = replace_from.Date 
        market_data = replace_from.iloc[:,16:]
    
    
    if district == 'Belet Xaawo':
        
        replace_from = full_data[full_data['District'] == 'Ceel Waaq'] 
        replace_from.index = replace_from.Date 
        market_data = replace_from.iloc[:,16:]
        
        
    if district == "Badhaadhe":
        
        replace_from = full_data[full_data['District'] == 'Afmadow']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        replace_from = full_data[full_data['District'] == 'Baardheere'] 
        replace_from.index = replace_from.Date        
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
    
    if district == "Afmadow":
            
        replace_from = full_data[full_data['District'] == 'Baardheere'] 
        replace_from.index = replace_from.Date        
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
        
    if district == "Jamaame":
        
        replace_from = full_data[full_data['District'] == 'Jilib']
        replace_from.index = replace_from.Date
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
                
        replace_from = full_data[full_data['District'] == 'Baraawe'] 
        replace_from.index = replace_from.Date        
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        
    
    if district == "Saakow":
        
        replace_from = full_data[full_data['District'] == 'Baardheere']
        replace_from.index = replace_from.Date
        
        replace_from['Goat Price'][replace_from['Goat Price'] > 1.6e+6]  = None
        
        market_data = replace_from.iloc[:,16:]
                
        replace_from = full_data[full_data['District'] == 'Diinsoor'] 
        replace_from.index = replace_from.Date
        market_data['Water Drum Price'] = replace_from['Water Drum Price']   
        
        
        market_data['Goat Price'][market_data['Goat Price'] > 2e+6]  = None
        
        
        
    if district == "Bu'aale":
        
        replace_from = full_data[full_data['District'] == 'Jilib']
        replace_from.index = replace_from.Date
        
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        
        replace_from = full_data[full_data['District'] == 'Diinsoor']
        replace_from.index = replace_from.Date
        
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        
    
    if district == 'Jilib':
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
    
    if district == 'Marka':
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        
        
    if district == 'Baraawe':
        
        replace_from = full_data[full_data['District'] == 'Jilib']
        replace_from.index = replace_from.Date
        
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
    
    
    if district == 'Banadir':
        
        replace_from = full_data[full_data['District'] == 'Marka']
        replace_from.index = replace_from.Date
        
        market_data = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        
    if district == 'Jowhar':
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn']
        replace_from.index = replace_from.Date
        
        market_data = replace_from.iloc[:,16:]
    
    
    if district == 'Jalalaqsi':
        
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        
    if district == 'Belet Weyne':
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
    
    if district == 'Ceel Buur':
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
    if district == 'Bulo Burto':
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
               
        
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
    
    if district == 'Ceel Barde':
        replace_from = full_data[full_data['District'] == 'Baidoa']
        replace_from.index = replace_from.Date
                
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        market_data['Cattle Price'] = replace_from['Cattle Price']
        
        
    if district == 'Rab Dhuure':
        replace_from = full_data[full_data['District'] == 'Ceel Barde']
        replace_from.index = replace_from.Date
        
        market_data = replace_from.iloc[:,16:]
                
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        
    
    if district == 'Tayeeglow':

        replace_from = full_data[full_data['District'] == 'Ceel Barde']
        replace_from.index = replace_from.Date
        
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        
        market_data['Goat Price'][market_data['Goat Price'] > 2.2e+6] =None
        
        replace_from = full_data[full_data['District'] == 'Belet Weyne']
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        
    
    if district == 'Kurtunwaarey':
        
        replace_from = full_data[full_data['District'] == 'Baraawe']
        replace_from.index = replace_from.Date
        
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 70000.0] =None
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
    
    if district == 'Jariiban':
        
        # Eliminate anomalies:
        market_data['Red Sorghum Price'][market_data['Red Sorghum Price'] > 100000] = None
        market_data['Tea Leaves Price'][market_data['Tea Leaves Price'] < 1000] = None
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 190000.0] = None
        
        # Replace poor quality data
        replace_from = full_data[full_data['District'] == 'Garoowe'] 
        replace_from.index = replace_from.Date
        
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        market_data['Camel Price'] = replace_from['Camel Price']        
        market_data['Cattle Price'] = replace_from['Cattle Price']     
        
    if district == 'Baidoa':
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 100000.0] = None
        
    
    if district == 'Kismayo':
        
        replace_from = full_data[full_data['District'] == 'Baraawe'] 
        replace_from.index = replace_from.Date
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        market_data['SomalilandShToUSD'] = np.NaN
        
        
    if district == 'Baardheere':

        replace_from = full_data[full_data['District'] == 'Diinsoor'] 
        replace_from.index = replace_from.Date
        market_data['Water Drum Price'] = replace_from['Water Drum Price']   
        
    if district == 'Lughaye':

        replace_from = full_data[full_data['District'] == 'Borama'] 
        replace_from.index = replace_from.Date
        market_data['Camel Price'] = replace_from['Camel Price'] 
        market_data['Cattle Price'] = None
        
    if district == 'Zeylac':
        
        replace_from = full_data[full_data['District'] == 'Borama'] 
        replace_from.index = replace_from.Date
        market_data['Camel Price'] = replace_from['Camel Price'] 
        market_data['Cattle Price'] = None
    
    if district == 'Qoryooley':
        replace_from = full_data[full_data['District'] == 'Wanla Weyn'] 
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']    
        
    
    if district == 'Buur Hakaba':
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        market_data['Vegetable Oil Price'] = replace_from['Vegetable Oil Price']
        
        
        replace_from = full_data[full_data['District'] == 'Baidoa'] 
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']
        
    if district == 'Sablaale':
        
        replace_from = full_data[full_data['District'] == 'Baraawe'] 
        replace_from.index = replace_from.Date
        market_data = replace_from.iloc[:,16:]
        
        
    if district == 'Afgooye':
        
        replace_from = full_data[full_data['District'] == 'Balcad'] 
        replace_from.index = replace_from.Date
        
        market_data['Red Sorghum Price'] = replace_from['Red Sorghum Price']
        market_data['Vegetable Oil Price'] = replace_from['Vegetable Oil Price']
        market_data['Goat Price'] = replace_from['Goat Price']
        market_data['Sugar Price'] = replace_from['Sugar Price']
        market_data['Camel Milk Price'] = replace_from['Camel Milk Price']
        market_data['Tea Leaves Price'] = replace_from['Tea Leaves Price']
        market_data['Vegetable Oil Price'][market_data['Vegetable Oil Price'] > 100000.0] = None       
        
        replace_from = full_data[full_data['District'] == 'Marka'] 
        replace_from.index = replace_from.Date
        market_data['SomaliShillingToUSD'] = replace_from['SomaliShillingToUSD']
        market_data['Water Drum Price'] = replace_from['Water Drum Price']
        market_data['Cowpeas Price'] = replace_from['Cowpeas Price']
        
        replace_from = full_data[full_data['District'] == 'Wanla Weyn'] 
        replace_from.index = replace_from.Date
        
        market_data['Cattle Price'] = replace_from['Cattle Price']
        market_data['Camel Price'] = replace_from['Camel Price']      
        
    
    if district == 'Garbahaarey':
        replace_from = full_data[full_data['District'] == 'Qansax Dheere'] 
        replace_from.index = replace_from.Date
        
        market_data = replace_from.iloc[:,16:]
        
    
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
        

