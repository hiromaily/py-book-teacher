# coding:utf-8
"""
Get scheduled data of favorite teachers through web scraping
"""
import configs.configs as con
import mails.mails as ml
from multiprocessing import Pool
import teachers.teachers as t
import time


def exec_teacher(ins_teacher):
    """
    job of each teacher by series
    """

    # get html
    count, content = ins_teacher.get_html_body()
    print(content)

    # open browser
    if count != 0 and con.ConfigClass.get_conf("system", "browser") == "1":
        ins_teacher.exec_browser()

    return content


def parallel_teacher(json_teacher):
    """
    job of each teacher by parallel
    """
    ins_teacher = t.TeacherClass(json_teacher)

    # get html
    count, content = ins_teacher.get_html_body()
    print(content)

    # open browser
    if count != 0 and con.ConfigClass.get_conf("system", "browser") == "1":
        ins_teacher.exec_browser()

    return content


def main():
    """
    main
    """

    # time
    start = time.time()

    # config
    con.ConfigClass.init_conf()

    # read json data of teacher information
    t.init_teacher_list(con.ConfigClass.get_conf("json", "path"))

    if con.ConfigClass.get_conf("system", "parallel") == "1":
        print("parallel")

        num_pool = int(con.ConfigClass.get_conf("system", "pool"))
        p = Pool(num_pool)  # max process

        bodys = p.map(parallel_teacher, t.TEACHERS_LIST)
    else:
        print("series")
        bodys = []
        for i, teacher in enumerate(t.TEACHERS_LIST):
            body = exec_teacher(t.TeacherClass(teacher))
            bodys.append(body)

    # mail
    if con.ConfigClass.get_conf("mail", "enable") == "1":
        ml.send_email("\n".join(bodys))

    # time
    print("elapsed time:{0}[sec]".format(time.time() - start))

if __name__ == "__main__":
    main()

