import requests

from base64 import b64encode

class SynopsiTvApi:

    name = u'SynopsiTV'
    url_attr = 'url_synopsitv'

    oauth_key = "b8bf2410c1bd1e3b791d9ac0735953b9"
    oauth_secret = "6dac4978ec7e55fb5cc9af5291a8c833855f10cb23120e07b694d392ae30797d"

    properties = [
        'id', 'cover_full', 'url', 'name', 'year', 'trailer',
        'directors', 'runtime',
    ]

    def __init__(self, username, password):
        self.__token = None
        self.username = username
        self.password = password

    @property
    def _token(self):
        """Lazy token getter."""
        if not self.__token:
            url = "https://api.synopsi.tv/oauth2/token/"
            data = {
                'grant_type': 'password',
                'client_id': self.oauth_key,
                'client_secret': self.oauth_secret,
                'username': self.username,
                'password': self.password
            }

            headers = {
                'AUTHORIZATION': 'BASIC %s' % b64encode("%s:%s" % (self.oauth_key, self.oauth_secret))
            }

            resp = requests.post(url, data=data, headers=headers)

            self.__token = resp.json()['access_token']

        return self.__token

    def identify(self, title, type, *args, **kwargs):

        """
        2 Broke Girls S03E13

        """

        data = {
            'title_property[]': "id,name,type,year,watched,listed",
            'file_name': title,
            'type': type,
            'bearer_token': self._token
        }

        url = "https://api.synopsi.tv/1.0/title/identify/"
        r = requests.get(url, params=data)

        return r.json()


    def identify_title(self, title):
        """
        https://developers.synopsi.tv/documentation/version/1.0/group/identification/#nav_1
        """
        data = {
            'title_property[]': "id,name",
            'label': title,
            'type': 'episode',
            'bearer_token': self._token
        }

        url = "https://api.synopsi.tv/1.0/title/identify/"
        r = requests.get(url, params=data)

        return r.json()

    def get_episodes(self, title_id):
        """

        https://developers.synopsi.tv/documentation/version/1.1/group/titles/#nav_2

        """

        data = {
            'title_property[]': 'id,name,seasons',
            'episode_property[]': 'name,id,season_number,episode_number',
            'season_property[]': 'id,episodes',
            'bearer_token': self.token
        }

        url = "https://api.synopsi.tv/1.1/tvshow/%s/" % title_id

        r = requests.get(url, params=data)

        return r.json()

    def episode(self, title_id):

        url = "https://api.synopsi.tv/1.0/episode/%s/" % title_id

        title_property = 'id,name,season_number,episode_number,tvshow_id,tvshow_name,tvshow_url,tvshow_year'

        data = {
            'bearer_token': self.__token,
            'title_property[]': title_property,
        }

        r = requests.get(url, params=data)

        return r.json()

    """
    def episode(self, title_id, season_number, episode_number):

        episodes = self.get_episodes(title_id)

        for season in episodes['seasons']:
            for episode in season['episodes']:
                if episode['season_number'] == season_number and episode['episode_number'] == episode_number:
                    return episode

        return None
    """

    def check_in(self, title_id, rating='neutral', past=False, public=False):
        """
        """

        url = "https://api.synopsi.tv/1.1/title/%s/watched/" % title_id

        data = {
            'fb': False,
            'tw': False,
            'bearer_token': self._token
        }

        if rating in ('like', 'neutral', 'dislike'):
            data['rating'] = rating

        if past is True:
            data['past'] = 'true'
        else:
            data['past'] = 'false'

        if public is True:
            data['public'] = 'true'
        else:
            data['public'] = 'false'

        r = requests.post(url, params=data)

        return r.json()

    def undo_check_in(self, title_id):
        """
        https://developers.synopsi.tv/documentation/group/actions/#nav_2
        """

        d = {
            'bearer_token': self.token
        }

        url = "https://api.synopsi.tv/1.1/title/%s/revert_watched/" % title_id

        r = requests.post(url, params=d)

        return r.json()