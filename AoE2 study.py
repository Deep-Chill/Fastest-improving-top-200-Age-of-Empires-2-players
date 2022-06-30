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

        # for j in list_of_ratings[:-100]:
        #     if j.get('rating') == max_rating:
        #         df.loc[df['profile_id'] == i, 'date_of_max_rating'] = dt.datetime.fromtimestamp(j.get('timestamp'))
        #     elif j.get('rating') == min_rating:
        #         df.loc[df['profile_id'] == i, 'date_of_min_rating'] = dt.datetime.fromtimestamp(j.get('timestamp'))
        #     else:
        #         pass
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



    # rating_history = API.get_rating_history(profile_id=i)
    # print(i, rating_history)

# list_of_ratings = API.get_rating_history(profile_id=df['profile_id'][0])
# '''get the value of rating from the rating history of the first player'''
# for i in list_of_ratings:
#     print(list_of_ratings.get('rating'))

# '''find the lowest rating of all players in df'''
#
# a = API.get_leaderboard(search='TheViper', json=True)
#
# df = pd.read_json(a)
#
# print(df)

# # df = pd.read_json('https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&steam_id=76561199003184910&count=5')
#
# print(df)

# df = pd.read_csv('AoE2_list_of_top_10000_players.csv')
# for s in df['profile_id'].head():
#     ratings_of_player = API.get_rating_history(profile_id=s)
#     a = []
#     for i in ratings_of_player:
#         a.append(i.get('rating'))
#     print(a)
#     df['max_rating'] = max(a)
#
# print(df.head())
# ratings_of_player = API.get_rating_history(profile_id='199325')
# a = []
# for i in ratings_of_player:
#     a.append(i.get('rating'))
# print(max(a))

#
# profile_iden = df['profile_id']
# a = []
# for i in profile_iden.head():
#     rating_hist = API.get_rating_history(profile_id=str(i))
#     a.append(rating_hist)
#
# print(a)

# for i in df.head():
#     print(i.loc['name'])
    # # print(df['profile_id'])
    # profile_iden = df['profile_id']
    # rating_hist = API.get_rating_history(profile_id=profile_iden)
    # print(rating_hist)

# print(df.tail())

# leaderboard = API.get_leaderboard(leaderboard_id=3, count=10000)
#
# a = leaderboard.get('leaderboard')
# df = pd.DataFrame()
# for i in a:
#     df = df.append(i, ignore_index=True)
#
# df.to_csv('AoE2_list_of_top_10000_players.csv')


# json_object = json.dumps(leaderboard, indent=4)
#
# df = pd.read_json(json_object)

# print(leaderboard)

# rating_hist = API.get_rating_history(profile_id=196240)

# rating = []
# date = []
#
# df = pd.DataFrame()
# df['Rating'] = None
#
# for i in rating_hist:
#     rating.append(i['rating'])
#     date.append(dt.datetime.fromtimestamp(i['timestamp']))
#
# df['Rating'] = rating
# df['Timestamp'] = date
# print(df[df['Rating'] == df['Rating'].min()])
#
# # '''create a chart showing the rating history of the player'''
# # plt.plot(df['Timestamp'], df['Rating'])
# # plt.show()
