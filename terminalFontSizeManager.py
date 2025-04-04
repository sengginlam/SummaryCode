from os import getenv, path
from copy import deepcopy
from platform import system as systemType
from typing import Optional
import json


class TerminalFontSizeManager(object):
    def __init__(self):
        if systemType()=="Windows":
            self._SETTINGS_PATH = path.join(getenv("LOCALAPPDATA"), "Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json")
            self._callCount = 1
        else:
            raise SystemError(f"Only runs on Windows system. Current system is {systemType()}.")

    def __call__(self, fontSize:Optional[int]=None):
        if self._callCount:
            if fontSize:
                self.originData = self._setTerminalFontSize(fontSize)
            else:
                self.originData = None
            self._callCount -= 1
        else:
            self.originData and self._resetTerminalFontSize(self.originData)

    def _setTerminalFontSize(self, fontSize:int) -> dict:
        with open(self._SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        originData = deepcopy(data)
        for profile in data["profiles"]["list"]:
            profile["font"] = {"size": fontSize}
        with open(self._SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return originData

    def _resetTerminalFontSize(self, originData:dict) -> None:
        with open(self._SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(originData, f, indent=4)