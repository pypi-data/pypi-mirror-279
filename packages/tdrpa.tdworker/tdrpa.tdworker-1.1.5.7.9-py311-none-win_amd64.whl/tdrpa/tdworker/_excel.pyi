from tdrpa import _tdxlwings as xw

class Excel:
    @staticmethod
    def OpenExcel(filePath: str, visible: bool = True, appType: str = 'Excel', pwd: str = '', writePwd: str = '') -> xw.Book:
        '''
        打开Excel工作簿

        excelWorkBook = Excel.OpenExcel(r\'D:\x01.xlsx\', visible=True, appType="Excel", pwd="", writePwd="")

        :param filePath:[必选参数]Excel工作簿文件路径，如果指定路径不存在对应文件，该命令将在此路径创建该文件
        :param visible:[可选参数]是否已可视化的模式打开Excel。默认：True
        :param appType:[可选参数]使用Excel或者WPS打开。可填写”Excel“或者”WPS“。默认："Excel"
        :param pwd:[可选参数]工作薄的打开密码，创建新文件时忽略。默认：""
        :param writePwd:[可选参数]工作薄的编辑密码，创建新文件时忽略。默认：""
        :return:操作的工作簿对象，后续操作都会用到这个(excelWorkBook)
        '''
    @staticmethod
    def CloseExcel(excelWorkBook, save: bool = True) -> None:
        '''
        关闭Excel工作簿

        Excel.CloseExcel(excelWorkBook, save=True)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param save:[可选参数]退出时是否进行保存。默认True
        :return:None
        '''
    @staticmethod
    def BindBook(fileName: str, isFocus: bool = True, matchCase: bool = False) -> xw.Book:
        """
        绑定Excel工作簿

        Excel.BindBook(fileName, isFocus=True, matchCase=False)

        :param fileName:[必选参数]已经打开的Excel工作簿文件名。
        :param isFocus:[可选参数]如果是True, 把Excel窗口显示到最上层，并且把焦点切换到Excel。默认True
        :param matchCase:[可选参数]文档标题匹配时是否区分大小写字母。区分True，忽略False。默认False
        :return:操作的工作簿对象，后续操作都会用到这个(excelWorkBook)
        """
    @staticmethod
    def Save(excelWorkBook) -> None:
        '''
        保存Excel工作簿

        Excel.Save(excelWorkBook)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :return:None
        '''
    @staticmethod
    def SaveOtherFile(excelWorkBook, filePath: str) -> None:
        '''
        另存Excel工作簿

        Excel.SaveOtherFile(excelWorkBook, filePath=r"D:\test\test.xlsx")

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param filePath:[必选参数]另存为文件的文件路径（如果没有文件夹时，创建文件夹）
        :return:None
        '''
    @staticmethod
    def ActiveBook(excelWorkBook, isFocus: bool = True) -> None:
        '''
        激活Excel工作簿窗口

        Excel.ActiveBook(excelWorkBook, isFocus=True)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param isFocus:[可选参数]如果是True, 把Excel窗口显示到最上层，并且把焦点切换到Excel。默认True
        :return:None
        '''
    @staticmethod
    def Find(excelWorkBook, sheet: str | int = 'Sheet1', cellRange: str | list = 'A1:B2', findValue: str = '', retIndex: bool = False, retAll: bool = False, allMatch: bool = False, matchCase: bool = False) -> str | list:
        '''
        查找数据

        Excel.Find(excelWorkBook, sheet="Sheet1", cellRange="A1:B2", findValue="", retIndex=False, retAll=False, allMatch=False, matchCase=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cellRange:[可选参数]指定的区域，支持单元格名如"A1:B2"与二维行列数组如[[第1个单元格行号，第1个单元格列号],[第2个单元格行号，第2个单元格列号]]两种形式，使用单元格名时不区分大小写。当只写一个单元格时，读取从单元格开始到此表最后有数据的地方。默认"A1:B2"
        :param findValue:[可选参数]需要查找的数据内容。默认""
        :param retIndex:[可选参数]是否返回单元格索引，True返回[行号,列号]形式的单元格索引，False返回字母加数字的单元格名称。默认False
        :param retAll:[可选参数]是否返回全部单元格，True返回数组包含所有查找到数据的单元格，False返回范围内第一个查找到数据的单元格。默认False
        :param allMatch:[可选参数]搜索内容是否完全匹配。完全匹配True，部分匹配False。默认False
        :param matchCase:[可选参数]搜索内容是否区分大小写字母。区分True，忽略False。默认False
        :return:查找结果
        '''
    @staticmethod
    def ReadCell(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', retStr: bool = False):
        '''
        读取单元格

        Excel.ReadCell(excelWorkBook, sheet="Sheet1", cell="A1", retStr=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号，列号]两种形式，当使用单元格名时不区分大小写。默认"A1"
        :param retStr:[可选参数]选择True，则返回内容与Excel单元格中显示的内容一致，且始终以字符串形式返回；选择否，则返回内容会根据数据类型自动转换，如0.1返回数值0.1而不是字符串"0.1"。默认False
        :return:指定单元格的值
        '''
    @staticmethod
    def ReadRange(excelWorkBook, sheet: str | int = 'Sheet1', cellRange: str | list = 'A1:B2', retStr: bool = False, excludeEndBlankRow: bool = False, excludeEndBlankColum: bool = False) -> list:
        '''
        读取区域

        Excel.ReadRange(excelWorkBook, sheet="Sheet1", cellRange="A1:B1", retStr=False, excludeEndBlankRow=False, excludeEndBlankColum=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cellRange:[可选参数]指定的区域，支持单元格名如"A1:B2"与二维行列数组如[[单元格1行号，单元格1列号],[单元格2行号，单元格2列号]]两种形式，使用单元格名时不区分大小写。当只写一个单元格时，读取从单元格开始到此表最后有数据的地方。默认"A1:B2"
        :param retStr:[可选参数]选择True，则返回内容与Excel单元格中显示的内容一致，且始终以字符串形式返回；选择否，则返回内容会根据数据类型自动转换，如0.1返回数值0.1而不是字符串"0.1"。默认False
        :param excludeEndBlankRow:[可选参数]如果为True，读取范围内，从最后一行开始倒序检查，如果该行全是空值，则排除该行，直到发现非全空值的行停止检查。默认False
        :param excludeEndBlankColum:[可选参数]如果为True，读取范围内，从最后一列开始倒序检查，如果该列全是空值，则排除该列，直到发现非全空值的列停止检查。默认False
        :return:指定单元格范围的值(二维列表)
        '''
    @staticmethod
    def ReadRow(excelWorkBook, sheet: str | int = 'Sheet1', rowFirstCell: str | list = 'A1', retStr: bool = False, excludeEndBlankCells: bool = False) -> list:
        '''
        读取行

        Excel.ReadRow(excelWorkBook, sheet="Sheet1", rowFirstCell="A1", retStr=False, excludeEndBlankCells=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param rowFirstCell:[可选参数]指定哪个单元格右侧的一整行（包含指定单元格），支持单元格名如"A1"与行列数组如[行号，列号]两种形式，当使用单元格名时不区分大小写
        :param retStr:[可选参数]选择True，则返回内容与Excel单元格中显示的内容一致，且始终以字符串形式返回；选择否，则返回内容会根据数据类型自动转换，如0.1返回数值0.1而不是字符串"0.1"。默认False
        :param excludeEndBlankCells:[可选参数]选择True，排除最后面连续的空单元格。默认False
        :return:指定单元格右侧一整行的所有值（包含指定单元格）(一维列表)
        '''
    @staticmethod
    def ReadColumn(excelWorkBook, sheet: str | int = 'Sheet1', columnFirstCell: str | list = 'A1', retStr: bool = False, excludeEndBlankCells: bool = False) -> list:
        '''
        读取列

        Excel.ReadColumn(excelWorkBook, sheet="Sheet1", columnFirstCell="A1", retStr=False, excludeEndBlankCells=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param columnFirstCell:[可选参数]指定哪个单元格下侧的一整列（包含指定单元格），支持单元格名如"A1"与行列数组如[行号，列号]两种形式，当使用单元格名时不区分大小写
        :param retStr:[可选参数]选择True，则返回内容与Excel单元格中显示的内容一致，且始终以字符串形式返回；选择否，则返回内容会根据数据类型自动转换，如0.1返回数值0.1而不是字符串"0.1"。默认False
        :param excludeEndBlankCells:[可选参数]选择True，排除最后面连续的空单元格。默认False
        :return:指定单元格下侧一整列的所有值（包含指定单元格）(一维列表)
        '''
    @staticmethod
    def GetRowsCount(excelWorkBook, sheet: str | int = 'Sheet1', excludeEndBlankRow: bool = False) -> int:
        '''
        获取行数

        Excel.GetRowsCount(excelWorkBook, sheet="Sheet1", excludeEndBlankRow=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param excludeEndBlankRow:[可选参数]如果为True，表格有效范围内，从最后一行开始倒序检查，如果该行全是空值，则继续向上行检查，直到该行是非全空值，则为最大行数。默认False
        :return:当前工作簿的最大行数
        '''
    @staticmethod
    def GetColumsCount(excelWorkBook, sheet: str | int = 'Sheet1', excludeEndBlankColum: bool = False) -> int:
        '''
        获取列数

        Excel.GetColumsCount(excelWorkBook, sheet="Sheet1", excludeEndBlankColum=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param excludeEndBlankColum:[可选参数]如果为True，表格有效范围内，从最后一列开始倒序检查，如果该列全是空值，则继续向左列检查，直到该列是非全空值，则为最大列数。默认False
        :return:当前工作簿的最大列数
        '''
    @staticmethod
    def MergeRange(excelWorkBook, sheet: str | int = 'Sheet1', cellRange: str | list = 'A1:B1', bOption: bool = True, bAcross: bool = False, isSave: bool = False) -> None:
        '''
        合并或拆分单元格

        Excel.MergeRange(excelWorkBook, sheet="Sheet1", cellRange="A1:B1", bOption=True, bAcross=False, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cellRange:[可选参数]合并或拆分的单元格范围，支持单元格名如"A1:B1"与行列数组如[[行号, 列号], [行号, 列号]]两种形式，当使用单元格名时不区分大小写。拆分时也可以指定独立的单元格，如"A1"或[1, 1]。默认"A1:B1"
        :param bOption:[可选参数]合并单元格或者取消合并，选择是合并单元格，选择否拆分单元格。默认True
        :param bAcross:[可选参数]如果设置为True，合并单元格时将指定区域中每一行的单元格合并为一个单独的合并单元格。默认值为False
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def WriteCell(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', data: str | list = '', strictlyWrite: bool = True, isSave: bool = False) -> None:
        '''
        写入单元格

        Excel.WriteCell(excelWorkBook, sheet="Sheet1", cell="A1", data="", strictlyWrite=True, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号, 列号]两种形式，当使用单元格名时不区分大小写。默认"A1"
        :param data:[可选参数]要写入的数据，支持写入公式。默认""
        :param strictlyWrite:[可选参数]严格的写入标准，选True：只能写入一个单元格的数据，选False：可写入多行多列的数据(则功能与WriteRow、WriteRange类似)。默认True
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def WriteRow(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', data: list = [1, '贰', 3, '肆'], strictlyWrite: bool = True, isSave: bool = False) -> None:
        '''
        写入行

        Excel.WriteRow(excelWorkBook, sheet="Sheet1", cell="A1", data=[1,\'贰\',3,\'肆\'], strictlyWrite=True, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号, 列号]两种形式，当使用单元格名时不区分大小写。默认"A1"
        :param data:[可选参数]要写入的数据，支持写入公式。默认""
        :param strictlyWrite:[可选参数]严格的写入标准，选True：只能写入一行的单元格数据，选False：可写入多行多列的数据(则功能与WriteRange类似)。默认True
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def DeleteRow(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | int = 'A1', isSave: bool = False) -> None:
        '''
        删除行

        Excel.DeleteRow(excelWorkBook,sheet="Sheet1",cell="A1",isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的行，可以使用单元格名称如\'A1\'定位，或者直接使用数字定位行号
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def WriteColumn(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', data: list = [1, '贰', 3, '肆'], strictlyWrite: bool = True, isSave: bool = False) -> None:
        '''
        写入列

        Excel.WriteColumn(excelWorkBook, sheet=\'Sheet1\', cell=\'A1\', data=[1,\'贰\',3,\'肆\'], strictlyWrite=True, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号, 列号]两种形式，当使用单元格名时不区分大小写。默认"A1"
        :param data:[可选参数]要写入的数据，支持写入公式。默认[1, \'贰\', 3, \'肆\']
        :param strictlyWrite:[可选参数]严格的写入标准，选True：只能写入一列的单元格数据，选False：可写入多行多列的数据(则功能与WriteRange类似)。默认True
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def DeleteColumn(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | int = 'A1', isSave: bool = False) -> None:
        '''
        删除列

        Excel.DeleteColumn(excelWorkBook, sheet="Sheet1", cell="A1", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的列，可以使用单元格名称如\'A1\'定位，或者直接使用数字定位列号
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def InsertRow(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', data: list = [1, '贰', 3, '肆'], isSave: bool = False) -> None:
        '''
        插入行

        Excel.InsertRow(excelWorkBook, sheet="Sheet1", cell="A1", data=[1, \'贰\', 3, \'肆\'], isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号, 列号]两种形式，新行从该单元格开始写入数据，当使用单元格名时不区分大小写。默认"A1"
        :param data:[可选参数]要写入的数据，支持写入公式。默认[1, \'贰\', 3, \'肆\']
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def InsertColumn(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', data: list = [1, '贰', 3, '肆'], isSave: bool = False) -> None:
        '''
        插入列

        Excel.InsertColumn(excelWorkBook, sheet="Sheet1", cell="A1", data=[1, \'贰\', 3, \'肆\'], isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号, 列号]两种形式，新列从该单元格开始写入数据，当使用单元格名时不区分大小写。默认"A1"
        :param data:[可选参数]要写入的数据，支持写入公式。默认[1, \'贰\', 3, \'肆\']
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def InsertImage(excelWorkBook: Incomplete | None = None, sheet: str | int = 'Sheet1', filePath: str = 'D:\\1.png', name: str = '', left: int = 0, top: int = 0, width: int = 100, height: int = 100, isSave: bool = False) -> None:
        '''
        插入图片

        Excel.InsertImage(excelWorkBook, sheet="Sheet1", filePath=r"D:\x01.png", name="", left=0, top=0, width=100, height=100, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param filePath:[可选参数]要插入的图片文件路径。默认r"D:\x01.png"
        :param name:[可选参数]默认值为空字符串，由Excel自动编排。如需删除或者更新相应图片，建议修改名字。默认""
        :param left:[可选参数]图片距离左边的边距。默认0
        :param top:[可选参数]图片距离顶部的边距。默认0
        :param width:[可选参数]图片的宽度，按原图的百分比计算。默认100
        :param height:[可选参数]图片的高度，按原图的百分比计算。默认100
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def DeleteImage(excelWorkBook, sheet: str | int = 'Sheet1', pic: str | int = 0, isSave: bool = False) -> None:
        '''
        删除图片

        Excel.DeleteImage(excelWorkBook, sheet="Sheet1", pic=0)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param pic:要删除的图片的顺序或名字，顺序从0开始(-1：所有添加图片的最后一个)
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def WriteRange(excelWorkBook, sheet: str | int = 'Sheet1', cell: str | list = 'A1', data: list = [[1, '壹'], [2, '贰'], [3, '叁']], transpose: bool = False, isSave: bool = False) -> None:
        '''
        写入区域

        Excel.WriteRange(excelWorkBook, sheet="Sheet1", cell="A1", data=[[1, \'壹\'], [2, \'贰\'], [3, \'叁\']], transpose=False, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cell:[可选参数]指定的单元格，支持单元格名如"A1"与行列数组如[行号，列号]两种形式，当使用单元格名时不区分大小写。默认"A1"
        :param data:[可选参数]要写入的二维列表，若使用的二维列表内的子列表长度没对齐，会自动使用空值对齐列表之后进行写入，请注意影响以免发生值覆盖。默认[[1, \'壹\'], [2, \'贰\'], [3, \'叁\']]
        :param transpose:[可选参数]选择True，数据纵向写入，选择False，数据横向写入。默认False
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SelectRange(excelWorkBook, sheet: str | int = 'Sheet1', cellRange: list = 'A1:B2') -> None:
        '''
        选中区域

        Excel.SelectRange(excelWorkBook, sheet="Sheet1", cellRange="A1:B2")

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cellRange:[可选参数]选中的单元格范围，支持单元格名如"A1:B1"与行列数组如[[行号, 列号], [行号, 列号]]两种形式，当使用单元格名时不区分大小写。默认"A1:B1"
        :return:None
        '''
    @staticmethod
    def ClearRange(excelWorkBook, sheet: str | int = 'Sheet1', cellRange: list = 'A1:B2', clearFormat: bool = False, isSave: bool = False) -> None:
        '''
        清除区域

        Excel.ClearRange(excelWorkBook, sheet="Sheet1", cellRange="A1:B2", clearFormat=False, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cellRange:[可选参数]清除的单元格范围，支持单元格名如"A1:B1"与行列数组如[[行号, 列号], [行号, 列号]]两种形式，当使用单元格名时不区分大小写。默认"A1:B1"
        :param clearFormat:[可选参数]是否清除所选区域格式。默认False
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def DeleteRange(excelWorkBook, sheet: str | int = 'Sheet1', cellRange: list = 'A1:B2', shift: str | None = None, isSave: bool = False) -> None:
        '''
        删除区域

        Excel.DeleteRange(excelWorkBook, sheet="Sheet1", cellRange="A1:B2", shift=None, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cellRange:[可选参数]删除的单元格范围，支持单元格名如"A1:B1"与行列数组如[[行号, 列号], [行号, 列号]]两种形式，当使用单元格名时不区分大小写。默认"A1:B1"
        :param shift:[可选参数]填写"up"时(不区分大小写)，删除的区域下面向上移动，填写"left"时(不区分大小写)，删除的区域右侧向左移动，填写None时，Excel根据区域的形状决定。默认None
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetColumnWidth(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', fWidth: float | int | None = 8.38, isSave: bool = False) -> None:
        '''
        设置列宽

        Excel.SetColumnWidth(excelWorkBook, sheet="Sheet1", cells="A1", fWidth=8.38, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param fWidth:[可选参数]调整的列宽,在0磅至255磅之间，当填写其他值或None时，将自动调整。默认8.38
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetRowHeight(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', fHeight: float | int | None = 14.25, isSave: bool = False) -> None:
        '''
        # 设置行高

        Excel.SetRowHeight(excelWorkBook, sheet="Sheet1", cells="A1", fHeight=14.25, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param fHeight:[可选参数]调整的行高，在0磅至409.5磅之间，当填写其他值或None时，将自动调整。默认14.25
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellColor(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', cellColor: str | list = [255, 255, 255], isSave: bool = False) -> None:
        '''
        设置单元格（或区域）背景颜色

        Excel.SetCellColor(excelWorkBook, sheet="Sheet1", cells="A1", cellColor=[255, 255, 255], isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param cellColor:[可选参数]列表形式的RGB颜色，如[255, 255, 255] 或 字符串形式的16进制颜色码，如"FFFFFF"。字符串形式时不区分大小写。默认[255, 255, 255]
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellFontColor(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', fontColor: str | list = [255, 255, 255], isSave: bool = False) -> None:
        '''
        设置单元格（或区域）字体颜色

        Excel.SetCellFontColor(excelWorkBook, sheet="Sheet1", cells="A1", fontColor=[255, 255, 255], isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param fontColor:[可选参数]列表形式的RGB颜色，如[255, 255, 255] 或 字符串形式的16进制颜色码，如"FFFFFF"。字符串形式时不区分大小写。默认[255, 255, 255]
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def CreateSheet(excelWorkBook, newSheetName: str = None, addWhere: str = 'after', isSave: bool = False) -> None:
        '''
        创建工作表

        Excel.CreateSheet(excelWorkBook, newSheetName="newSheet", addWhere="after", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param newSheetName:新工作表的名字，字符串类型，如果没有就使用Excel给的缺省名字。默认None
        :param addWhere:填写"after"时，在当前的工作表后面创建，填写"before"时，在当前的工作表前面创建。默认"after"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def CurrentSheet(excelWorkBook, retName: bool = True) -> str | int:
        '''
        获取当前工作表

        Excel.CurrentSheet(excelWorkBook, retName=True)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param retName:选择True返回表名，选择False返回表索引。默认True
        :return:工作表名(str)或者索引(int)
        '''
    @staticmethod
    def GetSheetsName(excelWorkBook) -> list:
        '''
        获取所有工作表名

        Excel.GetSheetsName(excelWorkBook)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :return:所有工作表的名字
        '''
    @staticmethod
    def SheetRename(excelWorkBook, sheet: str | int = 'Sheet1', newSheetName: str = 'newName', isSave: bool = False) -> None:
        '''
        重命名工作表

        Excel.SheetRename(excelWorkBook, sheet="Sheet1", newSheetName="newName", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param newSheetName:[可选参数]重命名后的工作表名称。默认"newName"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def CopySheet(excelWorkBook, sheet: str | int = 'Sheet1', newSheetName: str = 'newName', newSheetWhere: str = 'before', isSave: bool = False) -> None:
        '''
        复制工作表

        Excel.CopySheet(excelWorkBook, sheet="Sheet1", newSheetName="newName", newSheetWhere="before", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]需要复制的工作表，如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param newSheetName:[可选参数]重命名后的工作表名称。默认"newName"
        :param newSheetWhere:[可选参数]填写"before"时，复制到指定工作表前面相邻位置，填写"after"时，复制到指定工作表后面相邻位置。默认"before"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def ActiveSheet(excelWorkBook, sheet: str | int = 'Sheet1') -> None:
        '''
        激活工作表

        Excel.ActiveSheet(excelWorkBook, sheet="Sheet1")

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :return:None
        '''
    @staticmethod
    def DeleteSheet(excelWorkBook, sheet: str | int = 'Sheet1', isSave: bool = False) -> None:
        '''
        删除工作表

        Excel.DeleteSheet(excelWorkBook, sheet="Sheet1", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def ExecuteMacro(excelWorkBook, macro: str = '', listArgs: list = None):
        '''
        执行宏

        Excel.ExecuteMacro(excelWorkBook, "test", [3])

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param macro:[可选参数]Excel中的宏定义名称，可以是sub、function(如宏是Sub test() ...，此参数应填写"test")
        :param listArgs:[可选参数]需要传给宏定义的属性，如调用subSum(1,2)，则传递[1,2]
        :return:宏的返回值
        '''
    @staticmethod
    def SetFontSizeBold(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', fontSize: int = None, fontBold: bool = None, isSave: bool = False) -> None:
        '''
        设置单元格字体大小粗细

        Excel.SetFontSizeBold(excelWorkBook, sheet="Sheet1", cells="A1", fontSize=24, fontBold=True, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param fontSize:[可选参数]字体的大小，数字填写范围在1-409范围内，填写None时不进行设置。默认None
        :param fontBold:[可选参数]字体是否加粗，选择True则加粗，选择False取消加粗，填写None时不进行设置。默认None
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsAlignmentFormat(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', horizontal: str = None, vertical: str = None, isSave: bool = False) -> None:
        '''
        设置单元格对齐格式

        Excel.SetCellsAlignmentFormat(excelWorkBook, sheet="Sheet1", cells="A1", horizontal="center", vertical="center", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param horizontal:水平对齐方式，填写"left"时水平靠左，填写"right"时水平靠右，填写"center"时水平居中，填写None时不设置保持现状。默认None
        :param vertical:垂直对齐方式，填写"up"时垂直靠上，填写"down"时垂直靠下，填写"center"时垂直居中，填写"auto"时自动换行对齐，填写None时不设置保持现状。默认None
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatGeneral(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', isSave: bool = False) -> None:
        '''
        设置单元格数字格式为常规

        Excel.SetCellsNumFormatGeneral(excelWorkBook, sheet="Sheet1", cells="A1", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatNumber(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', decimalPlaces: int = 2, use1000Separator: bool = False, isSave: bool = False) -> None:
        '''
        设置单元格数字格式为数值

        Excel.SetCellsNumFormatNumber(excelWorkBook, sheet="Sheet1", cells="A1", decimalPlaces=2, use1000Separator=False, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param decimalPlaces:[可选参数]保留的小数位数（只能选择0-30范围内）。默认2
        :param use1000Separator:[可选参数]选择True时使用千分位，否则不使用。默认False
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatCurrency(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', symbol: str = 'CHN', decimalPlaces: int = 2, isSave: bool = False) -> None:
        '''
        设置单元格数字格式为货币

        Excel.SetCellsNumFormatCurrency(excelWorkBook, sheet="Sheet1", cells="A1", symbol="CHN", decimalPlaces=2, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param symbol:[可选参数]货币符号，填写"CHN"会有"￥"，填写"USA"会有"$",填写"USA2"会有"US$"，填写""为没有符号。默认"CHN"
        :param decimalPlaces:[可选参数]保留的小数位数（只能选择0-30范围内）。默认2
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatAccounting(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', symbol: str = 'CHN', decimalPlaces: int = 2, isSave: bool = False) -> None:
        '''
        设置单元格数字格式为会计专用

        Excel.SetCellsNumFormatAccounting(excelWorkBook, sheet="Sheet1", cells="A1", symbol="CHN", decimalPlaces=2, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param symbol:[可选参数]货币符号，填写"CHN"会有"￥"，填写"USA"会有"$",填写"USA2"会有"US$"，填写""为没有符号。默认"CHN"
        :param decimalPlaces:[可选参数]保留的小数位数（只能选择0-30范围内）。默认2
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatDate(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', dataType: str = 'y/m/d/h:m', isSave: bool = False) -> None:
        '''
        设置单元格数字格式为日期

        Excel.SetCellsNumFormatDate(excelWorkBook, sheet="Sheet1", cells="A1", dataType=\'y/m/d/h:m\', isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param dataType:填写"y/m/d/h:m"时，格式为"2023/12/31 13:30"，填写"ymdCN"时，格式为"2023年12月31日"，填写"y/m/d"时，格式为"2023/12/31"。默认\'y/m/d/h:m\'
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatTime(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', timeType: str = 'hmsCN', isSave: bool = False) -> None:
        '''
        设置单元格数字格式为时间

        Excel.SetCellsNumFormatTime(excelWorkBook, sheet="Sheet1", cells="A1", timeType=\'hmsCN\', isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param timeType:填写"h:m:s"时，格式为"13:30:50"，填写"h:m"时，格式为"13:30"，填写"hmsCN"时，格式为"13时30分50秒"，填写"hmCN"时，格式为"13时30分"。默认"hmsCN"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatPercentage(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', decimalPlaces: int = 2, isSave: bool = False) -> None:
        '''
        设置单元格数字格式为百分比

        Excel.SetCellsNumFormatPercentage(excelWorkBook, sheet="Sheet1", cells="A1", decimalPlaces=2, isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param decimalPlaces:[可选参数]保留的小数位数（只能选择0-30范围内）。默认2
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatText(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', isSave: bool = False) -> None:
        '''
        设置单元格数字格式为文本

        Excel.SetCellsNumFormatText(excelWorkBook, sheet="Sheet1", cells="A1", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def SetCellsNumFormatChnNum(excelWorkBook, sheet: str | int = 'Sheet1', cells: str | list = 'A1', case: str = 'B', isSave: bool = False) -> None:
        '''
        设置单元格数字格式为中文大写或小写

        Excel.SetCellsNumFormatChnNum(excelWorkBook, sheet="Sheet1", cells="A1", case="B", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param cells:[可选参数]指定的单元格或单元格范围，支持单元格名如"A1"或"A1:B1"与行列数组如[行号, 列号]或[[行号, 列号], [行号, 列号]]四种格式，当使用单元格名时不区分大小写。默认"A1"
        :param case:[可选参数]填写"B"时为中文大写数字，填写"b"时为中文小写数字。默认"B"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def AutoFill(excelWorkBook, sheet: str | int = 'Sheet1', srcRange: str | list = 'A1:A2', distRange: str | list = 'A1:A10', isSave: bool = False) -> None:
        '''
        自动填充区域

        Excel.AutoFill(excelWorkBook, sheet="Sheet1", srcRange="A1:A2", distRange="A1:A10", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param srcRange:[可选参数]指定的区域，支持单元格名如"A1:B2"与二维行列数组如[[单元格1行号，单元格1列号],[单元格2行号，单元格2列号]]两种形式，使用单元格名时不区分大小写。默认\'A1:A2\'
        :param distRange:[可选参数]要填充的区域，必须包括源区域，支持单元格名如"A1:B2"与二维行列数组如[[单元格1行号，单元格1列号],[单元格2行号，单元格2列号]]两种形式，使用单元格名时不区分大小写。默认\'A1:A10\'
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
    @staticmethod
    def RefreshPivotTables(excelWorkBook, sheet: str | int = 'Sheet1', isSave: bool = False) -> None:
        '''
        更新数据透视图

        Excel.RefreshPivotTables(excelWorkBook, sheet="Sheet1", isSave=False)

        :param excelWorkBook:[必选参数]使用 "打开Excel工作簿"命令（Excel.OpenExcel） 或 "绑定Excel工作簿" 命令（Excel.BindBook）返回的工作簿对象
        :param sheet:[可选参数]如果使用字符串，则表示指定工作表的名字；使用数字，则表示指定工作表的顺序（从0开始）。默认"Sheet1"
        :param isSave:[可选参数]操作完成立即保存。默认False
        :return:None
        '''
