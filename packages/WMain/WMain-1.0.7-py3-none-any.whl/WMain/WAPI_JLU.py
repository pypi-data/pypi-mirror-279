from WMain.WRequests import WSession
from WMain.WSelenium import WEdgeDownloader
from WMain.WAPI_CloudCode import api_cloudcode
from WMain.WResponse import WResponse
from WMain.WJs import JsFileModel
from WMain.WUrl import WUrl
import re
from Crypto.Cipher import AES
import base64
import json
import time


class WAPI_IEDU_Selenium:
    URL_IEDU = "https://iedu.jlu.edu.cn/"
    URL_IEDU_COMMENT = (
        "https://ievaluate.jlu.edu.cn/index.html?v=3.11.1#/my-task/main/UnFinished"
    )

    XPATH_USERNAME = '//*[@class="login_box_input user-pic pic-input"]'
    XPATH_PASSWORD = '//*[@class="login_box_input password-pic pic-input"]'
    XPATH_LOGIN_BUTTON = '//*[@class="login_box_landing_btn"]'
    XPATH_COMMENT_FIRST_SPAN_1 = '//*[@class="ant-table-tbody"]/tr[1]//span'
    XPATH_COMMENT_FIRST_SPAN_2 = (
        '//*[@class="ant-table-row ant-table-row-level-0"][1]/td[7]/span'
    )
    XPATH_COMMENT_COMMIT_BUTTON = '//*[@class="ant-form ant-form-horizontal"]//button'
    XPATH_COMMENT_SCORE_1 = (
        '//*[@class="ant-form-item-children"]/div/div[1]/label/span[2]/div'
    )

    XPATH_COMMENT_SCORE_2 = (
        '//*[@class="ant-form-item-children"]/div/div[2]/label/span[2]/div'
    )
    XPATH_COMMENT_SCORE_3 = (
        '//*[@class="ant-form-item-children"]/div/div[3]/label/span[2]/div'
    )

    def __init__(
        self, session: WSession, edge_version: str, driver_path: str = "./driver"
    ) -> None:
        dn = WEdgeDownloader(session, driver_path)
        dn(edge_version)
        self.edge = dn.get_driver()

    def start(self):
        self.edge.start()
        self.edge.get(self.URL_IEDU)

    def login(self, username: str, password: str) -> None:
        self.edge.send_keys_by_xpath(self.XPATH_USERNAME, username)
        self.edge.send_keys_by_xpath(self.XPATH_PASSWORD, password)
        self.edge.click_by_xpath(self.XPATH_LOGIN_BUTTON)

    def comment(self):
        while 1:
            self.edge.get(self.URL_IEDU_COMMENT)
            element = self.edge.wait_for_element(self.XPATH_COMMENT_FIRST_SPAN_1, 2)
            if not element:
                break
            try:
                element.click()
                element = self.edge.wait_for_element(self.XPATH_COMMENT_FIRST_SPAN_2, 2)
                element.click()
                self.edge.wait_for_element(self.XPATH_COMMENT_COMMIT_BUTTON, 2)
                elements_1 = self.edge.get_elements_by_xpath(self.XPATH_COMMENT_SCORE_1)
                elements_2 = self.edge.get_elements_by_xpath(self.XPATH_COMMENT_SCORE_2)
                elements_3 = self.edge.get_elements_by_xpath(self.XPATH_COMMENT_SCORE_3)
                for i in range(len(elements_1)):
                    if i % 3 == 0:
                        elements_1[i].click()
                    elif i % 3 == 1:
                        elements_2[i].click()
                    else:
                        elements_3[i].click()
                self.edge.click_by_xpath(self.XPATH_COMMENT_COMMIT_BUTTON)
            except Exception:
                break


