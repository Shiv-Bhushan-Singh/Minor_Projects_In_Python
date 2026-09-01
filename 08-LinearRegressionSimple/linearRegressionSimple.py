import numpy as np

X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

w, b = 0.0, 0.0
lr = 0.01

for epoch in range(1000):
    y_pred = w * X + b
    error = y_pred - y
    dw = (2 / len(X)) * np.dot(error, X)
    db = (2 / len(X)) * np.sum(error)
    w -= lr * dw
    b -= lr * db

print(f"w: {w:.2f}, b: {b:.2f}")
print(f"Prediction for x=6: {w*6+b:.2f}")