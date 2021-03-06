# 众创神捕1.0 使用指南

**<u>众创神捕</u>**是一个用于批量发送短信的应用。在这里，您可以自建短信模板，并导入收信号码以及相应的变量，选定模板发送后，**<u>众创神捕</u>**会自动套用模板将包含变量的短信批量发送给相应的收信人。

**<u>众创神捕 1.0</u>**包含三个主要模块：*<u>模板导入</u>*、*<u>短信群发</u>* 和 *<u>历史查看</u>*。 点击本页面左侧导航栏即可进入相应的模块。

为了您保持心情舒畅，我们强烈建议您使用Chrome浏览器访问本网页，并于使用前认真阅读本指南。



## 模板导入

本模块主要包含 *<u>新增模板</u>*、*<u>模板查看</u>*、*<u>模板编辑</u>*、 *<u>模板删除</u>* 四个主要功能。

该页面会默认显示储存的所有模板的信息列表。

### 新增模板

> 点击页面右上角的 “新增” 按钮，进入表单填写页——新增模板，您只需输入模板名称、模板主题、模板内容 和 备注（非必填项），最后点击页面最下方的“提交”按钮即可。
>
> 提交后，将自动返回模板导入主页面。
>
> 使用时请注意：
>
> - 请保证您所命名之模板名称**不存在重名**情况。
> - 若您需要在模板中添加变量，变量请在**英文输入环境下**用**{n}**占位，如：{1},{2},{3}...
> - 同时，您需注意，请保证您输入的占位符{n}，中的数字n对应该模板中变量的**位置排序号**，最先出现的变量用{1}占位，第二个出现的变量用{2}占位，并以此类推。

### 模板查看

> 点击位于您希望查看的模板的信息同行的“查看”按钮，页面将自动弹出该模板的详情，点击“确定”可退出查看。

### 模板编辑

> 点击位于您希望查看的模板的信息同行的“编辑”按钮，进入表单编辑页——编辑模板，此处您可参照新增模板的操作编辑模板内容，最后点击页面最下方的“提交”按钮即可。
>
> 为了方便您事后对历史记录进行统计归档，我们只建议您使用该功能对模板内容进行小幅修改调整，不建议您进行以下类型的编辑操作：
>
> 1. 修改模板名称
> 2. 修改模板主题
> 3. 增删模板中的变量

### 模板删除

> 删除分为 *删除单个模板* 和 *删除选中*。
>
> 点击位于您希望删除的模板同行右侧的“删除按钮”即删除该模板。
>
> 您也可以在表格左侧多选框中勾选多个模板后，点击右上角“删除选中”按钮批量删除选中的模板。（最上方的勾选框可实现“全选”/“全不选”操作）



## 短信群发

群发短信时，我们建议您记住页面左上方显示的当前批次，这标记了您当前发送的批次是今日发送的第几批，稍后您可利用该批次号进入历史查看页查看批量发送的结果。

群发操作在此不做赘述。需要注意的事项如下：

- 上传的文件必须是**CSV(逗号分隔)(*.csv)**格式，文件中请不要加标题行，保持文件第一列为手机号码**（手机号码数字前请打'号转成文本格式）**，各变量请按顺序排放右侧若干列**（请不要放置空列）**
- 点下“立即发送”按钮后，文件上传需要时间，请耐心等待，批量发送成功后会自动进入历史查看页面。
- 若发送不成功，20S+后，页面还将停留在短信群发页。这时我们建议您先去查看模板中的变量个数是否同文件中变量个数保持一致，并且确认上传的文件格式、内容符和上述要求。



## 历史查看

历史查看页您只需填写您需要限制查询字段，点击“查询”按钮后将自动跳转到查询结果页。

历史消息列表中，您将在最右侧列中看到发送结果，该结果以 返回码 显示，返回码表示的实际意义如下表：

| 返回码 | 说明             |
| :----: | :--------------- |
|  200   | 查询成功         |
|  400   | 输入参数错误     |
|  401   | 未授权账户       |
|  402   | 使用条数用完     |
|  404   | 服务不支持       |
|  410   | 服务不再支持     |
|  420   | 用户过期         |
|  421   | 用户禁用         |
|  422   | 账户余额不足     |
|  423   | 服务未开启       |
|  499   | 未知错误         |
|  500   | 内部执行异常     |
|  504   | 数据查询异常     |
|  511   | 解密错误         |
|  512   | 解析数据格式错误 |

