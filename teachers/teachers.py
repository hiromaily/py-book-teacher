# coding:utf-8
from htmldom import htmldom
import http.client
import json
import subprocess
import sys

"""teachers module"""
TEACHERS_LIST = {}


def init_teacher_list(file):
    global TEACHERS_LIST

    f = open(file, 'r')
    json_obj = json.load(f)
    TEACHERS_LIST = json_obj["teachers"]


class TeacherClass:
    """teacher class"""
    TEACHERS_LIST = {}

    def __init__(self, teacher):
        self.id = teacher["id"]
        self.name = teacher["name"]
        self.country = teacher["country"]

    """
    private
    """
    def __get_html_body(self):
        """
        get html to request http
        """
        conn = http.client.HTTPConnection("eikaiwa.dmm.com", 80)

        # noinspection PyBroadException,PyBroadException,PyBroadException
        try:
            conn.request("GET", "/teacher/index/" + str(self.id) + "/")
        except:
            # NoneType: 'NoneType' object is not iterable
            print("[ERROR] Unexpected error:", sys.exc_info()[0])
            sys.exit()

        res = conn.getresponse()

        # http status code
        if res.status == 200:
            htmldata = res.read().decode("UTF-8")
            conn.close()

            return htmldata
        else:
            conn.close()
            return 0

    def __get_dates_by_parsing_html(self, htmldata):
        """
        format html file
        """
        dom = htmldom.HtmlDom().createDom(htmldata)
        elem = dom.find("a[class=bt-open]")

        return_data = []

        for a in elem:
            # print( a.attr("class"))
            id_json = a.attr("id")

            # decode
            jsondata = self.__decode_html_string(id_json)

            # convert data to json object
            jsondata = json.loads(jsondata)
            # {'field19': '2016-05-03 18:00:00', 'field10': 'teacher_id', 'field8': '23839442',
            # 'field9': 'lesson_id', 'field4': '4565'}

            # extract only date from json
            return_data.append(jsondata['field19'])

        return return_data

    @staticmethod
    def __decode_html_string(str_data):
        """
        replace character of unique html format
        """
        return_data = str_data
        # mapping table
        lst = (
            ('&amp;', '&'),
            ('&lt;', '<'),
            ('&gt;', '>'),
            ('&quot;', '"'),
            ('a:3:', ''),
            ('s:', '"field'),
            (';', ','),
            (':"', '":"'),
            (',}', '}')
        )

        # replace
        for val in lst:
            return_data = return_data.replace(val[0], val[1])

        return return_data

    @staticmethod
    def __show_date(dates):
        body = ""
        for dt in dates:
            body += dt + "\n"

        return body

    """
    public
    """
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_country(self):
        return self.country

    def exec_browser(self):
        """
        execute Chrome browser
        """
        # open /Applications/Google\ Chrome.app http://eikaiwa.dmm.com/teacher/index/4823/
        cmd = "open /Applications/Google\ Chrome.app http://eikaiwa.dmm.com/teacher/index/" + str(self.id) + "/"
        subprocess.call(cmd, shell=True)

        # cmd = "open -a safari http://eikaiwa.dmm.com/teacher/index/" + str(self.id) + "/"
        # subprocess.call(cmd, shell=True)

    def get_html_body(self):
        """
        get html
        """
        # htmldata = ht.getHtmlBody(self.id)
        htmldata = self.__get_html_body()

        # extract json info from html and then return date arrays
        if not htmldata:
            print("{0} is empty!".format(self.name))
            return (0, "")

        # empty valuable is not acceptable and occur error
        dates = self.__get_dates_by_parsing_html(htmldata)

        # check length
        count = len(dates)

        # show available teacher's information
        body = "-----------[{0}]{1} / {2} -----------/\n".format(str(self.id), self.name, self.country)
        body += "http://eikaiwa.dmm.com/teacher/index/" + str(self.id) + "/\n"

        # show date
        if count != 0:
            body += self.__show_date(dates)

        return (count, body)

