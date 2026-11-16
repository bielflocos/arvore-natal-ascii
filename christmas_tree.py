"""Recriação independente do visual de dwcminh.ascii. Python 3.10+.
Execute: python christmas_tree.py | Teste: python christmas_tree.py --capture preview.png
"""
import argparse
import math
import os
from pathlib import Path

import numpy as np

COLS, ROWS = 88, 74
CW, CH = 9, 12
WIDTH, HEIGHT = COLS * CW, ROWS * CH
BG = (3, 10, 14)
GREEN = (40, 160, 88)
GOLD = (255, 206, 82)
WHITE = (211, 234, 241)
RED = (223, 49, 61)
BLUE = (63, 98, 225)


def build_scene():
    rng = np.random.default_rng(7)
    points, colors, symbols, births, kinds, normals, ambient = [], [], [], [], [], [], []

    def add(x, y, z, color, char, birth, kind=0, normal=None, ao=1.):
        points.append((x, y, z))
        colors.append(color)
        symbols.append(char)
        births.append(birth)
        kinds.append(kind)
        normal = np.array(normal if normal is not None else (x, .25, z), dtype=float)
        normals.append(normal / max(np.linalg.norm(normal), 1e-9))
        ambient.append(ao)

    # Ramos em camadas, com pontas pendentes e agulhas individuais.
    for level in range(30):
        y = .38 + level * .105
        radius = 1.34 * (1 - (y - .3) / 3.5)
        for branch in range(11):
            angle = branch * math.tau / 11 + level * 1.87
            for _ in range(82):
                u = rng.uniform(.08, 1)
                a = angle + rng.normal(0, .08 + .14 * u)
                r = radius * u
                yy = y + .12 * np.sin(u * math.pi) - .14 * u**3 + rng.normal(0, .025)
                snow = rng.random() < .055
                c = WHITE if snow else tuple(np.array(GREEN) * rng.uniform(.85, 1.12))
                add(r * math.cos(a), yy, r * math.sin(a), c,
                    rng.choice(list('vxY*+;')) if not snow else '#', 1 + y * 1.45,
                    normal=(math.cos(a), .35 + .35*math.sin(u*math.pi), math.sin(a)),
                    ao=.40 + .60*u)

    # Tronco.
    for _ in range(650):
        a, y = rng.uniform(0, math.tau), rng.uniform(.02, .65)
        add(.09 * math.cos(a), y, .09 * math.sin(a), (124, 85, 55), ':', 1)

    # Festão dourado em espiral.
    for u in np.linspace(0, 1, 2400):
        y = .48 + 2.96 * u
        a = u * math.tau * 5.3
        r = 1.34 * (1 - (y - .3) / 3.5) + .025
        yy = y - .07 * abs(math.sin(a * 2.5))
        add(r * math.cos(a), yy, r * math.sin(a), GOLD, '=', 6.5 + u * .5, 1)

    # Bolas vermelhas e douradas distribuídas sobre os ramos.
    for j in range(38):
        y = rng.uniform(.55, 3.3)
        a = j * 2.39996
        r = 1.34 * (1 - (y - .3) / 3.5) + .025
        center = np.array([r * math.cos(a), y, r * math.sin(a)])
        size = rng.uniform(.043, .075)
        for _ in range(75):
            d = rng.normal(size=3)
            d /= np.linalg.norm(d)
            p = center + d * size
            add(*p, RED if j % 3 else GOLD, 'o', 7 + j / 60, 2, normal=d)

    # Pequenas lâmpadas, com fase de brilho independente.
    for j in range(175):
        y = rng.uniform(.45, 3.48)
        a = rng.uniform(0, math.tau)
        r = 1.34 * (1 - (y - .3) / 3.5) + .04
        add(r * math.cos(a), y, r * math.sin(a), WHITE if j % 4 == 0 else GOLD,
            '*', 7.5 + j / 175, 3)

    # Caixas tridimensionais com fitas cruzadas e laços.
    for j in range(7):
        a = j * math.tau / 7
        cx, cz = 1.28 * math.cos(a), 1.28 * math.sin(a)
        w, h, d = rng.uniform(.28, .46, 3)
        base = [RED, GREEN, WHITE, BLUE][j % 4]
        ribbon = GOLD if j % 2 == 0 else RED
        for _ in range(1900):
            p = rng.uniform(-.5, .5, 3) * [w, h, d]
            axis = rng.integers(0, 3)
            p[axis] = [w, h, d][axis] * rng.choice([-.5, .5])
            normal = np.zeros(3)
            normal[axis] = np.sign(p[axis])
            band = (abs(p[0]) < .032 or abs(p[2]) < .032) if axis == 1 else (
                abs(p[1]) < .025 or abs(p[2 if axis == 0 else 0]) < .032)
            add(cx + p[0], h / 2 + p[1], cz + p[2], ribbon if band else base,
                '#' if band else '+', 9 + j * .22, 4, normal=normal,
                ao=.72 + .28*(p[1]/h + .5))
        for u in np.linspace(0, math.tau, 160):
            add(cx + .12 * math.sin(u), h + .07 * abs(math.sin(2*u)),
                cz + .06 * math.sin(2*u), ribbon, '*', 9 + j * .22, 4)

    return (np.array(points), np.clip(colors, 0, 255).astype(float),
            np.array(symbols), np.array(births), np.array(kinds), np.array(normals), np.array(ambient))


