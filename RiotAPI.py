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

        #Wait between requests because of the data cap
        if timediff < 0.8:
            time.sleep(0.8 - timediff)
        response = requests.get(
            Consts.URL['base'].format(
                proxy=self.region,
                region=self.region,
                url=api_url
            ),
            params=args
        )
        self.prevQueryTime = time.time()
        #print "Queried: " + str(response.url)
        if response.status_code != 200:
            print('Error code ' + str(response.status_code) + ' - ' + ErrorInfo.ERROR[str(response.status_code)])
            print("Retrying...")
            while response.status_code != 200:
                #Wait one second and then try again
                time.sleep(1)
                response = requests.get(
                    Consts.URL['base'].format(
                        proxy=self.region,
                        region=self.region,
                        url=api_url
                    ),
                    params=args
                )
            print("Succes :)" )
                   
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_matchlist_by_summonerid(self, summonerid):
        api_url = Consts.URL['matchlist_by_summonerid'].format(
            version=Consts.API_VERSIONS['matchlist'],
            summonerid=summonerid
        )
        return self._request(api_url)

    def get_match_by_id(self, matchid):
        api_url = Consts.URL['match_by_id'].format(
            version=Consts.API_VERSIONS['match'],
            matchid=matchid
        )
        return self._request(api_url)
