import numpy as np

x_coords = [1,5]
y_coords = [2,6]
radius = [2,1]

size = 10

res = 24

factor = int(res/size)

arr = np.zeros((res,res))


for i in range(len(x_coords)):
    x_coords[i] = x_coords[i] * factor
    y_coords[i] = y_coords[i] * factor
    radius[i] = radius[i] * factor


for x,y,r in zip(x_coords,y_coords,radius):
  for i in range(size*factor):
    for j in range(size*factor):
      if (x - i)**2 + (y - j)**2 < r**2:
        arr[i][j] = 1

print(arr)