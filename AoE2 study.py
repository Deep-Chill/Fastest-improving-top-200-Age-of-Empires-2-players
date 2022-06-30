import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import time
import aoe2netapi as aoe
import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

API = aoe.API()

starttime = time.time()

df = pd.read_csv('AoE2_list_of_top_10000_players.csv')

df = df[['profile_id', 'name']]
df['max_rating'] = 0
df['min_rating'] = 0
df['date_of_max_rating'] = 0
df['date_of_min_rating'] = 0
df['difference_in_rating'] = 0

counter = 0

for i in df.head(200)['profile_id']:
    counter += 1
    print(counter)
    all_ratings = []
    list_of_ratings = API.get_rating_history(profile_id=i, count=5000)
    if len(list_of_ratings) < 200:
        continue
    else:
        for j in list_of_ratings[:-100]:
            if dt.datetime.fromtimestamp(j.get('timestamp')) > dt.datetime.fromtimestamp(1590973200):
                all_ratings.append(j.get('rating'))
            else:
                pass
        max_rating = max(all_ratings)
        min_rating = min(all_ratings)

        df.loc[df['profile_id'] == i, 'max_rating'] = max_rating
        df.loc[df['profile_id'] == i, 'min_rating'] = min_rating
        '''get the date of the max and min rating'''
        for j in list_of_ratings[:-100]:
            if dt.datetime.fromtimestamp(j.get('timestamp')) > dt.datetime.fromtimestamp(1590973200):
                if j.get('rating') == max_rating:
                    df.loc[df['profile_id'] == i, 'date_of_max_rating'] = dt.datetime.fromtimestamp(j.get('timestamp'))
                elif j.get('rating') == min_rating:
                    df.loc[df['profile_id'] == i, 'date_of_min_rating'] = dt.datetime.fromtimestamp(j.get('timestamp'))
                else:
                    pass
            else:
                pass

        '''get the difference in rating'''
        df.loc[df['profile_id'] == i, 'difference_in_rating'] = max_rating - min_rating

df.head(200).to_csv('test_aoe3.csv')
endtime = time.time()

print(endtime - starttime)

path2 = r'C:\Users\Welcome\PycharmProjects\CompetitiveProgramming\Pandas practice\test_aoe3.csv'

df = pd.read_csv(path2)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df[df['max_rating'] != 0]

print(df.sort_values(by='min_rating', ascending=True).head(10))
