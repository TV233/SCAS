import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, Activation, Input
from tensorflow.keras.optimizers import Adam

# 加载CSV数据
data = pd.read_csv('../lstm/1_601360_klines.csv')

# 提取股票的收盘价格
x0 = data[['close']].values

# 归一化处理数据
scaler = MinMaxScaler(feature_range=(0, 1))
x0 = scaler.fit_transform(x0)

# 创建数据集
n = len(x0)
p = 30  # 时间步长窗口
x = np.array([x0[i:i+p] for i in range(n-p+1)])
y = np.array(x0[p:])

# 对输入数据进行调整，符合 CNN 的输入要求
X = x[:-1]
X = X[:, :, np.newaxis]

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# 创建 CNN 模型
model = Sequential()
model.add(Input(shape=(p, 1)))  # Input layer
model.add(Conv1D(50, 4, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(20))
model.add(Dropout(0.2))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# 编译模型
optimizer = Adam(learning_rate=0.01)
model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

# 训练模型
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# 预测
y_pred = model.predict(X_test)

# 将测试集和预测的值进行可视化对比
plt.plot(scaler.inverse_transform(y_test), label='Actual Price')
plt.plot(scaler.inverse_transform(y_pred), label='Predicted Price', color='red')
plt.legend()
plt.show()

# 模型训练完毕后，我们使用最后的20天数据来预测未来的股票价格
def predict_next_day(model, last_30_days):
    # 归一化最近20天的数据
    last_30_days_scaled = scaler.transform(last_30_days)

    # Reshape 数据，使其符合模型的输入要求，形状应为 (1, p, 1)
    last_30_days_scaled = last_30_days_scaled.reshape((1, p, 1, 1))  # (batch_size, time_steps, features)

    # 预测下一天的价格
    next_day_pred = model.predict(last_30_days_scaled)

    # 将预测值逆归一化回原来的价格范围
    next_day_pred_rescaled = scaler.inverse_transform(next_day_pred)

    return next_day_pred_rescaled[0][0]


# 使用最近20天的数据进行未来股价预测
last_30_days = data['close'].values[-p:].reshape(-1, 1)
print(last_30_days)
next_day_price = predict_next_day(model, last_30_days)
print(f"Predicted stock price for the next day: {next_day_price}")

