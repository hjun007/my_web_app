这是一个简单的Python Web项目，使用Flask框架。
你可以使用这个项目来学习Flask框架的基本使用。
你目前处于项目的根目录中，你需要在根目录中生成项目必须的文件，使得项目可以直接运行。


<!--
{
    "wtcsjg": 350,                      # 委托价格
    "tygpbh": "47858775559",             # 统一编号
    "gpid": 780608596,                   # 挂牌ID
    "cqmc": "萧山",                      # 城区名称
    "xzqh": 330181,                      # 行政区划
    "xqmc": "锦粼云荟院",                 # 小区名称
    "cjsj": "2024-11-02",                 # 挂牌时间
    "gpfyid": 4785877,                   # 挂牌房源ID
    "jzmj": 96.43,                       #建筑面积
    "fwtybh": "230416ZJ407725",          #房屋统一编号
    "scgpshsj": "2024-11-08",              #挂牌时间
    "mdmc": "杭州巨隆房地产营销策划有限公司",    #挂牌机构名称
    "gplxrxm": "张云"                       #挂牌人姓名
}

{
    "wtcsjg": 570,                                        #委托价格
    "tygpbh": "47827435275",                                #统一编号
    "gpid": 779854870,                                       #挂牌ID
    "cqmc": "拱墅区",                                         #城区名称
    "xzqh": 33,                                              #行政区划
    "xqmc": "万家星城",                                       #小区名称
    "cjsj": "2024-10-30",                                      #挂牌时间
    "gpfyid": 4782743,                                         #挂牌房源ID
    "jzmj": 139.3,                                             #建筑面积
    "fwtybh": "241030GE274353",                                #房屋统一编号
    "scgpshsj": "2024-11-04",                                   #挂牌时间
    "mdmc": "浙江链家房地产经纪有限公司杭州万家星城二店",             #挂牌机构名称
    "gplxrxm": "崔志琴"                                           #挂牌人姓名   
}

{
    gply: 
    wtcsjg: 
    jzmj: 
    ordertype: 
    fwyt: 
    hxs: 
    xzqh: 
    secondxzqh: 
    wtcsjgMin: 
    wtcsjgMax: 
    starttime: 2024-11-06
    endtime: 2024-11-06
    keywords: 万家星城
    page: 1
    xqid: 0
}
-->

# 在现有的功能上完成以下任务
0. 完成用户注册功能
    0.1 主页左上角增加注册按钮
    0.2 点击注册按钮后弹出注册页面
    0.3 注册页面包含用户名、密码、确认密码、邮箱等信息
    0.4 注册成功后弹出提示框，提示注册成功，同时把注册信息写入数据库
    0.5 注册成功后自动完成登陆，使用session记录用户信息
1. 完成用户登陆功能
    1.1 主页左上角增加登陆按钮
    1.2 登陆后在主页右上角显示用户名
    1.3 点击用户名后弹出下拉框，显示用户信息和退出按钮
    1.4 点击退出按钮后退出登陆，跳转回主页
    1.5 登陆后才能进行订阅房源功能和邮箱订阅功能
2. 小区的订阅功能与当前用户绑定
    2.1 订阅的小区存储在数据库中
    2.2 订阅的小区只能由当前用户查看
3. 邮箱的订阅功能与当前用户绑定
    3.1 邮箱的订阅信息存储在数据库中
    3.2 邮箱的订阅信息只能由当前用户查看

#以上功能已完成
# 下一阶段开发任务
0. 小区详情页面美化
1. 发送订阅邮件，可设置发送时间
