# 创建：ZhengYL
# 创建日期：2024/05/02 14:28
# 描述：Excel 操作

import pandas as pd
import os
import re

class ExcelOpera:
    def __init__(self, Road="", SheetName=0):
        self.Road = Road
        self.SheetName = SheetName
        self.df = self.Open()

    # 打开并读取excel文件，返回df对象
    def Open(self, road=""):
        if road == "":
            df = pd.read_excel(r"{}".format(self.Road), header=None, sheet_name=self.SheetName)
            return df
        else:
            df = pd.read_excel(r"{}".format(road), header=None, sheet_name=self.SheetName)
            return df

    # 静态方法：创建表格
    @staticmethod
    def Create(Road):
        df = pd.DataFrame()
        df.to_excel(Road, index=False)
        print("已创建 {} ".format(Road))

    # 静态方法：清空表格
    @staticmethod
    def Clean(Road):
        pd.read_excel(Road)
        df = pd.DataFrame()
        df.to_excel(Road, index=False)
        print("已清空 {} ".format(Road))

    # 静态方法：保存表格
    @staticmethod
    def Save(df, Road):
        df.to_excel(Road, index=False)
        print("已保存 {} ".format(Road))

    # 将传递的参数转换为excel表格中对应的行列数字，以便于对单元格进行操作。
    # `index`参数需要传递一个字符串，如果不是字符串将会返回None
    # 返回值`index_x`，`index_y`为转换后的行，列值。
    def CellExchange(self, index):
        if not isinstance(index, str):
            return None, None
        match = re.match(r'([A-Za-z]+)(\d+)', index)
        if not match:
            return None, None
        index_x = ord(match.group(1).upper()) - ord('A') + 1
        index_y = int(match.group(2))
        return index_x, index_y

    # 获取单个指定单元格下方所有数据，需传递参数
    # `Road`为excel文件路径；
    # `*index_list`为所选单元格在excel中的位置（不区分大小写），可传入多个元素；
    # `SheetName`默认选择第一张表，也可以自定义；
    # `GuardElement`为守护元素，默认关闭，启用后可以选定一个列数据个数为基准来遍历剩下的元素，不足的将会补0。
    # 返回参数`Cols`为存放获取结果的字典
    def GetExcelColDatasByCell(self, *index_list, GuardElement=""):
        Cols = {}
        # 处理不启用守护元素的情况
        if not GuardElement:
            Cols = {index: self.__extract_col_data(index) for index in index_list}
        else:
            # 以第一个元素的长度为基准遍历其他元素
            reference_length = len(self.__extract_col_data(GuardElement))
            for index in index_list:
                col_data = self.__extract_col_data(index)
                if len(col_data) == reference_length:
                    Cols[index] = col_data
                elif len(col_data) > reference_length:
                    Cols[index] = col_data[:reference_length]
                else:
                    Cols[index] = col_data
                    Cols[index] = Cols[index] + [0 for n in range(reference_length - len(col_data))]
        return Cols

    # 获取单个指定单元格有方所有数据，需传递参数
    # `Road`为excel文件路径；
    # `*index_list`为所选单元格在excel中的位置（不区分大小写），可传入多个元素；
    # `SheetName`默认选择第一张表，也可以自定义；
    # `GuardElement`为守护元素，默认关闭，启用后可以选定一个列数据个数为基准来遍历剩下的元素，不足的将会补0。
    # 返回参数`Rows`为存放获取结果的字典
    def GetExcelRowDatasByCell(self, *index_list, GuardElement=""):
        Rows = {}
        # 处理不启用守护元素的情况
        if not GuardElement:
            # 遍历所有索引并提取数据
            for index in index_list:
                Rows[index] = self.__extract_row_data(index)
        else:
            # 以第一个元素的长度为基准遍历其他元素
            reference_length = len(self.__extract_row_data(GuardElement))
            for index in index_list:
                row_data = self.__extract_row_data(index)
                if len(row_data) == reference_length:
                    Rows[index] = row_data
                elif len(row_data) > reference_length:
                    Rows[index] = row_data[:reference_length]
                else:
                    Rows[index] = row_data
                    Rows[index] = Rows[index] + [0 for n in range(reference_length - len(row_data))]
        return Rows

    # 数据筛选并合并处理，需传入参数；
    # `filter_columns` 存放需要筛选的列名；
    # `sum_columns`存放需要计算总和的列名；
    # `SumCount`用于控制函数是否进行求和计算。
    def Grouped(self, Filter_Columns=None, Sum_Columns=None, SumCount=True):
        if Filter_Columns is None:
            Filter_Columns = []
        if Sum_Columns is None:
            Sum_Columns = []
        Df = pd.read_excel(self.Road, sheet_name=self.SheetName)
        if SumCount:
            grouped_df = Df.groupby(Filter_Columns)[Sum_Columns].sum().reset_index()
        else:
            grouped_df = pd.DataFrame(Df.groupby(Filter_Columns))
        return grouped_df

    @staticmethod
    def Merged(Df1, Df2, Left, Right, Show, How="left"):
        # 根据共同列合并数据
        merged_df = pd.merge(Df1, Df2[Show], left_on=Left, right_on=Right, how=How)
        return merged_df

    # 私有方法：根据给定的索引提取列数据
    def __extract_col_data(self, col_index):
        index_x, index_y = self.CellExchange(col_index)
        if index_x is None or index_y is None:
            return []
        Col_data = self.df.iloc[index_y:, index_x - 1]
        return Col_data.dropna().tolist()

    # 私有方法：根据给定的索引提取列数据并处理长度
    def __extract_row_data(self, row_index):
        index_x, index_y = self.CellExchange(row_index)
        if index_x is None or index_y is None:
            return []
        Row_data = self.df.iloc[index_y - 1, index_x:].values.flatten().tolist()
        return Row_data

# import pyotp
# key = 'BX6MYEMLW5BSTY2T6PQGNOJGONQFHD5P' # 从红箭头处复制copy过来
# totp = pyotp.TOTP(key)
# print(totp.now())

