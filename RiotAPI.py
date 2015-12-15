import requests
import RiotConsts as Consts
import ErrorInfo
import time

class RiotAPI(object):
    
    def __init__(self, api_key, region=Consts.REGIONS['europe_west']):
        self.api_key = api_key
        self.region = region
        self.prevQueryTime = 0

    def _request(self, api_url, params={}):
        args = {'api_key' : self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        timediff = time.time() - self.prevQueryTime
        if timediff < 1.2:
        #Wait between requests because of the data cap
        #The value should not be much larger than 600 seconds / 500 requests = 1.2 seconds between requests
        #A small value (0.5) is used to get good short-term results.
        #EDIT: Do not set to 0.5 as it will eventually get you blacklisted
            time.sleep(1.2 - timediff)
        try:
            response = requests.get(
                Consts.URL['base'].format(
                    proxy=self.region,
                    region=self.region,
                    url=api_url
                ),
                params=args
            )
        except:
            return self._request(api_url, params)
        self.prevQueryTime = time.time()
        #print "Queried: " + str(response.url)
        if response.status_code != 200:
            while response.status_code != 200:
                if response.status_code != 429:
                    print('Error code ' + str(response.status_code) + ' - ' + ErrorInfo.ERROR[str(response.status_code)])
                #else:
                    #print("Rate limited. Trying again soon...")
                if response.status_code == 404:
                    return None
                #print("Retrying...")
                #Wait and then try again
                if 'Retry-After' in response.headers:
                    time.sleep(int(response.headers['Retry-After']))
                else:
                    time.sleep(1)
                try:
                    response = requests.get(
                        Consts.URL['base'].format(
                            proxy=self.region,
                            region=self.region,
                            url=api_url
                        ),
                        params=args
                    )
                except:
                    return self._request(api_url, params)
                self.prevQueryTime = time.time()
                #print(api_url)
            #print("Succes :)" )
                   
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_matchlist_by_summonerid(self, summonerid, params={}):
        api_url = Consts.URL['matchlist_by_summonerid'].format(
            version=Consts.API_VERSIONS['matchlist'],
            summonerid=summonerid
        )
        return self._request(api_url, params)

    def get_match_by_id(self, matchid, params={}):
        api_url = Consts.URL['match_by_id'].format(
            version=Consts.API_VERSIONS['match'],
            matchid=matchid
        )
        return self._request(api_url, params)

    def get_all_champions(self):
        #This doesnt use the _request method, because it doesn't use the same base.
        requeststring = Consts.URL['staticbase'].format(
            proxy='global',
            region=self.region,
            url=Consts.URL['champions'].format(
                version=Consts.API_VERSIONS['champion']
                )
            )
        response = requests.get(
            requeststring,
            params={'api_key' : self.api_key , 'version' : '5.23.1'}
            )
        return response.json()

    def get_champion_portrait(self, champName):
        #This doesnt use the _request method, because it doesn't use the same base.
        return requests.get(
            'http://ddragon.leagueoflegends.com/cdn/5.23.1/img/champion/{name}.png'.format(
                name=champName
            )
            ).content