class Animation:
    def __init__(self):
        self.p, self.colors, self.symbols, self.births, self.kinds, self.normals, self.ao = build_scene()
        rng = np.random.default_rng(12)
        self.snow = rng.random((580, 4))
        self.ground = rng.uniform([-3.7, 0, -3.2], [3.7, 0, 3.2], (9500, 3))

    @staticmethod
    def project(p, rotation):
        co, si = math.cos(rotation), math.sin(rotation)
        x = p[:, 0] * co + p[:, 2] * si
        z = -p[:, 0] * si + p[:, 2] * co
        depth = 7 + z
        scale = 7 / depth
        col = np.rint(COLS / 2 + x * 19 * scale).astype(int)
        row = np.rint(60 - (p[:, 1] * 13 - z * 2.7) * scale).astype(int)
        return col, row, depth

    def frame(self, t):
        chars = np.full((ROWS, COLS), ' ', dtype='<U1')
        rgb = np.zeros((ROWS, COLS, 3), dtype=np.uint8)
        rot = t * math.tau / 20

        def put(x, y, char, color):
            if 0 <= x < COLS and 0 <= y < ROWS:
                chars[y, x], rgb[y, x] = char, color

        gx, gy, gz = self.project(self.ground, 0)
        for i in range(len(gx)):
            if 39 <= gy[i] < ROWS:
                put(gx[i], gy[i], '.' if i % 3 else '-', (24, 48, 57))

        for i, (x, y, speed, phase) in enumerate(self.snow):
            xx = int((x * COLS + math.sin(t*.6 + phase*50)*1.4) % COLS)
            yy = int((y * ROWS + t*(.6 + speed*2.8)) % ROWS)
            brightness = .3 + .65 * (.5 + .5*math.sin(t*1.6 + phase*90))
            put(xx, yy, '+' if i % 4 == 0 else '.', np.array(WHITE)*brightness)

        x, y, depth = self.project(self.p, rot)
        valid = np.where((t >= self.births) & (x >= 0) & (x < COLS) & (y >= 0) & (y < ROWS))[0]
        # Ordenar do fundo para a frente preserva a oclusão das faces da árvore.
        valid = valid[np.argsort(-depth[valid])]
        # Normais acompanham a rotação; luz fixa acima e à esquerda da câmera.
        co, si = math.cos(rot), math.sin(rot)
        n = self.normals.copy()
        n[:, 0] = self.normals[:, 0]*co + self.normals[:, 2]*si
        n[:, 2] = -self.normals[:, 0]*si + self.normals[:, 2]*co
        light = np.array([-.75, .85, -.65])
        light /= np.linalg.norm(light)
        diffuse = np.maximum(n @ light, 0)
        # Preenchimento frio discreto no lado oposto e reflexo especular.
        fill = np.maximum(n @ np.array([.7, .2, .5]), 0)
        half = light + np.array([0, .2, -1])
        half /= np.linalg.norm(half)
        spec = np.maximum(n @ half, 0)**24
        glossy = np.isin(self.kinds, [1, 2, 4])
        shade = (.16 + 1.25*diffuse) * self.ao
        fade = np.clip((t - self.births)*2, 0, 1)
        pulse = .65 + .35 * np.sin(t*3 + np.arange(len(x))*1.71)**2
        color = self.colors * shade[:, None]
        color += fill[:, None] * np.array([5, 12, 24])
        color += (spec * glossy * 160)[:, None] * np.array([1., .91, .72])
        bulbs = self.kinds == 3
        color[bulbs] = self.colors[bulbs] * (1.15 + .65*pulse[bulbs, None])
        color = np.clip(color * fade[:, None], 0, 255).astype(np.uint8)
        # Um único ponto visível por célula; resolve as colisões em NumPy.
        reverse = valid[::-1]
        _, first = np.unique(y[reverse] * COLS + x[reverse], return_index=True)
        front = reverse[first]
        chars[y[front], x[front]] = self.symbols[front]
        rgb[y[front], x[front]] = color[front]

        if t >= 12:
            sx, sy, _ = self.project(np.array([[0, 3.74, 0]]), rot)
            sx, sy = int(sx[0]), int(sy[0])
            star = ['    +    ', '    #    ', '###+###', '  ###  ', ' ## ## ']
            for row, line in enumerate(star):
                for col, char in enumerate(line):
                    if char != ' ':
                        put(sx + col - len(line)//2, sy + row - 2, char, GOLD)
            for dy in range(-6, -2):
                put(sx, sy + dy, '|', (91, 77, 42))

        message = 'M E R R Y  C H R I S T M A S  2 0 2 6'
        count = min(len(message), max(0, int((t - 13)*9)))
        for i, char in enumerate(message[:count]):
            put((COLS-len(message))//2+i, 66, char, [RED, GOLD, GREEN][i % 3])
        return chars, rgb


def main():
    parser = argparse.ArgumentParser(description='Árvore de Natal ASCII animada em 3D')
    parser.add_argument('--capture', type=Path, help='Salva uma imagem e encerra, sem abrir janela')
    parser.add_argument('--time', type=float, default=18.9, help='Instante da captura em segundos')
    args = parser.parse_args()
    if args.capture:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 44))
    pygame.display.set_caption('ASCII Christmas Tree')
    font = pygame.font.SysFont('consolas,couriernew,monospace', 12)
    small = pygame.font.SysFont('consolas,couriernew,monospace', 11)
    scene = Animation()
    cache = {}
    clock = pygame.time.Clock()
    t, paused, running = 0., False, True

    def draw(seconds):
        chars, rgb = scene.frame(seconds)
        screen.fill(BG)
        blits = []
        for row, col in zip(*np.where(chars != ' ')):
            # Paleta quantizada mantém o cache pequeno sem perder o brilho.
            color = tuple((rgb[row, col] // 16 * 16).tolist())
            key = (str(chars[row, col]), color)
            if key not in cache:
                cache[key] = font.render(key[0], True, color)
            blits.append((cache[key], (int(col)*CW, int(row)*CH)))
        screen.blits(blits)
        # Bloom aditivo: espalha só os pixels luminosos, mantendo os glifos nítidos.
        pixels = pygame.surfarray.array3d(screen)
        energy = np.clip((pixels.astype(float) - 110)*1.8, 0, 255).astype(np.uint8)
        glow = pygame.surfarray.make_surface(energy)
        for divisor, strength in [(4, 1.0), (12, .8)]:
            reduced = pygame.transform.smoothscale(glow, (WIDTH//divisor, (HEIGHT+44)//divisor))
            blurred = pygame.transform.smoothscale(reduced, screen.get_size())
            blurred.fill((int(255*strength),)*3, special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(blurred, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(small.render(f't {seconds:05.2f}s', True, GOLD), (WIDTH-80, 8))
        screen.blit(small.render(f'rotation {seconds*18 % 360:06.2f}  |  ASCII 3D', True, (96,124,133)), (12, HEIGHT-20))
        pygame.draw.line(screen, (34, 47, 57), (0, HEIGHT), (WIDTH, HEIGHT))
        screen.blit(small.render('christmas_tree.py', True, WHITE), (12, HEIGHT+7))
        screen.blit(small.render('SPACE pausa   R reinicia   S captura   ESC sai', True, (133,153,164)), (12, HEIGHT+25))
        status = 'paused' if paused else ('capture' if args.capture else f'{clock.get_fps():.0f} fps')
        screen.blit(small.render(status, True, GOLD), (WIDTH-125, HEIGHT+7))
        pygame.display.flip()

    if args.capture:
        draw(args.time)
        pygame.image.save(screen, str(args.capture))
        print(f'Captura salva: {args.capture}')
    else:
        while running:
            dt = min(clock.tick(30)/1000, .1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_r:
                        t = 0
                    elif event.key == pygame.K_s:
                        target = Path(__file__).with_name('captura.png')
                        pygame.image.save(screen, str(target))
                        print(f'Captura salva: {target}')
            if not paused:
                t += dt
            draw(t)
    pygame.quit()


if __name__ == '__main__':
    main()
