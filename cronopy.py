#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import session
from requests.exceptions import RequestException
import re
import json

# https://github.com/jrmycanady/gocronometer/blob/master/gocronometer.go
# https://labs.f-secure.com/blog/gwtmap-reverse-engineering-google-web-toolkit-applications/
# https://blog.gdssecurity.com/labs/2009/10/8/gwt-rpc-in-a-nutshell.html


class CronoPy:
    def __init__(self):
        self.s = session()
        self.s.headers["User-Agent"] = "Mozilla/5.0"

        self.APIContentType = "application/x-www-form-urlencoded; charset=UTF-8"

        # self.AppName = "com.cronometer.client.CronometerService"
        self.AppName = "com.cronometer.shared.rpc.CronometerService"
        self.GWTContentType = "text/x-gwt-rpc; charset=UTF-8"
        self.GWTModuleBase = "https://cronometer.com/cronometer/"
        self.GWTPermutation = "7B121DC5483BF272B1BC1916DA9FA963"
        # self.GWTHeader = "3B6C5196158464C5643BA376AF05E7F1"
        self.GWTHeader = "2D6A926E3729946302DC68073CB0D550"

        self.HTMLLoginURL = "https://cronometer.com/login/"
        self.APILoginURL = "https://cronometer.com/login"
        self.GWTBaseURL = "https://cronometer.com/cronometer/app"
        self.APIExportURL = "https://cronometer.com/export"
        self.APIImportURL = "https://cronometer.com/import"

        self.GWTUserIDRegex = "OK\[(\d*),.*"
        self.GWTAuthTokenRegex = '\["(.*)"\]'

        self.GWTAuthToken = ""
        self.crsf_token = ""
        self.nonce = ""
        self.userid = ""

    def GWTGenerateAuthToken(self):
        result = f"7|0|8|https://cronometer.com/cronometer/|{self.GWTHeader}|{self.AppName}|generateAuthorizationToken|java.lang.String/2004016611|I|com.cronometer.client.data.AuthScope/3337242207|{self.nonce}|1|2|3|4|4|5|6|6|7|8|{self.userid}|3600|7|2|"
        return result

    def GWTAuthenticate(self):
        result = f"7|0|5|https://cronometer.com/cronometer/|{self.GWTHeader}|{self.AppName}|authenticate|java.lang.Integer/3438268394|1|2|3|4|1|5|5|-300|"
        return result

    def GWTLogout(self):
        result = f"7|0|6|https://cronometer.com/cronometer/|{self.GWTHeader}|{self.AppName}|logout|java.lang.String/2004016611|{self.nonce}|1|2|3|4|1|5|6|"
        return result

    def doIneedThis(self, token, content):  # Dont think I do
        result = f"7|0|7|https://cronometer.com/cronometer/|{self.GWTHeader}|{self.AppName}|getFoodFromJSON|java.lang.String/2004016611|{token}|{content}|1|2|3|4|2|5|5|6|7|"
        return result

    def MakeImportPayload(self, data):
        # Working: name, nutrients, single barcode, notes aka comments, source
        # Missing: names={}, category=0, tags=[], barcodes=[], measures=[], defaultmeasure=52542633,
        # Ignored: label="EU"
        # Not needed: owner=0, id=8675309,
        label = 2 # American:0 American2016:1 European:2 Austalia/NZ:3 Canadian:4
        def_start = (
            f"7|0|26|https://cronometer.com/cronometer/|{self.GWTHeader}|{self.AppName}|addFood|"
            f"java.lang.String/2004016611|com.cronometer.shared.foods.models.Food/3392319142|"
            f"com.cronometer.shared.foods.models.IngredientSubstitutions/1892525086|{self.nonce}|"
            f"java.util.ArrayList/4159755760|{data['barcodes'][0]}|{data['comments']}|"
            f"com.cronometer.shared.foods.NutritionLabelType/1598919019|"
            f"com.cronometer.shared.foods.models.Measure/1232538395|Serving|"
            f"com.cronometer.shared.foods.models.Measure$Type/2365167904|"
            f"java.util.HashMap/1797211028|java.lang.Integer/3438268394|"
            f"java.lang.Double/858496421|{data['source']}|"
            f"java.util.HashSet/3273092938|com.cronometer.shared.foods.models.Translation/4034452093|"
            f"com.cronometer.shared.user.models.Language/1257207975|en|English|https://cdn1.cronometer.com/media/flags/us.png|"
            f"{data['name']}|1|2|3|4|3|5|6|7|8|6|0|9|1|5|10|0|11|0|0|0|12|"
            f"{label}|A|9|1|13|1|0|0|14|15|2|100|16|"
        )
        num_nutri = str(len(data["nutrients"])) #12
        if len(data["nutrients"]) > 0:
            nutri_string = "".join(
                f'|17|{item["id"]}|18|{item["amount"]}' for item in data["nutrients"]
            )
        def_end = (
            f"|16|0|0|0|19|20|0|9|1|21|22|23|24|25|24|26|0|{self.userid}|0|"
        )
        result = f"{def_start}{num_nutri}{nutri_string}{def_end}"
        return result

    def setContextHeaders(self):
        self.s.headers["content-type"] = self.GWTContentType
        self.s.headers["x-gwt-module-base"] = self.GWTModuleBase
        self.s.headers["x-gwt-permutation"] = self.GWTPermutation

    def MakeRequest(self, method, url, data=False):
        try:
            if method == "get":
                r = self.s.get(url, data=data if data else "")
            if method == "post":
                r = self.s.post(url, data=data if data else "")
        except RequestException as e:
            return e, True
        else:
            if "sesnonce" in r.cookies:
                self.nonce = r.cookies["sesnonce"]
            if r.status_code == 200:
                return r, False
            else:
                return f"HTTP Error: {r.status_code}", True

    def MakeAPIRequest(self, method, url, data=False):
        self.s.headers["Content-Type"] = self.APIContentType
        r, err = self.MakeRequest(method, url, data=data)
        if err:
            return r, True
        else:
            if method == "post":
                response = json.loads(r.content)
                if "error" in response:
                    return response["error"], True
                elif "success" in response:
                    return r, False
            return r, False

    def MakeGWTRequest(self, method, url, data=False):
        self.setContextHeaders()
        r, err = self.MakeRequest(method, url, data=data)
        if err:
            return r, False
        else:
            if "//OK" in r.text:
                return r, False
            elif "//EX" in r.text:
                return f"Error in request data: {r.text}", True

    def Login(self, username, password):
        # Getting crsf-token
        r, error = self.MakeAPIRequest("get", self.HTMLLoginURL)
        if error:
            return r, True
        else:
            self.crsf_token = (
                BeautifulSoup(r.text, "html.parser")
                .find("input", {"name": "anticsrf"})
                .get("value")
            )
        # Logging in
        login_payload = {
            "anticsrf": self.crsf_token,
            "password": password,
            "username": username,
        }
        r, error = self.MakeAPIRequest("post", self.APILoginURL, data=login_payload)
        if error:
            return r, True
        # GWT Login
        r, error = self.MakeGWTRequest(
            "post", self.GWTBaseURL, data=self.GWTAuthenticate()
        )
        if error:
            return r, True
        # Generating GWT Auth token
        self.userid = re.findall(self.GWTUserIDRegex, r.text)[0]
        """ r, error = self.MakeGWTRequest(
            "post", self.GWTBaseURL, data=self.GWTGenerateAuthToken()
        )
        if error:
            return r, True
        self.GWTAuthToken = re.findall(self.GWTAuthTokenRegex, r.text)[0] """
        return "Logged in.", False

    def importCustomFood(self, data):
        # Importing!
        r, error = self.MakeGWTRequest(
            "post", self.GWTBaseURL, data=self.MakeImportPayload(data)
        )
        if error:
            return r, True
        return f"Sucessfully imported \"{data['name']}\"", False

    def Logout(self):
        # Logging out
        r, error = self.MakeGWTRequest("post", self.GWTBaseURL, data=self.GWTLogout())
        if error:
            return error, True
        else:
            self.GWTAuthToken = ""
            self.crsf_token = ""
            self.nonce = ""
            self.userid = ""
            return "Logged out.", False
