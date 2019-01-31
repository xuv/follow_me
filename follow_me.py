import getpass
from mastodon import Mastodon
from mastodon.Mastodon import MastodonAPIError
from mastodon.Mastodon import MastodonIllegalArgumentError
from pprint import pprint
from pymongo import MongoClient
from pathlib import Path
import time
import sys

client = MongoClient('localhost', 27017)
masto_db = client.mastodon_db
profiles = masto_db.profiles

OLD = 'mastodon.social'
NEW = 'merveilles.town'

APP = 'follow_me'

MESSAGE = '''
I just wanted to let you know that I left Mastodon.social for Merveilles.town.

My new account is now at @xuv@merveilles.town.

Since you are following me here, I thought you might want to continue following me there.
See you soon.
'''


def getAccess( INSTANCE ):
    base_url = 'https://' + INSTANCE
    client_secret = INSTANCE + '_clientcred.secret'
    if not Path( client_secret ).is_file() :     
        Mastodon.create_app(
             APP,
             api_base_url = base_url,
             to_file = client_secret
        )
    
    user_secret = INSTANCE + '_usercred.secret'
    if not Path( user_secret ).is_file() :
        user_email = input( INSTANCE + ' email: ' )
        user_pass = getpass.getpass( INSTANCE + ' password: ' )
             
        mastodon = Mastodon(
            client_id = client_secret,
            api_base_url = base_url
        )

        try:
            mastodon.log_in(
                user_email,
                user_pass,
                to_file = user_secret
            )
        except MastodonIllegalArgumentError:
            print( 'Login and/or password is incorrect' )
            sys.exit(0)

    return Mastodon(
        access_token = INSTANCE + '_usercred.secret',
        api_base_url = base_url
    )


def getFollowers( mastodon ) :
    me = mastodon.account_verify_credentials()
    followers_page1 = mastodon.account_followers(me, limit=80)
    return mastodon.fetch_remaining(followers_page1)
    
def storeFollowers( followers ) :
    for follower in followers:
        profile_exist = profiles.find_one({'url': follower['url']})
        if profile_exist is None: 
            profiles.insert_one(follower)
    print('All followers stored \n')

def markFollowers( followers ) :
    for follower in followers:
        profile_exist = profiles.find_one({'url': follower['url']})
        if profile_exist is not None: 
            print('@' + profile_exist['acct'] + ' is following you already' )
            profiles.update_one({
                '_id': profile_exist['_id']
            }, {
                '$set': {'isFollowing': True}
            })
    print('All those who already follow were marked \n')

def getNonFollowers():
    query = {'$and': [
        {'isFollowing': {'$ne': True}},
        {'isInvited': {'$ne': True}}
    ]}
    print( 'Inviting %s followers' % profiles.count_documents( query ) )
    non_followers = profiles.find( query )
    return non_followers


def inviteNonFollowers( non_followers, mastodon ): 
    for follower in non_followers:
        try:
            print('Inviting @' + follower['acct'])
            mastodon.status_post('Hello @' + follower['acct'] + message, visibility='direct')
            profiles.update_one({
                '_id': follower['_id']
            }, {
                '$set': {'isInvited': True}
            })
        except MastodonAPIError:
            print('There was an error with %s api' % OLD)
            pass
        time.sleep(1)
    print('Invited everyone')

def main():
  old_masto = getAccess( OLD )
  old_followers = getFollowers( old_masto )
  print('Found %s followers on %s' % ( len( old_followers ), OLD ) )
  storeFollowers( old_followers )
  
  new_masto = getAccess( NEW )
  new_followers = getFollowers( new_masto )
  print('Found %s followers on %s \n' % ( len( new_followers ), NEW ) )
  
  markFollowers( new_followers )
  
  non_followers = getNonFollowers()
  inviteNonFollowers( non_followers, old_masto )
  
if __name__== "__main__":
  main()


