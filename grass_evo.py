import random
import copy
import math
import os
import datetime

import matplotlib.pyplot as plt
import matplotlib.colors


TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
os.makedirs(f'./runs/{TIME}')
COLORS = list(matplotlib.colors.CSS4_COLORS.keys())

ACTORS_N = 10
X_POSITIONS = [x for x in range(ACTORS_N)]
EPOCHS = 50
SAVE_IMAGE_EACH_N_EPOCHS = EPOCHS / 10
SECTIONS = 10
SECTION_LENGTH = 1
INIT_EXPLR_RATE = 1
EXPLR_RATE_DECREASE = 0.9  # Multiply
MIN_EXPLR = 0.001

XLIM = [-1, ACTORS_N]
YLIM = [0, 10 + 1]
plt.xlim(XLIM)
plt.ylim(YLIM)

def random_color():
    return COLORS[random.randint(0, len(COLORS) - 1)]

def randangle():
    return 2 * math.pi * random.random() * random.choice((-1, 1))


def to_cartesian(model):
    displacements = []
    for angle in model:
        displacements.append((math.cos(angle) * SECTION_LENGTH, math.sin(angle) * SECTION_LENGTH))
    return displacements

models = []
rewards = []
alpha = [randangle() for _ in range(SECTIONS)]  # Angles
for epoch in range(1, EPOCHS + 1):
    for i in range(ACTORS_N):
        model = copy.deepcopy(alpha)  # Alpha reproduces
        for step in range(SECTIONS):
            prev_angle = model[step]
            angle = randangle() * INIT_EXPLR_RATE * max(MIN_EXPLR, EXPLR_RATE_DECREASE ** epoch)
            model[step] = prev_angle + angle
        models.append(model)
        cartesian = to_cartesian(model)
        x = X_POSITIONS[i]
        y = 0
        xs = [x]
        ys = [y]
        for coord in cartesian:
            x += coord[0]
            y += coord[1]
            xs.append(x)
            ys.append(y)
        rewards.append(y)  # The reward is y
        if epoch % SAVE_IMAGE_EACH_N_EPOCHS == 0 or epoch == 1:
            plt.plot(xs, ys, color="green")  # Paths
    zipped = []
    for m, r in zip(models, rewards):
        zipped.append((m, r))
    alpha = models[rewards.index(max(rewards))]
    models = []
    rewards = []
    if epoch % SAVE_IMAGE_EACH_N_EPOCHS == 0 or epoch == 1:
        plt.savefig(f'./runs/{TIME}/{epoch}')
        plt.clf()
        plt.xlim(XLIM)
        plt.ylim(YLIM)