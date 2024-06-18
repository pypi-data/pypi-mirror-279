# Zyro PY - Esempi di Utilizzo

## Regressione Lineare

```python
import numpy as np
from zyro_py.ml.linear_regression import LinearRegression

# Dataset
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3

# Modello di Regressione Lineare
model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)

print("Predictions:", predictions)