class Icourses_Session:
    URL_MAIN = "https://icourses.jlu.edu.cn/xsxk/profile/index.html"
    URL_ADD = "https://icourses.jlu.edu.cn/xsxk/elective/clazz/add"
    URL_LOGIN = "https://icourses.jlu.edu.cn/xsxk/auth/login"
    URL_CAPTCHA = "https://icourses.jlu.edu.cn/xsxk/auth/captcha"
    URL_USER = "https://icourses.jlu.edu.cn/xsxk/elective/user"
    URL_NOW = "https://icourses.jlu.edu.cn/xsxk/web/now"

    RE_AES_KEY = re.compile('loginVue.loginForm.aesKey = "(.*?)";')
    RE_BATCH_ID = re.compile('batch = {"code":"(.*?)"')

    CODE_SUCCESS = 200
    CODE_ERRORS = [500]

    STR_SUCCESS = "登录成功"
    STR_RETURN_RELOGIN = "重新登录"
    STR_RETURN_SUCCESS = "成功"
    STR_RETURN_NOT_START = "未开始"
    STR_RETURN_CAPTCHA_ERROR = "验证码错误"

    session: WSession
    class_type: str
    main_resp: WResponse
    __AES_key: str
    __BatchId: str
    __classes = None
    __has_choosed = None
    __username: str
    __password: str

    def __init__(
        self, session: WSession, username: str, password: str, class_type: str = "TJKC"
    ):
        self.session = session
        self.class_type = class_type
        self.__has_choosed = []
        self.__username = username
        self.__password = password
        self.__flush_main()

    def __flush_main(self):
        self.main_resp = self.session.get(self.URL_MAIN).resp
        self.__AES_key = self.RE_AES_KEY.findall(self.main_resp.text)[0]
        self.__BatchId = self.RE_BATCH_ID.findall(self.main_resp.text)[0]

    def __token_json(self, username, password):
        captcha = ""
        while len(captcha) != 4:
            captcha_json = self.session.post(self.URL_CAPTCHA).json()["data"]
            captcha_img: str = captcha_json["captcha"].split(",")[-1]
            captcha_uuid: str = captcha_json["uuid"]
            captcha: str = api_cloudcode.Post4_by_base64(captcha_img)
        aes = AES.new(self.__AES_key.encode("utf-8"), AES.MODE_ECB)
        aes_str = aes.encrypt(
            password.ljust(16, chr(16 - len(password))).encode("utf-8")
        )
        aes_str = base64.b64encode(aes_str)
        aes_str = aes_str.decode("utf-8")
        login_data = {
            "loginname": username,
            "password": aes_str,
            "captcha": captcha,
            "uuid": captcha_uuid,
        }
        # {'code': 500, 'msg': '学生不在选课轮次中，暂时不能登录', 'data': None | {'token': '???'}}
        return self.session.post(self.URL_LOGIN, data=login_data).json()

    def __token_json_new(self, username, password):
        while 1:
            token_json = self.__token_json(username, password)
            if token_json["code"] in self.CODE_ERRORS:
                return token_json
            elif self.STR_RETURN_CAPTCHA_ERROR in token_json["msg"]:
                continue
            else:
                return token_json

    def login(self) -> str:
        token_json = self.__token_json_new(self.__username, self.__password)
        if token_json["code"] != self.CODE_SUCCESS:
            return token_json["msg"]
        token = token_json["data"]["token"]
        self.session.session.cookies.set(
            name="Authorization", value=token, domain="icourses.jlu.edu.cn"
        )
        self.session.ini.headers["Authorization"] = token
        self.session.ini.headers["BatchId"] = self.__BatchId
        self.session.post(self.URL_USER, data={"batchId": self.__BatchId})
        self.session.post(self.URL_NOW)
        dic = {
            "teachingClassType": self.class_type,
            "pageNumber": 1,
            "pageSize": 100,
            "orderBy": "",
            "campus": "02",
        }
        self.__classes = self.session.post(
            "https://icourses.jlu.edu.cn/xsxk/elective/jlu/clazz/list",
            data=json.dumps(dic),
            headers={"Content-Type": "application/json"},
        ).json()["data"]["rows"]

        return token_json["msg"]

    def __add_class(self, class_id: str, secret_val: str) -> str:
        data = {
            "clazzType": self.class_type,
            "clazzId": class_id,
            "secretVal": secret_val,
        }
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "application/json, text/plain, */*",
        }
        return self.session.post(self.URL_ADD, data=data, headers=headers).json()["msg"]

    def choose(self, class_teacher: str):
        for row in self.__classes:
            for c in row["tcList"]:
                try:
                    _class_teacher = f'{c["KCM"]}_{c["SKJS"]}'
                except KeyError:
                    continue
                if (
                    _class_teacher not in self.__has_choosed
                    and class_teacher == _class_teacher
                ):
                    resp = self.__add_class(c["JXBID"], c["secretVal"])
                    if self.STR_RETURN_RELOGIN in resp:
                        return self.STR_RETURN_RELOGIN
                    elif self.STR_RETURN_SUCCESS in resp:
                        self.__has_choosed.append(class_teacher)
                        return self.STR_RETURN_SUCCESS
                    elif self.STR_RETURN_NOT_START in resp:
                        return self.STR_RETURN_NOT_START

    def get_all_class_teacher(self):
        class_teacher_list = []
        for row in self.__classes:
            for c in row["tcList"]:
                try:
                    _class_teacher = f'{c["KCM"]}_{c["SKJS"]}'
                except KeyError:
                    continue
                class_teacher_list.append(_class_teacher)
        return class_teacher_list


