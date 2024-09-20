LOCAL = False
try:
    from js import window,document
    from pyodide.http import open_url # type: ignore
except:
    import urllib.request
    import os

    LOCAL = True
import json

class Cloud_data:
    """
    クラウドにデータをセーブ・ロードする際のクラス

    Parameters
    ----------
    is_test : bool
        デバッグのバージョンかどうか
    """
    def __init__(self,is_test):
        self.is_test = is_test

    def import_(self) -> bool:
        """
        ローカルかクラウドかの判断

        Returns
        ----------
        LOCAL : bool
            ローカル動作ならTrue、クラウド動作ならFalse
        """
        global LOCAL
        return LOCAL

    def save(self,savedata):
        """
        セーブデータのセーブ

        Parameters
        ----------
        savedata : dict
            セーブデータ
        """
        save_name = ""
        if self.is_test:
            save_name = "savedata_test"
        else:
            save_name = "savedata"
        window.localStorage.setItem(save_name,savedata)

    def load(self):
        """
        セーブデータのロード

        Returns
        ----------
        savedata : Any
            セーブデータ
        """
        save_name = ""
        if self.is_test:
            save_name = "savedata_test"
        else:
            save_name = "savedata"
        if window.localStorage.getItem(save_name) == None:
            savedata = {}
            window.localStorage.setItem(save_name,savedata)
        savedata = json.loads(window.localStorage.getItem(save_name).replace("\'","\""))
        return savedata

    def config_save(self,config):
        """
        コンフィグのセーブ

        Parameters
        ----------
        config : dict
            コンフィグ
        """
        config_name = ""
        if self.is_test:
            config_name = "config_test"
        else:
            config_name = "config"
        window.localStorage.setItem(config_name,config)

    def config_load(self):
        """
        コンフィグのロード

        Returns
        ----------
        config : dict
            コンフィグ
        """
        config_name = ""
        if self.is_test:
            config_name = "config_test"
        else:
            config_name = "config"
        if window.localStorage.getItem(config_name) == None:
            config = {
                "basic":{
                        "screen_x":300,"screen_y":200,"name":"一工クエスト","fps":30
                        }
                }
            window.localStorage.setItem(config_name,config)
        config = json.loads(window.localStorage.getItem(config_name).replace("\'","\""))
        return config