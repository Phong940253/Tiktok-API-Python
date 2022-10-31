from TiktokApi import *
from tqdm import tqdm
import pandas as pd
Api = Tiktok()


Api.openBrowser()

limit = 1000000
count = 0
first = True
flag = 0

hashtags = []
with tqdm(total=limit) as pbar:
    while True:
        data = Api.getTrendingFeed(first=first)
        if first == True:
            for x in data['ItemModule']:
                if 'challenges' in x:
                    for challenge in x['challenges']:
                        if 'title' in challenge:
                            hashtags.append(['#' + challenge['title'], 'tiktok'])
                pbar.update(1)

                
                if count > 0 and (count % 10000 == 0):
                    df = pd.DataFrame(hashtags, columns=['hashtag','platform', 'lang'])
                    df = df.drop_duplicates()
                    df.to_csv(f'tiktok-{count}.csv', index=False, encoding='utf-16', sep='\t')

                count += 1
                if count == limit:
                    flag = 1
                    break
        else:
            if 'itemList' in data:
                for x in data['itemList']:

                    if 'challenges' in x:
                        for challenge in x['challenges']:
                            if 'title' in challenge:
                                hashtags.append(['#' + challenge['title'], 'tiktok', 'vi'])
                    pbar.update(1)

                    if count > 0 and (count % 10000 == 0):
                        df = pd.DataFrame(hashtags, columns=['hashtag','platform', 'lang'])
                        df = df.drop_duplicates()
                        df.to_csv(f'tiktok-{count}.csv', index=False, encoding='utf-16', sep='\t')

                    count += 1
                    if count == limit:
                        flag = 1
                        break
        if flag == 1:
            break
        first = False

       

df = pd.DataFrame(hashtags, columns=['hashtag','platform', 'lang'])
df = df.drop_duplicates()
df.to_csv(f'tiktok-{count}.csv', index=False, encoding='utf-16', sep='\t')

Api.closeBrowser()
