# 创建：LiuZY
# 创建日期：2022/11/30 11:18
# 描述：SQL Server 连接

from openpyxl import Workbook
from Crypto.Cipher import AES
import pandas as pd
import datetime
import logging
import pymssql
import base64
import wmi

class MSSQL:
    def __init__(self, host, database, user, password):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.mode=AES.MODE_CBC
        self.iv=b'vlPz53H442VmEhbb'
        self.encoding='utf-8'

    # 显示加密后的用户名、密码字符串
    @staticmethod
    def showEncryptedString(user,password):
        instance=MSSQL('','','','')
        enc_user=instance.encrypt_password(user)
        enc_psd=instance.encrypt_password(password)
        print(f"Encrypted users: {enc_user}\nEncrypt password: {enc_psd}")

    # 连接数据库
    def get_connect(self):
        if not self.database:
            raise (NameError,'请先设置数据库信息')

        try: # 这是一个 `try` 语句，用于捕获和处理可能发生的异常。
            dec_name=self.decrypt_password(self.user)
            dec_psd=self.decrypt_password(self.password)

            self.conn=pymssql.connect(host=self.host,user=dec_name,password=dec_psd,database=self.database)
            cur=self.conn.cursor()
            if not cur:
                raise (NameError,'连接数据库失败')
            else:
                return cur
        except  pymssql.Error as e:
            print(f"Connection database {self.database} failed,Error Msg: {e}")
        # finally:
        #     if self.conn:
        #         self.conn.close()

    # 执行SQL语句，返回查询结果
    def ExecQuery(self,sql):
        cur=self.get_connect();
        try:
            cur.execute(sql)
            reslist=cur.fetchall()
            return reslist
        except pymssql.Error as e:
            print(e)
        finally:
            self.conn.close()

    # 执行无返回结果的SQL语句
    def ExecNonQuery(self,sql):
        cur = self.get_connect()
        try:
            cur.execute(sql)
            self.conn.commit()
        except pymssql.Error as e:
            self.conn.rollback()
            print(f"Error:{e}")
            self.__write_log(e)
        finally:
            cur.close()
            self.conn.close()

    # 执行存储过程
    def ExecProc(self,proc,param):
        cur=self.get_connect()
        try:
            cur.execute_proc(proc,param)
            return cur.fetchall()
        except pymssql.Error as e:
            print(f"Error:{e}")
        finally:
            cur.close()
            self.conn.close()

    def CheckTableExist(self,table):
        cursor = self.get_connect()
        try:
            # 这行代码构造了一个SQL查询语句，用来查询信息模式中的表名。
            sql_str=f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table}' AND table_type = 'BASE TABLE'"
            cursor.execute(sql_str)
            cursor.fetchall()
            # exists=cursor.fetchone()[0]

            return cursor.rowcount>0
        except pymssql.Error as e:
            print(f"Error:{e}")
        finally:
            cursor.close()
            self.conn.close()


    # 插入数据表表
    def InsertToTable(self,table,fields,values):
        cursor=self.get_connect()

        # 数据为空时退出执行
        if values is None or len(values)<=0:
            print('数据源为空或无数据，插入操作终止')
            return

        field_count=len(fields.split(','))
        par_str=','.join(['%s'] * field_count)

        try:
            sql_insert=f"Insert into {table} ({fields})values ({par_str})"

            for row in values:
                cursor.execute(sql_insert,row)
            self.conn.commit()
            print('insert end')
        except pymssql.Error as e:
            print(f"Error:{e}")
            self.__write_log(e)
        finally:
            cursor.close()
            self.conn.close()

    # 导出到Excel
    def ExportToExcel(self,sql,name):
        cursor=self.get_connect()
        try:
            cursor.execute(sql)
            # 获取查询结果
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(list(rows), columns=columns)

            #这格式，取消导出文件的行号，列头的边框线
            df.T.reset_index().T.to_excel(name,header=None,index=None)
        except pymssql.Error as e:
            print(f"Error:{e}")
        finally:
            cursor.close()
            self.conn.close()

    # 私有方法，获取主板序列号
    def __get_serial(self):
        c=wmi.WMI()
        for sys in c.Win32_BaseBoard():
            return sys.SerialNumber

    # 私有方法，自动生成Key,用户字符串的加、解密
    def __get_key(self):
        enc_key=self.__get_serial()
        return self.__add_to_16(enc_key)

    # 格式化字符串长度为16的倍数
    def __add_to_16(self, text):
        if len(text.encode(self.encoding)) % 16:
            add = 16 - (len(text.encode(self.encoding)) % 16)
        else:
            add=0
        text = text + ('\0' * add)
        return text.encode(self.encoding)

    # 私有方法字符串加、解密对象
    def __get_cryptor(self):
        return  AES.new(self.__get_key(), self.mode, self.iv)

    # 字符串加密
    def encrypt_password(self,password):
        text = self.__add_to_16(password)
        cryptos = self.__get_cryptor()
        cipher_text =cryptos.encrypt(text)
        return base64.b64encode(cipher_text).decode(self.encoding)

    # 字符串解密
    def decrypt_password(self,text):
        cryptos = self.__get_cryptor()
        dec_text = cryptos.decrypt(base64.b64decode(text))
        return bytes.decode(dec_text).rstrip('\0')

    # 写日志信息
    def __write_log(self,content):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # 创建文件处理程序并添加到日志记录器
        log_name=f'{datetime.datetime.now().strftime("%Y%m%d")}_log.log'
        file_handler = logging.FileHandler(log_name)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 测试日志输出
        logger.error(content)
