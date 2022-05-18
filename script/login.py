import logging
import random
import unittest
from time import sleep

import requests

from api.loginAPI import loginAPI
from utils import assert_utils

class login(unittest.TestCase):
    phone1 = '1303344557711'
    phone2 = '1303344557712'
    phone3 = '1303344557714'
    phone4 = '1303344557717'
    phone5 = '1303344557720'
    phone6 = '1303344557723'
    pwd = 'test123'
    imgCode = '8888'
    smsCode = '666666'
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.session()

    def tearDown(self) -> None:
        pass
    #参数为随机小数获取图片验证码成功
    def test01_get_img_code_random_float(self):
        #定义参数(随机小数)
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImageCode(self.session,str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)
    #参数为随机整数获取图片验证码成功
    def test02_get_img_code_random_int(self):
        #定义参数（随机整数）
        r = random.randint(100000,900000)
        #调用接口类中的接口
        response = self.login_api.getImageCode(self.session,str(r))
        #接收接口返回的结果
        self.assertEqual(200,response.status_code)

    #参数为空时，获取图片验证码失败
    def test03_get_img_code_param_is_null(self):
        #定义参数（参数为空）

        #调用接口类中的接口
        response = self.login_api.getImageCode(self.session,"")
        #接收接口返回的结果
        self.assertEqual(404,response.status_code)
    #参数为随机字母时，获取图片验证码失败
    def test04_get_img_code_random_char(self):
        #定义参数（参数为空）
        r = random.sample("abcdefghijklm",8)
        #字符串拼接
        rand = ''.join(r)
        logging.info(rand)
        #调用接口类中的接口
        response = self.login_api.getImageCode(self.session,rand)
        #接收接口返回的结果
        self.assertEqual(400,response.status_code)

    #获取短信验证码成功
    def test05_get_sms_code_success(self):
        #1、定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        #2、获取图片验证码
        #定义参数（正确的手机号和验证码）
        #调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        #将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        #对收到的响应结果进行断言
        assert_utils(self,response,200,200,"短信发送成功")
    #获取短信验证码失败--图片验证码错误
    def test06_get_sms_code_wrong_img_code(self):
        # 1、定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        #2、获取短信验证码
        #定义参数（手机号正确，图片验证码错误）
        error_code = '1234'
        #调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,error_code)
        #对收到的响应结果进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 获取短信验证码失败--图片验证码为空
    def test07_get_sms_code_wrong_img_code_is_null(self):
        # 1、定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（手机号正确，图片验证码为空）
        # 调用接口类中的发送短信验证码的接口
        response =self.login_api.getSmsCode(self.session,self.phone1,'')
        # 对收到的响应结果进行断言
        assert_utils(self,response,200,100,"图片验证码错误")

    # 获取短信验证码失败--手机号为空
    def test08_get_sms_code_phone_is_null(self):
        # 1、定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（手机号为空，图片验证码正确）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,'',self.imgCode)
        logging.info("get sms code response={}".format(response.json()))

        # 对收到的响应结果进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

    # 获取短信验证码失败--未调用获取图片验证码接口
    def test09_get_sms_code_phone_no_img_verifycode(self):
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")


    #输入必填项，注册成功
    def test10_register_success_param_must(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        #3、成功注册--输入必填项
        #调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session,self.phone1,self.pwd)
        logging.info("get register code response={}".format(response.json()))

        #对结果进行断言
        assert_utils(self,response,200,200,"注册成功")

    #输入全部参数，注册成功
    def test11_register_success_param_all(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、成功注册--输入必填项
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone2, self.pwd,invite_phone='13012345678')
        logging.info("get register code response={}".format(response.json()))

        # 对结果进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    #注册失败，手机号已存在
    def test12_register_phone_is_exist(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、成功注册--输入必填项
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone='13012345678')
        logging.info("get register code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200,100, "手机已存在!")

    #注册失败，密码为空
    def test13_register_password_is_null(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone3, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、成功注册--输入必填项
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone3, '')
        logging.info("get register code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    #图片验证码错误，注册失败
    def test14_register_img_code_is_wrong(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、注册失败--图片验证码错误
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone4, self.pwd,'1234')
        logging.info("get register code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 100, "验证码错误!")


    #短信验证码错误，注册失败
    def test15_register_sms_code_is_wrong(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone5, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、注册失败--图片验证码错误
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone5, self.pwd, self.imgCode,'123456')
        logging.info("get register code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 100, "验证码错误")

    #未同意条款，注册失败
    def test16_register_noagree_protocol(self):
        # 1、成功获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImageCode(self.session, str(r))

        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取图片验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone6, self.imgCode)
        # 将response数据全部打印出来
        logging.info("get sms code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、注册失败--图片验证码错误
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone6, self.pwd, dyServer='off')
        logging.info("get register code response={}".format(response.json()))
        # 对收到的响应结果进行断言
        assert_utils(self, response, 200, 100, "请同意我们的条款")


    #登录成功
    def test17_login_success(self):
        #准备参数
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,self.pwd)
        #对结果进行断言
        assert_utils(self,response,200,200,"登录成功")

    #用户不存在，登录失败
    def test18_login_phone_not_exist(self):
        #准备参数
        wphone = '13000000000'
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,wphone,self.pwd)
        logging.info("get login code response={}".format(response.json()))

        #对结果进行断言
        assert_utils(self,response,200,100,"用户不存在")

    #密码为空，登录失败
    def test19_login_fail_pwd_is_null(self):
        #准备参数
        #调用接口类中的发送登录的接口
        response = self.login_api.login(self.session,self.phone1,'')
        #对结果进行断言
        assert_utils(self,response,200,100,"密码不能为空")

    #登录失败--密码错误
    def test20_login_wrong_pwd(self):
        wrong_pwd = 'error'
        #1、输入错误密码，提示错误一次
        response = self.login_api.login(self.session,self.phone1,wrong_pwd)
        assert_utils(self,response,200,100,"密码错误1次,达到3次将锁定账户")
        #2、输入错误密码，提示错误两次
        response = self.login_api.login(self.session, self.phone1, wrong_pwd)
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        #3、输入错误密码，提示错误三次被锁定
        response = self.login_api.login(self.session, self.phone1, wrong_pwd)
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #4、输入正确密码，提示被锁定
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        #5、等待60s，再输入正确密码，提示登录成功
        sleep(60)
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        assert_utils(self, response, 200, 200, "登录成功")