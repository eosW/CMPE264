import cv2
from composite import composite
from ToneMapping import ToneMapping

c = composite()
t = ToneMapping()
cv2.imwrite("alg1.jpg", t.map(c.alg1()))
cv2.imwrite("alg2.jpg", t.map(c.alg2()))
cv2.imwrite("alg3.jpg", t.map(c.alg3()))
