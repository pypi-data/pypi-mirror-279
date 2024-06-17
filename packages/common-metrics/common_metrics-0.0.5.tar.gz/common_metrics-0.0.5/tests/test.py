from common_metrics.metrics import eer, iapar, frr, threshold
import numpy as np

genuine = np.random.rand(1, 10_000)
morph = np.random.rand(1, 10_000)

th = threshold(genuine, 0.1)
print(th)

print(iapar(morph, th))
print(frr(genuine, th))

print("Deer:", eer(genuine, morph))
