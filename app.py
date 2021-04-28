from flask import Flask, render_template, request, redirect, url_for
import tweepy
import KeysAndTokens
import requests
import sys

app = Flask(__name__)

# twitter authentication
# https://twitter.com/tester3216
auth = tweepy.OAuthHandler(KeysAndTokens.API_KEY, KeysAndTokens.API_KEY_SECRET)
auth.set_access_token(KeysAndTokens.ACCESS_TOKEN, KeysAndTokens.ACCESS_TOKEN_SECRET)
twitterApi = tweepy.API(auth)
def twitterPost(caption):
    try:
        twitterApi.update_status(caption)
        return None
    except tweepy.TweepError as e:
        print(e.reason)
        return "Unable to post Twitter Status"
		
def facebookPost(caption):
    try:
        post_url = 'https://graph.facebook.com/{0}/feed'.format(KeysAndTokens.FACEBOOK_PAGE_ID)
        print(post_url)
        payload = {
            'message': caption,
            'access_token': KeysAndTokens.FACEBOOK_PAGE_ACCESS_TOKEN
        }
        r = requests.post(post_url, data=payload)
        print(r.status_code)
        print(r.text)
        if (r):
            return None
        else:
            return "Unable to post Facebook Status"
        return None
    except OSError as err:
        print("OS error: {0}".format(err))
        return "Unable to post Facebook Status"
    except ValueError as err:
        print("Value Error: {0}".format(err))
        return "Unable to post Facebook Status"
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "Unable to post Facebook Status"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/analytics.html')
def analytics():
    return render_template("analytics.html")

@app.route('/news-media.html', methods=['GET', 'POST'])
def nm():
    errorTwitter = None
    errorFacebook = None
    if request.method == "POST":
        if len(request.form['caption']) > 0 and len (request.form) > 1:
            caption = request.form['caption']
            if request.form.get('Twitter', "") == 'on' and request.form.get('Facebook', "") == 'on':
                print("both")
                errorTwitter = twitterPost(caption)
                errorFacebook = facebookPost(caption)
            elif request.form.get('Twitter', "") == 'on':
                errorTwitter = twitterPost(caption)
            elif request.form.get('Facebook', "") == 'on':
                print("fb")
                errorFacebook = facebookPost(caption)
            else:
                print("invalid")
                redirect(url_for('nm'))
            
            print(request.form)  

    return render_template("news-media.html", errorTwitter=errorTwitter, errorFacebook=errorFacebook)

if __name__ == '__main__':
    app.run('localhost', 5000)
