"""Sunflower seeds: which turning angle packs the most seeds into the head?

Vogel's model: seed n sits at radius c * sqrt(n) and angle n * theta. The head (a circle)
and the seed size are fixed. For each theta we ask: how many seeds N fit without any two
overlapping? The pattern for N seeds is scaled so the outermost seed just touches the rim
(c = (1 - SEED / 2) / sqrt(N)); N fits if then every pair is at least SEED apart. The
sweep runs from 0 to 360 degrees in steps of 0.1 degree and slows down around the golden
angle, 137.508 degrees.

Render: manimgx render sunflower.py Sunflower -o sunflower.mp4
"""

import numpy as np

import manimgx as m

SEED = 0.04  # seed diameter, in rim radii
N_MAX = 2000  # most seeds tried; the golden angle fits 1540
STEP = 0.1  # degrees
FPS = 60
GOLDEN = 180 * (3 - np.sqrt(5))  # 137.507...

FLOWER_CENTER = np.array([-3.85, 0, 0])
FLOWER_RADIUS = 3.15  # the rim, in scene units

SEED_COLOR = m.ManimColor("#F2B233")
CORE_COLOR = m.ManimColor("#8A4B1F")

n = np.arange(1, N_MAX + 1)
UPPER = np.triu_indices(N_MAX)  # pairs (i, j) with j >= i, masked out


def unit_points(theta: float) -> np.ndarray:
    """Vogel's spiral with spacing 1, as complex numbers."""
    return np.sqrt(n) * np.exp(1j * n * np.radians(theta))


def seed_count(theta: float) -> int:
    """The most seeds that fit inside the rim without overlapping."""
    p = unit_points(theta)
    d = np.abs(p[:, None] - p[None, :])
    d[UPPER] = np.inf
    # closest pair among the first N seeds, for every N
    closest = np.minimum.accumulate(d.min(axis=1))
    fits = (1 - SEED / 2) / np.sqrt(n) * closest >= SEED
    return int(n[fits].max()) if fits.any() else 1


# the 0.1 degree grid plus the exact golden angle and its mirror 360 - golden, which the
# grid misses by 0.008
GRID = np.round(np.arange(0, 3601) * STEP, 1)
ANGLES = np.sort(np.append(GRID, [GOLDEN, 360 - GOLDEN]))
GOLDEN_STEP = int(np.searchsorted(ANGLES, GOLDEN))
# ponytail: brute force over all 2000^2 distances per angle; cache to .npy if it gets slow
COUNTS = np.array([seed_count(t) for t in ANGLES])
TOP = int(COUNTS.max())


class Sunflower(m.Scene):
    def build(self) -> m.ValueTracker:
        """Flower, graph and readout, all driven by the returned index into ANGLES."""
        index = m.ValueTracker(0.0)  # position in ANGLES, one per frame at full speed

        def step() -> int:
            return int(round(index.get_value()))

        # the flower: only the seeds that fit, the outermost touching the rim
        seed_rgba = np.array(SEED_COLOR.to_rgba())
        core_rgba = np.array(CORE_COLOR.to_rgba())
        flower = m.PMobject()

        def draw_flower(cloud: m.PMobject) -> None:
            k = step()
            count = COUNTS[k]
            p = unit_points(ANGLES[k])[:count] * (1 - SEED / 2) / np.sqrt(count)
            p *= FLOWER_RADIUS
            mix = np.sqrt(n[:count] / count)[:, None]
            cloud.points = np.column_stack([p.real, p.imag, 0 * p.real]) + FLOWER_CENTER
            cloud.paint = cloud.paint.but(
                fill=(1 - mix) * core_rgba + mix * seed_rgba,
                stroke_width=90 * SEED * FLOWER_RADIUS,  # 100 would touch; a gap shows
            )

        flower.add_updater(draw_flower)
        draw_flower(flower)
        rim = m.Circle(
            radius=FLOWER_RADIUS, stroke_color=SEED_COLOR, stroke_width=3
        ).move_to(FLOWER_CENTER)

        # the graph
        axes = m.Axes(
            x_range=[0, 360, 45],
            y_range=[0, 1600, 400],
            x_length=5.6,
            y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 22, "color": m.GREY_B},
            tips=False,
        ).move_to([3.6, -0.75, 0])
        x_label = m.Text("angle in degrees", font_size=22, color=m.GREY_B).next_to(
            axes.x_axis, m.DOWN, buff=0.5
        )
        y_label = (
            m.Text("seeds that fit", font_size=22, color=m.GREY_B)
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

        self.axes = axes
        self.parts = m.Group(flower, rim, axes, x_label, y_label, readout, curve, marker)
        return index

    def construct(self) -> None:
        index = self.build()
        axes = self.axes

        def step() -> int:
            return int(round(index.get_value()))

        question = m.VGroup(
            m.Text("What's the best angle to fit", font_size=56),
            m.Text("the most seeds into a sunflower?", font_size=56),
        ).arrange(m.DOWN, buff=0.25)
        answer = m.Text("Nature figured it out.", font_size=36, color=m.GREY_B)
        m.VGroup(question, answer).arrange(m.DOWN, buff=0.7).center()
        self.play(m.Write(question), run_time=1.5)
        self.play(m.FadeIn(answer), run_time=0.6)
        self.wait(2.5)
        self.play(m.FadeOut(question, answer), run_time=0.8)

        self.play(m.FadeIn(self.parts), run_time=1.5)
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
        top = axes.c2p(GOLDEN, TOP)
        guide = m.DashedLine(axes.c2p(GOLDEN, 0), top, color=m.WHITE, stroke_width=1.5)
        note = m.Text("golden angle", font_size=26).next_to(top, m.UP, buff=0.15)
        self.play(m.Create(guide), m.FadeIn(note), run_time=0.8)
        self.wait(2.5)

        sweep(GOLDEN_STEP + 15, 6)
        sweep(len(ANGLES) - 1)
        self.wait(2)


class Preview(Sunflower):
    """Stills for checking: 130 degrees, then 137.5 degrees, half a second each."""

    def construct(self) -> None:
        index = self.build()
        self.add(self.parts)
        for theta in (130.0, 137.5):
            target = int(np.searchsorted(ANGLES, theta))
            self.play(index.animate.set_value(target), run_time=1 / FPS)
            self.wait(0.5)


if __name__ == "__main__":
    for theta, expected in ((GOLDEN, 1540), (137.5, 1440), (130.0, 450), (90.0, 50)):
        assert seed_count(theta) == expected, (theta, seed_count(theta))
    assert TOP == 1540, TOP
    print("ok")
