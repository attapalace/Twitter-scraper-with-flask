from datetime import date
from flask import Flask ,render_template,request
import os
import snscrape.modules.twitter as sntwitter
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
        
        today = date.today()
        #print('if you want to search for either of multiple terms write as (cats OR dogs), if you want to search for exact phrase write "cats and dogs"')
        #search_term = input('Enter your search term: ')
        #from_date = input('Enter starting date as 2020-06-01 foramt :') or '2021-06-01'
        #until_date = input('Enter end date as 2021-06-01 foramt') or today

        # Creating list to append tweet data to
        tweets_list2 = []

        search_term = request.form.get('search',False)
        from_date = request.form.get('from',False) or '2021-06-11'
        until_date = request.form.get('until',False) or str(today)
        max_results= request.form.get('max',False) or '100'


        if search_term:
                pd.set_option("display.colheader_justify","left")
                # Using TwitterSearchScraper to scrape data and append tweets to list
                for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_term} since:{from_date} until:{until_date}').get_items()):
                    if i > int(max_results):
                        break
                    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

                df = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
                
                return render_template('index.html',  tables=[df.to_html(classes='data')]
                                       , titles=df.columns.values)
        else:
                return render_template('index.html')



if __name__ == '__main__':
        port = int(os.getenv("PORT", 8080))
        app.run(host='0.0.0.0', port=port)
