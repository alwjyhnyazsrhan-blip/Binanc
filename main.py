import ccxt
import pandas as pd

# ضع مفاتيح الـ Testnet هنا
api_key = "MgzFNP74j4UgK3Vlosd2hVN2F5Rq 7nRNrpvTkdTFH4kgr6VxYYWeJtEoD yY4mvVX"
api_secret = "6N2FZuyvvzTALzRfhizsu11BHppJ9J 97a4aJTk7NMpVD1uevRdtsj8jPmw88rn64"

# تفعيل الاتصال مع Binance Testnet
binance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})
binance.set_sandbox_mode(True)  # مهم جداً لتجارب Testnet

# جلب بيانات الشموع (Candlesticks)
ohlcv = binance.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=50)

# تحويل البيانات إلى DataFrame
df = pd.DataFrame(ohlcv, columns=["timestamp","open","high","low","close","volume"])

# حساب Pivot Points (Classic)
last_high = df["high"].iloc[-2]
last_low = df["low"].iloc[-2]
last_close = df["close"].iloc[-2]

pivot = (last_high + last_low + last_close) / 3
support1 = (2 * pivot) - last_high
resistance1 = (2 * pivot) - last_low

print("Pivot:", pivot)
print("Support1:", support1)
print("Resistance1:", resistance1)

# السعر الحالي
current_price = df["close"].iloc[-1]
quantity = 0.001

# منطق مبسط: شراء عند الدعم، بيع عند المقاومة
if current_price <= support1:
    order = binance.create_market_buy_order('BTC/USDT', quantity)
    print("تم تنفيذ شراء:", order)

elif current_price >= resistance1:
    order = binance.create_market_sell_order('BTC/USDT', quantity)
    print("تم تنفيذ بيع:", order)
else:
    print("لا توجد إشارة دخول حالياً")
