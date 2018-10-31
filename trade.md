# 

1. 用户验证

/trade/sign?username=xxxx&password=xxxx&...


get: 登入

post: 注册

delete: 登出

2. 查询持仓

/trade/positions?


4. 查询委托单


/trade/order?orderid=xxx&&username=xxxx

查询未成交/已成交/已撤单

6. 买入/卖出

/trade/insert


params:

code: str
amount: str
price : str
towards: str
market


post

delete
