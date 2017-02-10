
import requests
# https://github.com/search?q=brewerydb+key&type=Code&utf8=%E2%9C%93
# KEY='da506aecce47e548b1877f8c6f9be793'
# KEY='b7336846d8cc7073b22ed905911c5f3b'
# KEY='c05155a3d80221ed8d3f3e4ebe231a17'
# KEY='6dab466c8f0979f11e35908c1b6671ff'
# KEY='37f05932e468ea014afabb1d166a6f99'
# KEY='7ad2c83100277e6fe89592046aae718c'
# KEY='fef981024ebb8b79b69f3ef9827b166b'
# KEY='179b4ca157d29bca1a09a4e7e013f5f2'
# KEY='8ae5e9d2cf9463f56dfbca4a4abef12a'
# KEY='5f529a9afee75cf72af3830047337534'
# KEY='179b4ca157d29bca1a09a4e7e013f5f2'
# KEY='38305e50f0d456cbb9b71ed5c689feac'
# KEY='6495f3ff13746e6935cd6e148f69c030'
# KEY='506bb9b48659b2737456b6f9e0966aa8'
# KEY+'25676e3b499c2bc9e35b75ec2632c810'
# KEY='dd604aa40606566d3f9fcba2c8ff7d8c'
# KEY='be63b9e7adb442b18524e654c8a59ed7'
# KEY='98946c0a780132c554b3af67a95b1712'
# KEY='3fb832160850da3fb006f7009a11cbd2'
# KEY='05ab45a0b401dffdfa9d8592006e3b6d'
# KEY='da50066428563d5c893a88431c968943'
# KEY='2fbdec68dd2a53cc1eb4689cbeb3fdf6'
# KEY='e22feee3d4f0adaf6576ea93d6038bbb'
# KEY='b44ee2dd41d99574d23d815835514d55'
# KEY='47f25f72907f1924061a1ee9b57d6f10'
https://github.com/search?p=7&q=brewerydb+key&type=Code&utf8=%E2%9C%93
KEY='a956af587b434c4c89ef18c7bbd2fac9'


result2 = []
url = "http://api.brewerydb.com/v2/breweries/?key={0}&withLocations=Y".format(KEY)
#initial load
r = requests.get(url).json()
if 'data' in r:
  result2 += r['data']
  num_pages = r['numberOfPages']
for i in range(1, num_pages+1):
  r = requests.get(url, params={'p':i}).json()
  if 'data' in r:
    result2 += r['data']
  if r['status'] == 'failure':
    print('fail')
    break

import pandas as pd
t = pd.DataFrame(result2)
t.to_csv('/Users/Ben_Pleasanton/Desktop/beer/breweries.csv', index=False,header=True)

result2 = []
url = "http://api.brewerydb.com/v2/beers/?key={0}".format(KEY)
#initial load
r = requests.get(url).json()
if 'data' in r:
  result2 += r['data']
  num_pages = r['numberOfPages']
for i in range(1, num_pages+1):
  r = requests.get(url, params={'p':i}).json()
  if 'data' in r:
    result2 += r['data']
  if r['status'] == 'failure':
    print('fail')
    break

import pandas as pd
t = pd.DataFrame(result2)
t.to_csv('/Users/Ben_Pleasanton/Desktop/beer/beers.csv', index=False,header=True)






result3=[]
for i in t.id.tolist():
  url = "http://api.brewerydb.com/v2/beer/{0}/breweries?key={1}".format(i,KEY)
  r = requests.get(url).json()
  if 'data' in r:
    for b in r['data']:
        c = b
        c['beer_id'] = i
        result3.append(c)

j = pd.DataFrame(result3)
j.to_csv('/Users/Ben_Pleasanton/Desktop/beer/beer_breweries.csv', index=False,header=True)


# result3=[]
# for i in t.id.tolist():
#   url = "http://api.brewerydb.com/v2/beer/{0}/ingredients?key={1}".format(i,KEY)
#   r = requests.get(url).json()
#   if 'data' in r:
#     for b in r['data']:
#         c = b
#         c['beer_id'] = i
#         result3.append(c)

# j = pd.DataFrame(result3)
# j.to_csv('/Users/Ben_Pleasanton/Desktop/beer/beer_ingredients.csv', index=False,header=True)

TO DO - pull Events


from geoluigi import LuigiMap
import shapely.geometry as shp
import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt

breweries = pd.DataFrame.from_csv('breweries.csv',index_col=None)
beers = pd.DataFrame.from_csv('beers.csv',index_col=None)
bb_map = pd.DataFrame.from_csv('beer_breweries.csv',index_col=None)

beers = pd.merge(beers,bb_map,how='left',left_on='id',right_on='beer_id',suffixes=['','_map'])
beers = pd.merge(beers,breweries,how='left',left_on='name_map',right_on='name',suffixes=['','_brewery'])

