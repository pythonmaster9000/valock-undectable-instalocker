from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import requests
import base64
import json
import os
import psutil
import asyncio
import concurrent.futures
import gui

disable_warnings(InsecureRequestWarning)
with open(rf'{os.getenv("APPDATA")}\valock\config.json') as file:
    pref = json.load(file)['preferrence']['pref']
preference = [pref]
class ValClient:
    def __init__(self, region: str = 'na', shard: str = 'na'):
        self.region: str = region
        self.shard: str = shard
        self.auth: str = ''
        self.entitlement: str = ''
        self.puuid: str = ''
        self.lockfile: str = rf"{os.getenv('LOCALAPPDATA')}\Riot Games\Riot Client\Config\lockfile"
        if not self.get_basic():
            raise Exception('Unable to get auth game may not be running')
        self.headers = {
            'X-Riot-Entitlements-JWT': self.entitlement,
            'Authorization': f'Bearer {self.auth}'
        }

    def get_basic(self) -> bool:
        try:
            with open(self.lockfile, 'r') as file:
                content = file.readlines()[0].split(':')
                port = content[2]
                password = content[3]
        except FileNotFoundError:
            return False
        url = f"https://127.0.0.1:{port}/entitlements/v1/token"
        userinfo_url = f'https://127.0.0.1:{port}/rso-auth/v1/authorization/userinfo'
        headers = {"Authorization": f"Basic {base64.b64encode(f'riot:{password}'.encode()).decode()}"}
        response = requests.get(url=url, headers=headers, verify=False)
        userinfo_response = requests.get(url=userinfo_url, headers=headers, verify=False)
        try:
            userinfo_response = userinfo_response.json()
            response = response.json()
        except requests.exceptions.JSONDecodeError:
            return False
        self.entitlement = response['token']
        self.auth = response['accessToken']
        self.puuid = json.loads(userinfo_response['userInfo'])['sub']
        return True

    async def wait_not_match(self):
        while True:
            await asyncio.sleep(2)
            current_game = f'https://glz-{self.region}-1.{self.shard}.a.pvp.net/core-game/v1/players/{self.puuid}'
            game_info = requests.get(url=current_game, headers=self.headers).json()
            if game_info.get("httpStatus", None) is not None:
                return True

    async def wait_not_pregame(self):
        while True:
            await asyncio.sleep(2)
            pregame_info = f'https://glz-{self.region}-1.{self.shard}.a.pvp.net/pregame/v1/players/{self.puuid}'
            pregame_response = requests.get(url=pregame_info, headers=self.headers).json()
            if pregame_response.get("httpStatus", None) is not None:
                return True

    async def auto_lock(self, agent: str = 'a3bfb853-43b2-7238-a4f1-ad90e9e46bcc') -> None:
        await self.wait_not_match()
        match_id = None
        pregame_url = f'https://glz-{self.region}-1.{self.shard}.a.pvp.net/pregame/v1/players/{self.puuid}'
        while not match_id:
            response = requests.get(url=pregame_url, headers=self.headers).json()
            if response.get("MatchID", None) is not None:
                match_id = response['MatchID']

        pregame_select = f'https://glz-{self.region}-1.{self.shard}.a.pvp.net/pregame/v1/matches/{match_id}/select/{preference[0]}'
        pregame_lock = f'https://glz-{self.region}-1.{self.shard}.a.pvp.net/pregame/v1/matches/{match_id}/lock/{preference[0]}'
        while True:
            f = requests.post(pregame_select, headers=self.headers)
            p = requests.post(pregame_lock, headers=self.headers)
            await asyncio.sleep(.01)
            if f.status_code != 200 and p.status_code != 200:
                break
        await self.wait_not_pregame()


async def auto_lock():
    #print('locking!!')
    client = ValClient()
    await client.auto_lock()

async def task_runner():
    #task2 = asyncio.create_task(gui.rungui(preference))
    while True:
        #print('prbing for game also preferred agent is', preference)
        lockfile = rf"{os.getenv('LOCALAPPDATA')}\Riot Games\Riot Client\Config\lockfile"
        #if "VALORANT.exe" in (p.name() for p in psutil.process_iter()):
        if os.path.isfile(lockfile):
            if len(asyncio.all_tasks()) == 1:
                task = asyncio.create_task(auto_lock())
        elif len(asyncio.all_tasks()) == 2:
            task.cancel()
        await asyncio.sleep(1)


if __name__ == "__main__":
    print('one', os.getenv("APPDATA"))
    # make thread and start gui bullshit
    # just make the damn autolocker open and search the json file for the thing to choose
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    pool.submit(gui.rungui, preference, os.getenv("APPDATA"))
    asyncio.run(task_runner())
