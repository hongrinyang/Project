import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 가상의 코스별 타율 데이터 (예시)
x = np.linspace(1, 5, 5)
y = np.linspace(1, 5, 5)
x, y = np.meshgrid(x, y)
z = np.random.rand(5, 5)  # 임의의 타율 데이터 생성

# 3차원 그래프 그리기
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(x, y, z, cmap='viridis')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Batting Average')

plt.title('3D Surface Plot of Batting Average by Hot/Cold Zone')

plt.show()

# 2차원 색깔 플롯 그리기
plt.imshow(z, cmap='coolwarm', extent=[1, 5, 1, 5], origin='lower')
plt.colorbar(label='Batting Average')  # 컬러바 추가
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('2D Color Plot of Batting Average by Hot/Cold Zone')

plt.show()