for b in beers.index.tolist():
    try:  beers.loc[b,'glass'] = literal_eval(beers.at[b,'glass'])['name']
    except: beers.loc[b,'glass'] = None
    try:  beers.loc[b,'labels'] = literal_eval(beers.at[b,'labels'])['icon']
    except: beers.loc[b,'labels'] = None
    try:  beers.loc[b,'style_name'] = literal_eval(beers.at[b,'style'])['shortName']
    except: continue
    try:  beers.loc[b,'category_name'] = literal_eval(beers.at[b,'style'])['category']['name']
    except: continue
    try:  beers.loc[b,'desc_name'] = literal_eval(beers.at[b,'style'])['description']
    except: continue


locations = []
for i in breweries.index.tolist():
  status = breweries.at[i,'statusDisplay']
  name = breweries.at[i,'name']
  try: img = literal_eval(breweries.at[i,'images'])['icon']
  except: img = None
  established = breweries.at[i,'established']
  try: locs = literal_eval(breweries.at[i,'locations'])
  except: locs = []
  for j in locs:
    lat = None
    lon = None
    locality = None
    zipcode = None
    location_type = None
    is_closed = None
    street = None
    region = None
    in_planning = None
    is_primary = None
    if 'longitude' in j:
      if 'latitude' in j:
        lon = j['longitude']
        lat = j['latitude']
    if 'inPlanning' in j:
      in_planning = j['inPlanning']
    if 'locality' in j:
      locality = j['locality']
    if 'postalCode' in j:
      zipcode = j['postalCode']
    if 'locationTypeDisplay' in j:
      location_type = j['locationTypeDisplay']
    if 'isClosed' in j:
      is_closed = j['isClosed']
    if 'isPrimary' in j:
      is_primary = j['isPrimary']
    if 'streetAddress' in j:
      street = j['streetAddress']
    if 'region' in j:
      region = j['region']
    if 'inPlanning' in j:
      in_planning = j['inPlanning']
    r = [name,status,img,established,lat,lon,locality,zipcode,location_type,is_closed,street,region,in_planning,is_primary]
    locations.append(r)

locations = pd.DataFrame(locations,columns=['name','status','img','established','lat','lon','locality','zipcode','location_type','is_closed','street','region','in_planning','is_primary'])
locations.to_csv('locations.csv',header=True,index=False)
import json
jlocations = { "type": "FeatureCollection",
               "features": []}
for i in locations.index.tolist():
  feature = { "type":"Feature",
              "geometry": {"type":"Point",
                           "coordinates":[locations.at[i,'lon'],locations.at[i,'lat']]},
              "properties":{"name":locations.at[i,'name'],
                            "status":locations.at[i,'status'],
                            "img":locations.at[i,'img'],
                            "established":locations.at[i,'established'],
                            "location_type":locations.at[i,'location_type'],
                            "is_closed":locations.at[i,'is_closed']}}
  jlocations['features'].append(feature)

with open('locations.geojson','w') as f:
  f.write(json.dumps(jlocations))

add number of bars established as comparison
note that these are breweries that are still open?!

# established.tsv
established = locations.dropna(subset=['established'])
established = established[~established['established'].isin(['NULL'])]
established = established.groupby(['established']).count() #location_type
established = established.reset_index()[['established','name']]
established.columns = ['date','Established Each Year']
established['Established Each Year'] = established['Established Each Year'].astype(int)
established['date'] = established['date'].astype(int)
# established['Cumulative Established'] = 0
# for i in established.index.tolist():
#   y = established.at[i,'date']
#   established.loc[i,'Cumulative Established'] = established[established['date'] <= y]['Established Each Year'].sum()


# typs = ['Cidery', 'Meadery']
# for t in typs:
#   temp = locations.dropna(subset=['established'])
#   temp = temp[temp['location_type'].isin([t])]
#   temp = temp[~temp['established'].isin(['NULL'])]
#   temp = temp.groupby(['established']).count().reset_index()[['established','name']]
#   temp.columns = ['date',t]
#   temp['date'] = temp['date'].astype(int)
#   temp[t] = temp[t].astype(int)
#   established = pd.merge(established,temp,how='left',on='date')


temp = locations.dropna(subset=['established'])
temp = temp[temp['location_type'].isin(['Cidery', 'Meadery'])]
temp = temp[~temp['established'].isin(['NULL'])]
temp = temp.groupby(['established']).count().reset_index()[['established','name']]
temp.columns = ['date','']
temp['date'] = temp['date'].astype(int)
temp[''] = temp[''].astype(int)
established = pd.merge(established,temp,how='left',on='date')



temp = locations.dropna(subset=['established'])
temp = temp[temp['location_type'].isin(['Restaurant/Ale House','Brewpub'])]
temp = temp[~temp['established'].isin(['NULL'])]
temp = temp.groupby(['established']).count().reset_index()[['established','name']]
temp.columns = ['date','Ale House / Brew Pub']
temp['date'] = temp['date'].astype(int)
temp['Ale House / Brew Pub'] = temp['Ale House / Brew Pub'].astype(int)
established = pd.merge(established,temp,how='left',on='date')