class Iedu_Session:
    URL_IEDU = "https://iedu.jlu.edu.cn/"
    URL_LOGIN_CODE = "https://cas.jlu.edu.cn/tpass/code"
    URL_IEDU_MAIN = "https://iedu.jlu.edu.cn/jwapp/sys/emaphome/portal/index.do"
    URL_API_SERVICE = "https://iedu.jlu.edu.cn/jwapp/sys/emaphome/appTips.do"
    URL_API_SCORE = "https://iedu.jlu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do"
    URL_SCORE = (
        "https://iedu.jlu.edu.cn/jwapp/sys/cjcx/*default/index.do?EMAP_LANG=zh#/cjcx"
    )

    WURL_IEDU_LOGIN = WUrl(
        "https://cas.jlu.edu.cn/tpass/login?service=https://iedu.jlu.edu.cn/jwapp/sys/emaphome/portal/index.do"
    )

    XPATH_STRS_SERVICE_NAME = '//*[@class="menu_item tg-left "]/@title'
    XPATH_STRS_SERVICE_DATA_URL = '//*[@class="menu_item tg-left "]/@data-url'

    STR_LOGIN_SUCCESS = "登录成功"
    STR_LOGIN_ERROR = "登录失败"

    def __init__(
        self, session: WSession, username: str, password: str, des_js: str
    ) -> None:
        self.session = session
        self.session.ini.headers["Referer"] = str(self.WURL_IEDU_LOGIN)
        self.username = username
        self.password = password
        self.des_js = JsFileModel(des_js)
        self.flush_iedu()

    def flush_iedu(self):
        resp = self.session.get(self.URL_IEDU)
        self.salt = re.findall('id="lt" name="lt" value="(.*?)"', resp.text)[0]
        self.rsa = self.des_js.call(
            "strEnc", self.username + self.password + self.salt, "1", "2", "3"
        )
        self.excution = re.findall('name="execution" value="(.*?)"', resp.text)[0]

    def login(self):
        captcha_img = self.session.get(self.URL_LOGIN_CODE).content
        captcha = api_cloudcode.Post4_by_bytes(captcha_img)
        data = {
            "code": captcha,
            "rsa": self.rsa,
            "ul": str(len(self.username)),
            "pl": str(len(self.password)),
            "sl": "0",
            "lt": self.salt,
            "execution": self.excution,
            "_eventId": "submit",
        }
        self.resp_main = self.session.post(self.WURL_IEDU_LOGIN, data=data)
        self._get_services_dict()
        if self.URL_IEDU_MAIN == self.resp_main.url:
            return self.STR_LOGIN_SUCCESS
        else:
            return self.STR_LOGIN_ERROR

    def get_scores(self):
        self._post_service("成绩查询")
        self.session.ini.headers["Referer"] = self.URL_SCORE
        data = {
            "querySetting": '[{"name":"SFYX","caption":"是否有效","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"1","value_display":"是"},{"name":"SHOWMAXCJ","caption":"显示最高成绩","linkOpt":"AND","builderList":"cbl_m_List","builder":"m_value_equal","value":"0","value_display":"否"}]',
            "*order": "-XNXQDM,-KCH,-KXH",
            "pageSize": "20",
            "pageNumber": "1",
        }
        r = self.session.post(self.URL_API_SCORE, data=data)
        print(r.text)

    def _get_services_dict(self):
        titles = self.resp_main.xpath(self.XPATH_STRS_SERVICE_NAME)
        urls = self.resp_main.xpath(self.XPATH_STRS_SERVICE_DATA_URL)
        ids = [i.split("=")[-1] for i in urls]
        self.service_dict = dict(zip(titles, ids))
        return self.service_dict

    def _post_service(self, service_name):
        data = {"appwid": self.service_dict[service_name]}
        print(self.session.post(self.URL_API_SERVICE, data=data).resp.headers)


if __name__ == "__main__":
    s = WSession()
    s.ini.set_proxy(20000)
    iedu = Iedu_Session(s, "weiyn2021", "13214310112asdw", "des.js")
    print(iedu.login())
    print(iedu.get_scores())
    # choose = Icourses_Session(s, "20210112", "124113")
    # r = choose.login()
    # print(r)
    # print(choose.get_all_class_teacher())
    # choose_classes = ["运筹学导论_宗芳"]
    # while 1:
    #     for i in choose_classes:
    #         r = choose.choose(i)
    #         if r == choose.STR_RETURN_RELOGIN:
    #             choose.login()
    #             break
    #         print(r)
    #         time.sleep(1)
