# follow_me
_Send a direct message to your Mastodon followers to inform them of a move._

If you just moved from one instance to another, you might want to inform your followers to follow you there. 
Since just posting a public post informing of the change might not be seen by everyone, sending a direct private message to your followers will have a bigger impact.

The script here connects to both instances to compare the list of followers and only send a direct message to the ones that are not following your now account already.

### Installation

 - Have mongodb running on your local machine
 - Create a virtual python env.
 - Install packages with `pip install -r requirements.txt`
 
### Configuration

**DO CHANGE both configuration and MESSAGE before running the script**

3 things to change in the `follow_me.py` file (OLD, NEW and MESSAGE):

```
OLD = 'mastodon.social' # Insert here the domain name of your old instance
NEW = 'merveilles.town' # Insert here the domain name of your new instance

APP = 'follow_me'

# Change the content of the message below with whatever you want to tell your followers

MESSAGE = '''
I just wanted to let you know that I left Mastodon.social for Merveilles.town.
My new account is now at @xuv@merveilles.town.
Since you are following me here, I thought you might want to continue following me there.
See you soon.
'''
```


### Run

`python follow_me.py`

You will be prompted to enter your login and password for both instances. Those pieces of information are not stored. 
Tokens on the other hand will be written to `.secret` files in the same folder so that the script could be re run later without asking for login and password again.
Delete those files if you want to prevent further access to your accounts afterwards.

### Credits

[@xuv@merveilles.town](https://merveilles.town/@xuv)