temp = locations.dropna(subset=['established'])
temp = temp[temp['location_type'].isin(['Micro Brewery', 'Nano Brewery', 'Tasting Room'])]
temp = temp[~temp['established'].isin(['NULL'])]
temp = temp.groupby(['established']).count().reset_index()[['established','name']]
temp.columns = ['date','Micro / Nano Brewery']
temp['date'] = temp['date'].astype(int)
temp['Micro / Nano Brewery'] = temp['Micro / Nano Brewery'].astype(int)
established = pd.merge(established,temp,how='left',on='date')


temp = locations.dropna(subset=['established'])
temp = temp[temp['location_type'].isin(['Production Facility', 'Macro Brewery'])]
temp = temp[~temp['established'].isin(['NULL'])]
temp = temp.groupby(['established']).count().reset_index()[['established','name']]
temp.columns = ['date','Macro / Production Brewery, Meadery, Cidery']
temp['date'] = temp['date'].astype(int)
temp['Macro / Production Brewery, Meadery, Cidery'] = temp['Macro / Production Brewery, Meadery, Cidery'].astype(int)
established = pd.merge(established,temp,how='left',on='date')


established = established.fillna(0)
for col in established.columns.tolist():
  established[col] = established[col].astype(int)

established = established[established['date']>=1800]
established = established[established['date']<2017]

established.to_csv('established.tsv',header=True,index=False,sep='\t')

################################
################################
################################
style
servingTemperatureDisplay
nameDisplay                   object
originalGravity
glass                         object
glasswareId                  float64
ibu                          float64
isOrganic


beers['glass'].value_counts().to_csv('glasses.csv')
beers[['name','ibu','abv','style_name']].to_csv('beer_ibu_style.csv',index=False,header=True)

beers.style_name.value_counts().reset_index().to_csv('styles.csv',index=False,header=True)



stream = beers.dropna(subset=['style_name','established'])
stream = stream.groupby(['style_name','established']).count().reset_index()
stream['established'] = stream['established'].astype(int)
stream = stream[['style_name','name','established']]
stream.columns = ['key','value','date']
stream = stream[stream['date']>=1980]
stream = stream[stream['date']<2017]


# f = stream.key.value_counts().reset_index()
# f = f[f['key']>35]
# f = f['index'].tolist()
f = ['American Pale','American Brown','Blonde','American IPA','Brown Porter','Hefeweizen','Amber','Imperial IPA','American Stout','Belgian Tripel','American Lager','Fruit Beer','Witbier','Kölsch','Oatmeal Stout','Imperial Red','Spice Beer','Belgian Dubbel','German Pilsener','Wheat Ale','Belgian Blonde','Saison','American Imperial Stout','Specialty']

stream = stream[stream['key'].isin(f)]
#NEED TO MAKE EACH SERIES STARTS AT THE SAME YEAR AND ENDS AT SAME YEAR
years = [i for i in range(1980,2017)]
dfs = []
for s in f:
  temp_df = stream[stream['key']==s]
  temp_df = temp_df.merge(how='right', on='date', right = pd.DataFrame({'date':range(1980,2017)})).sort(columns='date').reset_index().drop(['index'], axis=1)
  temp_df['key']=s
  dfs.append(temp_df)

stream = pd.concat(dfs)
stream = stream[['key','value','date']]
stream['date'] = stream['date'].astype(int)
stream['value'] = stream['value'].fillna(0)
stream.to_csv('style_stream.csv',index=False,header=True)


# TO DO - Heatmap
# from geoluigi import LuigiMap
# import shapely.geometry as shp
# import pandas as pd
# from ast import literal_eval
# df = pd.DataFrame.from_csv('breweries.csv',index_col=None)
# locs = []
# for i in df.index.tolist():
#     try: l = literal_eval(df.at[i,'locations'])
#     except: l = []
#     for j in l:
#         if 'longitude' in j:
#             if 'latitude' in j:
#                 locs.append([df.at[i,'name'],j['longitude'],j['latitude']])

# loc = pd.DataFrame(locs,columns=['name','x','y'])
# m=LuigiMap()
# loc['t'] = 0.01
# m.scatter(loc,'x','y',popup_col='name',fill_opacity=1,value_col='t')
# m.save('breweries.html')

TO DO - Heatmap timeseries using established

# with open(f,'w') as g:
#     f.write(str(result2))

# url = "http://api.brewerydb.com/v2/breweries?key={0}&withLocations=Y".format(KEY);r = requests.get(url).json();r

# years = [x for x in range(1800,2017)]
# result2 = []
# for year in years:
#     url = "http://api.brewerydb.com/v2/breweries/?key={0}&withLocations=Y&established={1}".format(KEY,year)
#     #initial load
#     r = requests.get(url).json()
#     if 'data' in r:
#       result2 += r['data']
#       num_pages = r['numberOfPages']
#     for i in range(1, num_pages+1):
#       r = requests.get(url, params={'p':i}).json()
#       if 'data' in r:
#         result2 += r['data']
#       if r['status'] == 'failure':
#         print('fail')
#         break



def converttoFloat(inputNum):
    try:
        flnum = float(inputNum)
    except:
        flnum = 0.0


