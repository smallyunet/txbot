
rais = [
    "看涨",
    "RSI底背离",
    "上穿MA5",
    "多头排列",
]

fail = [
    "看跌",
    "RSI顶背离",
    "下穿MA5",
    "空头排列",
]

print("----")
for i in range(len(rais)):
    print(rais[i].encode('utf-8'))

print("----")
for i in range(len(fail)):
    print(fail[i].encode('utf-8'))

print("----")
print("【标的】".encode('utf-8'))

print("----")
mail_content = """
【标的】T/USDT
【交易所】币安
【级别】4H
【现价】$8.85
【4H额】$67.47万
【流通市值】$6.24亿
【信号】上穿MA5
【时间】2023-02-06 08:00:00


说明：
1.本消息为MA5短线策略订阅内容的推送，可在信号-MA5短线策略订阅处反勾选“已接收订阅推送”进行取消推送。
2.可回复本邮件，解除邮件接收次数限制。
"""
k = "T"
kStr = b'\xe3\x80\x90\xe6\xa0\x87\xe7\x9a\x84\xe3\x80\x91'.decode('utf-8') + k + '/USDT'
print(kStr)
print(kStr in mail_content)