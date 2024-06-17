#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/08/13
# @Author  : zxp

import json, time, os, pytest
import shutil
import threading


class Output(object):
    """
    调用run_case()类方法进行用例的执行已经报告的输出
    """

    @classmethod
    def file_path(cls, root_path):
        cls.file_json = os.path.join(root_path,
                                     "report",
                                     "allure-reports",
                                     "data",
                                     "categories.json"
                                     )
        return cls.file_json

    @classmethod
    def summary_file(cls, root_path):
        cls.summary_file = os.path.join(root_path,
                                        "report",
                                        "allure-reports",
                                        "widgets",
                                        "summary.json"
                                        )
        cls.create_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        return cls.summary_file

    @classmethod
    def result_txt(cls, root_path):
        """
        判断成功or失败
        :return:
        """
        exists = os.path.exists((os.path.join(root_path,
                                              "report",
                                              "allure-reports"
                                              )))
        if exists is True:
            with open(root_path + "/report/allure-reports/widgets/summary.json") as summary:
                summary_obj = json.load(summary)
                passed = summary_obj.get("statistic").get("passed")
                failed = summary_obj.get("statistic").get("failed")
                total = summary_obj.get("statistic").get("total")
                if total == 0:  # fix:没有用例执行成功 导致 ZerDivisionError: division by zero
                    logger_data = "执行异常,总用例数:%s" % total
                else:
                    logger_data = "成功:%s(%.2f%%);失败:%s(%.2f%%)" % (
                        passed, (passed / total) * 100, failed, (failed / total) * 100)
                filename = root_path + '/test_result.txt'
            with open(filename, 'w') as file_object:
                file_object.write(logger_data)
        else:
            raise ValueError('allure静态文件不存在')

    @classmethod
    def run_allure_report(cls, report_path, allure_path):
        os.system('allure generate ' + report_path + ' -o ' + allure_path + '/ --clean')

    @classmethod
    def run_case(cls, root_path, *args, cpu='auto', case_path=None, limited_time=300, report_path=None, **kwargs):
        """
         --dist=loadscope
        将按照同一个模块module下的函数和同一个测试类class下的方法来分组，然后将每个测试组发给可以执行的worker，确保同一个组的测试用例在同一个进程中执行
        目前无法自定义分组，按类class分组优先于按模块module分组
         --dist=loadfile
        按照同一个文件名来分组，然后将每个测试组发给可以执行的worker，确保同一个组的测试用例在同一个进程中执行
        :param case_path: 指定用例路径参数；
        例：Output.run_case(rootPath, cpu="4", case_path='/compatible_version/test_alter_523mail.py')
         或 Output.run_case(rootPath, cpu="4", case_path='/compatible_version）
        :param root_path:
        :param limited_time: 默认300秒超时
        :param report_path: 测试报告生成地址，示例："F:\\report"
        :param cpu: 核数
        :param kwargs:
            has_special 传入时用例跟进文件夹进行拆分执行,例如(has_special=True),special_file_path 单独报告文件夹不传则默认
            single_tag_name 仅串行执行用例的标识，如：single
        :return:
        """
        if report_path is None:
            report_path = root_path + '/report'
        allure_path = report_path + '/allure-reports'
        report_path = report_path + '/report'
        try:
            shutil.rmtree(root_path + '/report/report')
        except Exception:
            pass
        file_path = '/test_cases'
        if case_path is not None:
            file_path += case_path

        # 判断是否存在串行用例pytest.mark标识
        if kwargs.get("single_tag_name"):
            # 先并发执行没标识的用例
            pytest.main(
                ['-v', '-n', cpu, *args, '--dist=loadfile', '-m not ' + kwargs.get("single_tag_name"), '-s',
                 root_path + file_path, '--alluredir', report_path, '--clean-alluredir'])
            # 再串行执行有标识的用例
            pytest.main(
                ['-v', '-n', "1", *args, '-m ' + kwargs.get("single_tag_name"), '-s', root_path + file_path,
                 '--alluredir', report_path])
        else:
            # 并发执行全用例
            pytest.main(
                ['-v', '-n', cpu, *args, '--dist=loadfile', '-s', root_path + file_path, '--alluredir',
                 report_path, '--clean-alluredir'])

        # 判断是否有需要串行执行的测试用例文件夹
        if kwargs.get("has_special"):
            if kwargs.get("special_file_path"):
                special_file_path = kwargs.get("special_file_path")
            else:
                special_file_path = '/test_cases_special'
            pytest.main(
                ['-v', '-n', "1", *args, '-s', root_path + special_file_path, '--alluredir',
                 report_path])

        # 启动子线程用于生成报告
        now = time.time()
        thread = threading.Thread(target=cls.run_allure_report,
                                  args=(report_path, allure_path))
        # 线程守护
        thread.setDaemon(True)
        if os.path.exists(report_path):
            thread.start()
        else:
            print('报告不存在')
            return
        # 防止生成报告卡死,导致的阻塞
        thread.join(limited_time)
        if time.time() - now > limited_time:
            print('等待生成报告超时')
        else:
            # 生成ci判断结果
            cls.result_txt(root_path)
