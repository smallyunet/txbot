
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

for i in range(len(rais)):
    print(rais[i].encode('utf-8'))

for i in range(len(fail)):
    print(fail[i].encode('utf-8'))
