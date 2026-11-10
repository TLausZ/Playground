"""Sunflower seeds: which turning angle packs the most seeds?

Vogel's model: seed n sits at radius sqrt(n) and angle n * theta. Every seed has the
same diameter. Seeds are placed from the center outwards until the first one overlaps
another; the count up to there is the score for theta. The sweep runs from 0 to 360
degrees in steps of 0.1 degree and slows down around the golden angle, 137.508 degrees.

Render: manimgx render sunflower.py Sunflower -o sunflower.mp4
"""

import numpy as np

import manimgx as m

N = 1500  # seeds in the full disk, the ceiling of the score
SEED = 1.6  # seed diameter in model units; at 1.5 the angle 99.5 also fills the disk
STEP = 0.1  # degrees
FPS = 60
GOLDEN = 180 * (3 - np.sqrt(5))  # 137.507...

FLOWER_CENTER = np.array([-3.85, 0, 0])
FLOWER_RADIUS = 3.15
SCALE = FLOWER_RADIUS / np.sqrt(N)

SEED_COLOR = m.ManimColor("#F2B233")
CORE_COLOR = m.ManimColor("#8A4B1F")
DEAD_COLOR = m.ManimColor("#3A3A3A")

n = np.arange(1, N + 1)
radius = np.sqrt(n)
I, J = np.triu_indices(N, 1)  # every pair once, J > I


def positions(theta: float) -> tuple[np.ndarray, np.ndarray]:
    a = n * np.radians(theta)
    return radius * np.cos(a), radius * np.sin(a)


def seed_count(theta: float) -> int:
    """Seeds placed before the first overlap: the smallest J of any touching pair."""
    x, y = positions(theta)
    close = (x[I] - x[J]) ** 2 + (y[I] - y[J]) ** 2 < SEED**2
    return int(J[close].min()) if close.any() else N


# the 0.1 degree grid plus the exact golden angle and its mirror 360 - golden, which the
# grid misses by 0.008
GRID = np.round(np.arange(0, 3601) * STEP, 1)
ANGLES = np.sort(np.append(GRID, [GOLDEN, 360 - GOLDEN]))
GOLDEN_STEP = int(np.searchsorted(ANGLES, GOLDEN))
# ponytail: brute force over all ~1.1M pairs per angle, about 12 s for the sweep
COUNTS = np.array([seed_count(t) for t in ANGLES])


class Sunflower(m.Scene):
    def construct(self) -> None:
        index = m.ValueTracker(0.0)  # position in ANGLES, one per frame at full speed

        def step() -> int:
            return int(round(index.get_value()))

        # the flower
        seed_rgba = np.array(SEED_COLOR.to_rgba())
        core_rgba = np.array(CORE_COLOR.to_rgba())
        dead_rgba = np.array(DEAD_COLOR.to_rgba())
        mix = (n / N)[:, None] ** 0.5
        alive_rgba = (1 - mix) * core_rgba + mix * seed_rgba
        flower = m.PMobject()

        def draw_flower(cloud: m.PMobject) -> None:
            k = step()
            x, y = positions(ANGLES[k])
            pts = np.column_stack([x, y, 0 * x]) * SCALE + FLOWER_CENTER
            rgba = alive_rgba.copy()
            rgba[COUNTS[k] :] = dead_rgba
            cloud.points = pts
            cloud.paint = cloud.paint.but(fill=rgba, stroke_width=88 * SEED * SCALE)

        flower.add_updater(draw_flower)
        draw_flower(flower)

        # the graph
        axes = m.Axes(
            x_range=[0, 360, 45],
            y_range=[0, N, 500],
            x_length=5.6,
            y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 22, "color": m.GREY_B},
            tips=False,
        ).move_to([3.6, -0.75, 0])
        x_label = m.Text("angle in degrees", font_size=22, color=m.GREY_B).next_to(
            axes.x_axis, m.DOWN, buff=0.5
        )
        y_label = (
            m.Text("seeds until first overlap", font_size=22, color=m.GREY_B)
            .rotate(90 * m.DEGREES)
            .next_to(axes.y_axis, m.LEFT, buff=0.55)
        )
        curve = m.VMobject(stroke_color=SEED_COLOR, stroke_width=2)

        def draw_curve(line: m.VMobject) -> None:
            k = max(step(), 1)
            line.set_points_as_corners(axes.c2p(ANGLES[: k + 1], COUNTS[: k + 1]).T)

        curve.add_updater(draw_curve)
        draw_curve(curve)
        marker = m.Dot(radius=0.06, color=m.WHITE)
        marker.add_updater(lambda d: d.move_to(axes.c2p(ANGLES[step()], COUNTS[step()])))

        # the readout
        angle_value = m.DecimalNumber(0, num_decimal_places=3, font_size=48, unit=r"^\circ")
        angle_value.add_updater(lambda d: d.set_value(ANGLES[step()]))
        count_value = m.Integer(COUNTS[0], font_size=48, color=SEED_COLOR)
        count_value.add_updater(lambda d: d.set_value(COUNTS[step()]))
        readout = m.VGroup(
            m.VGroup(m.Text("angle", font_size=30, color=m.GREY_B), angle_value).arrange(
                m.RIGHT, buff=0.3
            ),
            m.VGroup(m.Text("seeds", font_size=30, color=m.GREY_B), count_value).arrange(
                m.RIGHT, buff=0.3
            ),
        ).arrange(m.RIGHT, buff=0.7)
        readout.to_edge(m.UP, buff=0.7)
        readout.set_x(axes.get_center()[0])

        self.play(
            m.FadeIn(flower),
            m.Create(axes),
            m.FadeIn(x_label, y_label, readout, curve, marker),
            run_time=1.5,
        )
        self.wait(0.5)

        def sweep(to: int, seconds: float | None = None) -> None:
            frames = to - step()
            self.play(
                index.animate.set_value(to),
                run_time=seconds or frames / FPS,
                rate_func=m.linear,
            )

        sweep(GOLDEN_STEP - 15)
        sweep(GOLDEN_STEP, 6)  # slow: 15 steps over 6 s

        # the golden angle
        top = axes.c2p(GOLDEN, N)
        guide = m.DashedLine(axes.c2p(GOLDEN, 0), top, color=m.WHITE, stroke_width=1.5)
        note = m.Text("golden angle", font_size=26).next_to(top, m.UP, buff=0.15)
        self.play(m.Create(guide), m.FadeIn(note), run_time=0.8)
        self.wait(2.5)

        sweep(GOLDEN_STEP + 15, 6)
        sweep(len(ANGLES) - 1)
        self.wait(2)


if __name__ == "__main__":
    for theta, expected in ((GOLDEN, N), (137.5, 465), (99.5, 4), (90.0, 4)):
        assert seed_count(theta) == expected, (theta, seed_count(theta))
    print("ok")
