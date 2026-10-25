"""ManimGL proof of concept for the precedence-constrained search paper.

Every numerical picture in the animation is either derived from the paper or
explicitly marked as a toy instance.  Mathematical notation is rendered by
LaTeX through ManimGL's Tex mobject.
"""

from pathlib import Path
import re
import random
import wave

import numpy as np
from manimlib import *

ROOT = Path(__file__).resolve().parents[1]
VOICE = ROOT / "output" / "voiceover"
SCRIPT = ROOT / "script" / "voiceover.txt"


def prose(text, size=25, color=WHITE):
    return Text(text, font_size=size, color=color)


def formula(tex, size=40, color=WHITE):
    obj = Tex(tex, font_size=size, color=color)
    if obj.get_width() > 13.0:
        obj.set_width(13.0)
    return obj


def colored_dot(point, radius, color):
    """A filled Dot; ManimGL's `color` alone only colored its outline here."""
    return Dot(point, radius=radius, color=color, fill_color=color,
               fill_opacity=1, stroke_color=color, stroke_width=0)


class ArticleVideo(Scene):
    """Ten narrated chapters, with proof objects built in view."""

    TITLES = [
        "Search under precedence constraints",
        "Worst case and average case",
        "Why a useful test can be unavailable",
        "Sepcover: remove a path, inspect every component",
        "The recursive shrinkage argument",
        "Coverage time and the min-sum objective",
        "Algorithms for general orders and forests",
        "PDS: encode planted cliques as witnesses",
        "Label Cover: bundles, witnesses, and soundness",
        "The reduction framework",
    ]
    # Script timing targets.  When a chapter WAV exists, its duration replaces
    # this target and its audio is placed under the complete visual sequence.
    ESTIMATED_SECONDS = [100, 100, 110, 150, 150, 170, 120, 150, 150, 90]

    def construct(self):
        chapters = [
            self.chapter_search,
            self.chapter_costs,
            self.chapter_precedence,
            self.chapter_sepcover,
            self.chapter_recursion,
            self.chapter_minsum,
            self.chapter_approximation,
            self.chapter_pds,
            self.chapter_label_cover,
            self.chapter_summary,
        ]
        for index, (title, chapter) in enumerate(zip(self.TITLES, chapters), 1):
            self.chapter_header(index, title)
            chapter()
            self.chapter_audio_hold(index)
            self.clear()

    def chapter_header(self, index, title):
        heading = prose(f"{index:02d}   {title}", 31, YELLOW).to_edge(UP, buff=0.28)
        rule = Line(LEFT * 6.8 + UP * 2.78, RIGHT * 6.8 + UP * 2.78, color=GREY_B, stroke_width=1.5)
        self.play(Write(heading), ShowCreation(rule), run_time=0.8)

    def chapter_audio_hold(self, index):
        path = VOICE / f"chapter_{index:02d}.wav"
        target = self.ESTIMATED_SECONDS[index - 1]
        if path.exists():
            with wave.open(str(path), "rb") as wav:
                target = wav.getnframes() / wav.getframerate()
            self.add_sound(str(path))
        narration = self.read_chapter_script(index)
        chunks = self.caption_chunks(narration)
        if not chunks:
            self.wait(target)
            return
        total_words = sum(len(c.split()) for c in chunks)
        # A moving proof caption advances the story in the silent POC as well;
        # with a WAV present these same captions follow its chapter timing.
        for chunk in chunks:
            seconds = target * len(chunk.split()) / total_words
            caption = Text(chunk, font_size=21, color=WHITE)
            if caption.get_width() > 12.2:
                caption.set_width(12.2)
            caption.to_edge(DOWN, buff=0.28)
            back = SurroundingRectangle(caption, buff=0.18, color=BLACK, fill_color=BLACK,
                                        fill_opacity=0.88, stroke_opacity=0)
            fade = min(0.18, seconds / 4)
            self.play(FadeIn(back), FadeIn(caption), run_time=fade)
            self.wait(max(0, seconds - 2 * fade))
            self.play(FadeOut(back), FadeOut(caption), run_time=fade)

    @staticmethod
    def read_chapter_script(index):
        if not SCRIPT.exists():
            return ""
        current = None
        bodies = {}
        for line in SCRIPT.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"CHAPTER\s+(\d+)", line.strip(), flags=re.IGNORECASE)
            if match:
                current = int(match.group(1))
                bodies[current] = []
            elif current is not None and line.strip():
                bodies[current].append(line.strip())
        return " ".join(bodies.get(index, []))

    @staticmethod
    def caption_chunks(text, max_words=16):
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        chunks = []
        for sentence in sentences:
            words = sentence.split()
            while words:
                chunks.append(" ".join(words[:max_words]))
                words = words[max_words:]
        return chunks

    def footer(self, text, color=GREY_A):
        # Explanatory prose is carried by the synchronized narration captions.
        # A second fixed footer would compete with both captions and equations.
        return None

    def swap(self, old, new, run_time=0.65):
        self.play(FadeOut(old), FadeIn(new), run_time=run_time)

    @staticmethod
    def test_node(name, center, color=TEAL_B, radius=0.34):
        circle = Circle(radius=radius, color=color, stroke_width=3).move_to(center)
        tag = formula(rf"{name}", 25, WHITE).move_to(circle)
        return VGroup(circle, tag)

    @staticmethod
    def small_hypotheses(count, start, columns=6, color=BLUE_B):
        dots = VGroup()
        labels = VGroup()
        for i in range(count):
            p = start + RIGHT * ((i % columns) * 0.62) + DOWN * ((i // columns) * 0.62)
            dots.add(colored_dot(p, 0.10, color))
            labels.add(formula(rf"h_{{{i+1}}}", 17).next_to(dots[-1], DOWN, buff=0.04))
        return dots, labels

    def chapter_search(self):
        # Three distinct tests on the same 12-hypothesis universe.  Each row is
        # an exact partition; these are alternatives, not successive outcomes.
        heading = formula(r"\mathcal H=\{h_1,\ldots,h_{12}\}\qquad\text{three possible tests}", 31, BLUE_B).shift(UP * 2.1)
        rows = [("t_A", [6, 6], "6 + 6   (balanced, 2 replies)"),
                ("t_B", [9, 3], "9 + 3   (uneven, 2 replies)"),
                ("t_C", [4, 4, 4], "4 + 4 + 4   (balanced, 3 replies)")]
        row_groups = VGroup()
        for row_i, (name, sizes, desc) in enumerate(rows):
            y = 1.2 - row_i * 1.18
            tag = self.test_node(name, LEFT * 5.2 + UP * y, radius=0.27)
            dots = VGroup()
            colors = [TEAL_B, GOLD, PURPLE_B]
            x0 = -3.45
            for group_i, size in enumerate(sizes):
                # Pack each reply into a clearly bounded run of tokens.
                for j in range(size):
                    px = x0 + (j + 0.5) * 0.32
                    dots.add(colored_dot(RIGHT * px + UP * y, 0.095, colors[group_i]))
                x0 += size * 0.32 + 0.23
            split = prose(desc, 19, WHITE).move_to(RIGHT * 3.65 + UP * y)
            row_groups.add(VGroup(tag, dots, split))
        legend = VGroup(
            colored_dot(LEFT * 1.4 + DOWN * 2.45, 0.09, TEAL_B),
            prose("reply 1", 18, GREY_A).next_to(LEFT * 1.4 + DOWN * 2.45, RIGHT, buff=0.12),
            colored_dot(RIGHT * 0.2 + DOWN * 2.45, 0.09, GOLD),
            prose("reply 2", 18, GREY_A).next_to(RIGHT * 0.2 + DOWN * 2.45, RIGHT, buff=0.12),
            colored_dot(RIGHT * 1.9 + DOWN * 2.45, 0.09, PURPLE_B),
            prose("reply 3", 18, GREY_A).next_to(RIGHT * 1.9 + DOWN * 2.45, RIGHT, buff=0.12))
        note = prose("Each row is one alternative test on the same hypothesis pool.", 20, GREY_A).shift(DOWN * 2.95)
        self.play(Write(heading), run_time=0.55)
        for row in row_groups:
            self.play(FadeIn(row[0]), LaggedStart(*[FadeIn(x) for x in row[1]], lag_ratio=0.025), Write(row[2]), run_time=0.85)
        self.play(FadeIn(legend), Write(note), run_time=0.55)
        self.wait(3)

    def chapter_costs(self):
        # A nonuniform binary strategy tree with eight outcomes.  Its leaf
        # depths are [2,3,3,3,3,3,4,4], giving max=4 and sum=25.
        leaf_x = np.linspace(-5.6, 5.6, 8)
        leaf_pos = [RIGHT * xx + DOWN * 2.0 for xx in leaf_x]
        # Internal nodes are positioned over the leaves in their descendant interval.
        pos = {
            "r": (leaf_pos[0] + leaf_pos[7]) / 2 + UP * 3.95,
            "A": (leaf_pos[0] + leaf_pos[2]) / 2 + UP * 3.0,
            "B": (leaf_pos[3] + leaf_pos[7]) / 2 + UP * 3.0,
            "A2": (leaf_pos[1] + leaf_pos[2]) / 2 + UP * 1.9,
            "B1": (leaf_pos[3] + leaf_pos[4]) / 2 + UP * 1.9,
            "B2": (leaf_pos[5] + leaf_pos[7]) / 2 + UP * 1.9,
            "B21": (leaf_pos[6] + leaf_pos[7]) / 2 + UP * 0.95,
        }
        child_edges = [("r", "A"), ("r", "B"), ("A", "h1"), ("A", "A2"), ("A2", "h2"), ("A2", "h3"),
                       ("B", "B1"), ("B", "B2"), ("B1", "h4"), ("B1", "h5"), ("B2", "h6"),
                       ("B2", "B21"), ("B21", "h7"), ("B21", "h8")]
        def endpoint(key):
            if key == "h1": return leaf_pos[0]
            if key in ("h2", "h3"): return leaf_pos[int(key[1])-1]
            if key in ("h4", "h5", "h6", "h7", "h8"): return leaf_pos[int(key[1])-1]
            return pos[key]
        edges = VGroup(*[Line(endpoint(a), endpoint(b), color=GREY_B, stroke_width=2.0)
                         for a, b in child_edges])
        nodes = VGroup(*[colored_dot(p, 0.075, TEAL_B) for p in pos.values()])
        leaves = VGroup(*[colored_dot(p, 0.055, GOLD) for p in leaf_pos])
        leaf_labels = VGroup(*[formula(rf"h_{i+1}", 16, GOLD).next_to(p, DOWN, buff=0.07) for i, p in enumerate(leaf_pos)])
        max_formula = formula(r"\mathrm{cost}_{\max}(D)=\max_h d_D(h)=\max\{2,3,3,3,3,3,4,4\}=4", 28, ORANGE).shift(DOWN * 2.3)
        sum_formula = formula(r"\mathrm{cost}_{\mathrm{sum}}(D)=\sum_h d_D(h)=2+3+3+3+3+3+4+4=25", 27, TEAL_B).shift(DOWN * 2.3)
        self.play(ShowCreation(edges), FadeIn(nodes), FadeIn(leaves), Write(leaf_labels), run_time=1.3)
        long_path = VGroup(*[Line(a, b, color=ORANGE, stroke_width=5) for a, b in [
            (pos["r"], pos["B"]), (pos["B"], pos["B2"]), (pos["B2"], pos["B21"]), (pos["B21"], leaf_pos[6])]])
        self.play(ShowCreation(long_path), run_time=0.7)
        self.wait(4)
        self.play(FadeOut(edges), FadeOut(nodes), FadeOut(leaves), FadeOut(leaf_labels), FadeOut(long_path), run_time=0.45)
        self.play(Write(max_formula), run_time=0.7)
        self.wait(2)
        self.play(Transform(max_formula, sum_formula), run_time=0.7)
        self.wait(3)
        self.footer("These are the two paper objectives; uniform average cost is this sum divided by |H|.")

    def chapter_precedence(self):
        centers = {"t_1": LEFT * 4.8 + UP * 1.1, "t_2": LEFT * 4.8 + DOWN * 0.25,
                   "t_3": LEFT * 1.8 + UP * 0.2, "t_4": LEFT * 1.4 + UP * 1.45,
                   "t_5": RIGHT * 1.55 + DOWN * 0.15, "t_6": RIGHT * 4.55 + UP * 0.65}
        relations = [("t_1", "t_3"), ("t_2", "t_3"), ("t_1", "t_4"), ("t_2", "t_4"),
                     ("t_3", "t_5"), ("t_4", "t_6"), ("t_5", "t_6")]
        deps = VGroup(*[Arrow(centers[a], centers[b], color=YELLOW, buff=0.38, stroke_width=2.7)
                        for a, b in relations])
        nodes = VGroup(*[self.test_node(k, v, radius=0.31) for k, v in centers.items()])
        self.play(ShowCreation(deps), FadeIn(nodes), run_time=1.15)
        self.play(Indicate(VGroup(nodes[0], nodes[1], nodes[2], nodes[3]), color=YELLOW), run_time=0.6)
        self.wait(4)
        self.play(FadeOut(deps), FadeOut(nodes), run_time=0.45)
        constraints = formula(r"t_1,t_2\prec t_3,t_4;\qquad t_3\prec t_5;\qquad t_4,t_5\prec t_6", 27, YELLOW).shift(UP * 1.35)
        valid1 = formula(r"(t_1,t_2,t_3,t_4,t_5,t_6)\quad\checkmark", 29, TEAL_B).shift(UP * 0.25)
        valid2 = formula(r"(t_2,t_1,t_4,t_3,t_5,t_6)\quad\checkmark", 29, TEAL_B).shift(DOWN * 0.65)
        invalid = formula(r"(t_3,t_1,t_2,t_4,t_5,t_6)\quad\times\quad t_3\text{ is premature}", 27, RED).shift(DOWN * 1.65)
        self.play(Write(constraints), run_time=0.65)
        self.play(Write(valid1), run_time=0.6)
        self.play(Write(valid2), run_time=0.6)
        self.play(Write(invalid), run_time=0.65)
        self.wait(3)

    def sep_tree(self):
        # A contracted tree with 16 leaves. Subtree badges state exact leaf counts.
        r = UP * 1.65
        a, b = LEFT * 2.35 + UP * 0.4, RIGHT * 2.35 + UP * 0.4
        a1, a2 = LEFT * 3.4 + DOWN * 0.5, LEFT * 1.3 + DOWN * 0.5
        b1, b2 = RIGHT * 1.3 + DOWN * 0.5, RIGHT * 3.4 + DOWN * 0.5
        vertices = {"r": r, "a": a, "b": b, "u": a1, "v": a2, "w": b1, "z": b2}
        edges = VGroup(*[Line(vertices[x], vertices[y], color=GREY_B, stroke_width=2.5)
                         for x, y in [("r", "a"), ("r", "b"), ("a", "u"), ("a", "v"), ("b", "w"), ("b", "z")]])
        nodes = VGroup(*[self.test_node(rf"{k}", p, color=YELLOW if k in ("r", "a") else TEAL_B, radius=0.27)
                         for k, p in vertices.items()])
        badges = VGroup()
        for name, p, count, col in [("A", a + LEFT * 1.0, 12, ORANGE),
                                     ("B", b + RIGHT * 1.0, 4, TEAL_B),
                                     ("A_1", a1 + DOWN * 0.72, 8, TEAL_B),
                                     ("A_2", a2 + DOWN * 0.72, 4, TEAL_B),
                                     ("B_1", b1 + DOWN * 0.72, 2, TEAL_B),
                                     ("B_2", b2 + DOWN * 0.72, 2, TEAL_B)]:
            badges.add(formula(rf"{name}:\ {count}", 18, col).move_to(p))
        return vertices, edges, nodes, badges

    def chapter_sepcover(self):
        vertices, edges, nodes, badges = self.sep_tree()
        caption = prose("Contracted view: badges give exact leaf counts for each displayed subtree.", 20, GREY_A).shift(DOWN * 2.1)
        path = VGroup(Line(vertices["r"], vertices["a"], color=YELLOW, stroke_width=7))
        self.play(ShowCreation(edges), FadeIn(nodes), Write(badges), run_time=1.3)
        self.play(ShowCreation(path), Write(caption), Indicate(badges[0], color=ORANGE), run_time=0.8)
        self.wait(5)
        self.clear()
        self.chapter_header(4, self.TITLES[3])
        definition = formula(r"\mathrm{Sepcover}(D)=\mathrm{tests}(D,v)", 31, YELLOW).shift(UP * 1.85)
        total = formula(r"|\mathcal H|=16\quad\Longrightarrow\quad |\mathcal H|/2=8", 30).shift(UP * 0.85)
        fail = formula(r"\text{Remove root }r:\quad(12,4)\quad 12>8\quad\text{fails}", 29, ORANGE).shift(DOWN * 0.15)
        success = formula(r"\text{Remove path }(r,a):\quad(8,4,4)\quad\max=8\quad\checkmark", 28, TEAL_B).shift(DOWN * 1.2)
        note = prose("Closest-to-root node meeting the half-size condition is a.", 22, GREY_A).shift(DOWN * 2.15)
        self.play(Write(definition), Write(total), run_time=0.8)
        self.play(Write(fail), run_time=0.7)
        self.play(Write(success), run_time=0.7)
        self.play(Write(note), run_time=0.55)
        self.wait(4)
        self.clear()
        self.chapter_header(4, self.TITLES[3])
        heading = formula(r"\xi(t):\ \text{a reply qualifies when }|R|\leq\tfrac34|\mathcal H|", 27, YELLOW).shift(UP * 2.1)
        total = formula(r"|\mathcal H|=12\qquad\text{so threshold}=9", 29).shift(UP * 1.35)
        rows = [("t_A", "6 + 6", [6, 6]), ("t_B", "9 + 3", [9, 3]), ("t_C", "4 + 4 + 4", [4, 4, 4])]
        row_objs = VGroup()
        for i, (name, expression, sizes) in enumerate(rows):
            y = 0.65 - i * 0.85
            tag = formula(rf"{name}", 24, TEAL_B).move_to(LEFT * 4.6 + UP * y)
            partition = prose(expression, 22, WHITE).move_to(LEFT * 1.8 + UP * y)
            result = formula(r"\xi(t)=\mathcal H", 23, YELLOW).move_to(RIGHT * 3.2 + UP * y)
            row_objs.add(VGroup(tag, partition, result))
        self.play(Write(heading), Write(total), run_time=0.7)
        for row in row_objs:
            self.play(Write(row[0]), Write(row[1]), Write(row[2]), run_time=0.65)
        self.wait(3)
        self.footer("The paper's xi(t) definition is applied to each reply of a test, using the original hypothesis count.")

    def chapter_recursion(self):
        # Display the article's stated child-size bound and iterate the inequality.
        eq0 = formula(r"n_{i+1}\leq\frac{5\beta-1}{5\beta}\,n_i", 43, YELLOW).shift(UP * 1.55)
        eq1 = formula(r"=\left(1-\frac{1}{5\beta}\right)n_i", 37, WHITE).next_to(eq0, DOWN, buff=0.35)
        eq2 = formula(r"n_i\leq\left(1-\frac{1}{5\beta}\right)^i n_0", 37, TEAL_B).next_to(eq1, DOWN, buff=0.4)
        self.play(Write(eq0), run_time=0.8)
        self.play(Write(eq1), run_time=0.6)
        self.play(Write(eq2), run_time=0.7)
        self.wait(3)
        self.play(FadeOut(eq0), FadeOut(eq1), FadeOut(eq2), run_time=0.4)
        beta_note = formula(r"\text{Example }\beta=1:\quad n_{i+1}\leq\frac45 n_i", 30, YELLOW).shift(UP * 1.45)
        self.play(Write(beta_note), run_time=0.6)
        self.wait(2)
        bars = VGroup()
        beta = 1
        shrink = 1 - 1 / (5 * beta)
        values = [shrink ** i for i in range(6)]
        for i, v in enumerate(values):
            bar = Rectangle(width=5.8 * v, height=0.28, color=TEAL_B, fill_opacity=0.68)
            bar.move_to(LEFT * (2.9 - 2.9 * v) + UP * (0.5 - 0.43 * i))
            bars.add(bar)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in bars], lag_ratio=0.1), run_time=1.5)
        complexity = formula(r"i=O(\beta\log n_0)\quad\Longrightarrow\quad n_i<1", 31, YELLOW).shift(DOWN * 2.35)
        self.play(Write(complexity), run_time=0.7)
        self.wait(4)
        self.footer("Each sufficiently small reply becomes a recursive subproblem; a larger one follows the selected cover sequence.")

    def chapter_minsum(self):
        # A small incidence table makes every set-element membership explicit.
        elems = ["a", "b", "c", "d", "e", "f"]
        rows = [(r"S_1", {"a", "b", "c"}), (r"S_2", {"c", "d"}), (r"S_3", {"e", "f"})]
        xs = np.linspace(-3.3, 4.2, 6)
        headers = VGroup(*[formula(rf"{e}", 22, GOLD).move_to(RIGHT * x + UP * 1.25) for e, x in zip(elems, xs)])
        row_labels = VGroup(*[formula(name, 24, TEAL_B).move_to(LEFT * 4.6 + UP * (0.6 - i * 0.65))
                              for i, (name, _) in enumerate(rows)])
        cells = VGroup()
        for row_i, (_, members) in enumerate(rows):
            for e, x in zip(elems, xs):
                y = 0.6 - row_i * 0.65
                cell_color = TEAL_B if e in members else GREY_D
                cell_fill = TEAL_B if e in members else BLACK
                cell = RoundedRectangle(width=0.72, height=0.46, corner_radius=0.04,
                                        color=cell_color, fill_color=cell_fill,
                                        fill_opacity=0.55 if e in members else 0.08)
                cell.move_to(RIGHT * x + UP * y)
                if e in members:
                    cell.add(formula(r"\checkmark", 19, TEAL_B).move_to(cell))
                cells.add(cell)
        seq = formula(r"\mathcal C=(S_1,S_2,S_3),\qquad S_1\prec S_3", 28, YELLOW).shift(UP * 2.05)
        self.play(Write(seq), Write(headers), run_time=0.8)
        self.play(Write(row_labels), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.035), run_time=1.0)
        time_eq = formula(r"(\tau(a),\tau(b),\tau(c),\tau(d),\tau(e),\tau(f))=(1,1,1,2,3,3)", 27, WHITE).shift(DOWN * 1.55)
        sum_eq = formula(r"\sum_{u\in\mathcal U}\tau(u)=1+1+1+2+3+3=11", 31, TEAL_B).shift(DOWN * 2.25)
        self.play(Write(time_eq), run_time=0.7)
        self.play(Write(sum_eq), run_time=0.7)
        self.wait(4)
        self.footer("Toy instance. An uncovered item is assigned time |C|; here every item is covered.")

    def chapter_approximation(self):
        # Reduction and theorem values are transcribed from the article.
        stages = [
            (r"\text{Decision tree}", r"\downarrow\;\text{build a separated-hypothesis universe}"),
            (r"\text{PCSC / PCMSSC}", r"\downarrow\;\text{precedence-closed cover sequence}"),
            (r"\text{Partial Red--Blue Set Cover}", r"\alpha_{m,n}=O(m^{1/3}\log^{4/3}m\log n)"),
        ]
        ys = [1.6, 0.55, -0.55]
        boxes, inside = VGroup(), VGroup()
        for (name, _), y in zip(stages, ys):
            box = RoundedRectangle(width=6.5, height=0.67, corner_radius=0.12, color=TEAL_B, stroke_width=2.2).move_to(UP * y)
            boxes.add(box)
            inside.add(formula(name, 27).move_to(box))
        arrows = VGroup(Arrow(boxes[0].get_bottom(), boxes[1].get_top(), color=YELLOW, buff=0.06),
                        Arrow(boxes[1].get_bottom(), boxes[2].get_top(), color=YELLOW, buff=0.06))
        ratio = formula(stages[-1][1], 27, YELLOW).shift(DOWN * 1.25)
        general = formula(r"O(m^{1/3}\log^{4/3}m\log^2 n)\quad\text{for decision trees}", 25, WHITE).shift(DOWN * 1.9)
        forests = formula(r"\text{inforest: }O(\log n)\qquad\text{outforest: }O(\log^2 n)", 28, TEAL_B).shift(DOWN * 2.55)
        self.play(FadeIn(boxes), Write(inside), ShowCreation(arrows), run_time=1.1)
        self.play(Write(ratio), run_time=0.7)
        self.play(Write(general), run_time=0.7)
        self.play(Write(forests), run_time=0.7)
        self.wait(4)
        self.footer("The forest bounds use maximum coverage for inforests and group Steiner orienteering for outforests.")

    def pds_graph(self, planted=False):
        # One reproducible draw from the stated two-density model, not a hand-
        # chosen clique.  The irregularized lattice is just a readable layout.
        seed = 20261014
        rng = random.Random(seed)
        N, k = 36, 6
        alpha, beta = 0.5, 0.25
        p_out = N ** (alpha - 1)
        p_in = k ** (beta - 1)
        coords = []
        for i in range(N):
            row, col = divmod(i, 6)
            jx, jy = rng.uniform(-0.14, 0.14), rng.uniform(-0.13, 0.13)
            coords.append(LEFT * 4.95 + RIGHT * (0.83 * col + jx) + UP * (1.82 - 0.72 * row + jy))
        planted_ids = set(rng.sample(range(N), k))
        if not planted:
            planted_ids = set()
        edge_records = []
        for i in range(N):
            for j in range(i + 1, N):
                both_planted = i in planted_ids and j in planted_ids
                if rng.random() < (p_in if both_planted else p_out):
                    edge_records.append((i, j, both_planted))
        edges = VGroup()
        for i, j, within in edge_records:
            color = GOLD if within and planted else GREY_B
            edges.add(Line(coords[i], coords[j], color=color,
                           stroke_width=2.1 if color == GOLD else 1.05,
                           stroke_opacity=0.9 if color == GOLD else 0.55))
        vertices = VGroup()
        labels = VGroup()
        for i, p in enumerate(coords):
            is_planted = i in planted_ids
            vertices.add(colored_dot(p, 0.075, YELLOW if is_planted else BLUE_B))
            labels.add(formula(rf"{i+1}", 13, WHITE).next_to(p, DOWN, buff=0.015))
        return edges, vertices, labels, planted_ids, (p_out, p_in, seed)

    def chapter_pds(self):
        edge_draw, vertices, labels, planted, sample = self.pds_graph(planted=True)
        p_out, p_in, seed = sample
        null = formula(r"G_0\sim G(N,p_{out}),\quad p_{out}=N^{\alpha-1}", 25, BLUE_B).move_to(RIGHT * 2.55 + UP * 1.6)
        planted_model = formula(r"|\mathcal P|=k=\lceil\sqrt N\rceil", 25, YELLOW).move_to(RIGHT * 2.55 + UP * 0.75)
        inside = formula(r"p_{in}=k^{\beta-1}>p_{out}\quad\text{on }\mathcal P\text{ edges}", 23, WHITE).move_to(RIGHT * 2.55 + DOWN * 0.1)
        concrete = formula(r"N=36,\ k=6,\ \alpha=\tfrac12,\ \beta=\tfrac14", 23, WHITE).move_to(RIGHT * 2.55 + DOWN * 1.0)
        concrete_p = formula(r"p_{out}=\tfrac16,\quad p_{in}=6^{-3/4}\approx0.26", 21, TEAL_B).move_to(RIGHT * 2.55 + DOWN * 1.65)
        seed_note = prose(f"Illustrative seeded draw | seed {seed}", 16, GREY_A).move_to(LEFT * 2.7 + DOWN * 2.55)
        self.play(ShowCreation(edge_draw), FadeIn(vertices), Write(labels), run_time=1.2)
        self.play(Write(null), Write(planted_model), Write(inside), Write(concrete), Write(concrete_p), Write(seed_note), run_time=0.9)
        self.play(Indicate(VGroup(*[vertices[i] for i in sorted(planted)]), color=YELLOW), run_time=0.7)
        self.wait(5)

        # Move to a clean algebra board: derive the witness-universe scale.
        self.clear()
        self.chapter_header(8, self.TITLES[7])
        params = formula(r"R=\binom r2,\qquad \rho=k^{\beta-1}", 31, TEAL_B).shift(UP * 1.8)
        size = formula(r"M=k^r\rho^R", 40).shift(UP * 0.9)
        exponents = formula(r"\alpha=\frac{r-1}{r+1},\qquad \beta=\alpha-\delta", 28).shift(DOWN * 0.05)
        gamma = formula(r"M=\Theta(N^\gamma),\qquad \gamma=\frac r{r+1}-\frac{R\delta}{2}", 29, YELLOW).shift(DOWN * 0.95)
        self.play(Write(params), run_time=0.6)
        self.play(Write(size), run_time=0.7)
        self.play(Write(exponents), run_time=0.65)
        self.play(Write(gamma), run_time=0.7)
        bound = formula(r"\delta<\frac1{r(r+1)}\Longrightarrow\gamma>\frac{3r+1}{4(r+1)}>\frac12", 27, TEAL_B).shift(DOWN * 1.8)
        self.play(Write(bound), run_time=0.7)
        self.wait(4)

        # A candidate clique K is a gadget template, not a claim that the sample
        # graph above contains a planted clique.  The dependencies are explicit.
        self.clear()
        self.chapter_header(8, self.TITLES[7])
        gadget_title = formula(r"\text{Candidate }r=3\text{ clique }K=\{v_1,v_2,v_3\}", 27, YELLOW).shift(UP * 2.2)
        tri_pts = [LEFT * 4.3 + UP * 0.55, LEFT * 3.0 + UP * 0.55, LEFT * 3.65 + UP * 1.55]
        tri_edges = VGroup(*[Line(tri_pts[a], tri_pts[b], color=GOLD, stroke_width=3) for a, b in [(0,1),(1,2),(2,0)]])
        tri = VGroup(*[colored_dot(p, 0.13, GOLD) for p in tri_pts])
        tri_names = VGroup(*[formula(rf"v_{i+1}", 18, WHITE).next_to(p, DOWN, buff=0.08) for i,p in enumerate(tri_pts)])
        reps = VGroup(*[RoundedRectangle(width=1.75, height=0.52, corner_radius=0.06, color=TEAL_B).move_to(RIGHT * 0.5 + UP * (0.65 - i*0.65)) for i in range(3)])
        rtxt = VGroup(*[formula(rf"V_{{v_{i},j}}", 21, TEAL_B).move_to(box) for i, box in enumerate(reps, 1)])
        witness = RoundedRectangle(width=1.8, height=0.65, corner_radius=0.07, color=YELLOW).move_to(RIGHT * 4.15)
        wtxt = formula(r"E_K", 27, YELLOW).move_to(witness)
        arcs = VGroup(*[Arrow(box.get_right(), witness.get_left(), color=YELLOW, buff=0.08, stroke_width=2.2) for box in reps])
        self.play(ShowCreation(tri_edges), FadeIn(tri), Write(tri_names), run_time=0.7)
        self.play(FadeIn(reps), Write(rtxt), FadeIn(witness), Write(wtxt), ShowCreation(arcs), run_time=0.9)
        definition = formula(r"E_K=\bigcap_{v\in K}\mathcal U_v", 30, YELLOW).shift(DOWN * 1.45)
        order = formula(r"V_{v,i}\prec E_K\quad(v\in K,\ i\in[\lambda])", 27, TEAL_B).shift(DOWN * 2.1)
        self.play(Write(definition), run_time=0.65)
        self.play(Write(order), run_time=0.65)
        self.wait(4)

        # YES arithmetic gets its own quiet board.
        self.clear()
        self.chapter_header(8, self.TITLES[7])
        yes_head = prose("YES instance: the planted side admits a cheap cover", 29, YELLOW).shift(UP * 2.0)
        yes1 = formula(r"W=\#\{r\text{-clique witnesses inside }\mathcal P\}", 28, WHITE).shift(UP * 1.1)
        yes2 = formula(r"\mathbb E[W]=\binom{k}{r}\rho^R=\Theta(M)", 30, TEAL_B).shift(UP * 0.1)
        yes3 = formula(r"\operatorname{Var}(W)=o(M^2)\quad\Longrightarrow\quad W\leq M", 28, TEAL_B).shift(DOWN * 0.9)
        yes4 = prose("Chebyshev's inequality makes this event hold with high probability.", 20, GREY_A).shift(DOWN * 1.4)
        yes5 = formula(r"\lambda k\leq M+k\leq2M,\quad W\leq M\Longrightarrow\text{cost}\leq3M", 27, YELLOW).shift(DOWN * 2.1)
        self.play(Write(yes_head), Write(yes1), run_time=0.8)
        self.play(Write(yes2), run_time=0.65)
        self.play(Write(yes3), run_time=0.65)
        self.play(Write(yes4), run_time=0.65)
        self.play(Write(yes5), run_time=0.65)
        self.wait(4)

        # NO-side estimate and the hardness consequence have separate line breaks.
        self.clear()
        self.chapter_header(8, self.TITLES[7])
        no_head = prose("NO instance: every small set family covers few witnesses", 29, ORANGE).shift(UP * 2.0)
        q = formula(r"q=N^{-2/(r+1)}=N^{\alpha-1}", 28, WHITE).shift(UP * 1.15)
        bound1 = formula(r"F_G(X)\leq C_rN^\zeta\bigl(q^R|X|^r+|X|\log N\bigr)", 27, ORANGE).shift(UP * 0.2)
        bound2 = formula(r"\text{for every vertex set }X\subseteq[N]", 23, GREY_A).shift(DOWN * 0.65)
        hard = formula(r"\text{Rules out }O(n^{1/2-\epsilon})\text{ and }O(m^{1/4-\epsilon})\text{ factors}", 24, YELLOW).shift(DOWN * 1.55)
        self.play(Write(no_head), Write(q), run_time=0.7)
        self.play(Write(bound1), run_time=0.7)
        self.play(Write(bound2), run_time=0.6)
        self.play(Write(hard), run_time=0.7)
        self.wait(4)

        # Coverage proof: isolate the three probability steps across two cards.
        self.clear()
        self.chapter_header(8, self.TITLES[7])
        cover_head = prose("Completeness: cover every universe item", 27, YELLOW).shift(UP * 2.0)
        mark = formula(r"Z_j=|\{v\in\mathcal P:j\in\mathcal U_v\}|\sim\mathrm{Bin}(k,p),\quad\mathbb E Z_j=pk", 23).shift(UP * 1.05)
        block = formula(r"z=\lceil B\rho^{-(r-1)/2}\rceil,\quad \mathbb E Y=\binom zr\rho^R\to B^r/r!>8", 24, TEAL_B).shift(UP * 0.05)
        good = formula(r"\Pr[Y=0]\leq\frac12\quad\text{for each disjoint marked block}", 25, WHITE).shift(DOWN * 0.95)
        self.play(Write(cover_head), run_time=0.6)
        self.play(Write(mark), run_time=0.65)
        self.play(Write(block), run_time=0.7)
        self.play(Write(good), run_time=0.65)
        self.wait(4)
        self.clear()
        self.chapter_header(8, self.TITLES[7])
        coverage_head2 = prose("Repeat the block test, then union-bound over the universe", 27, YELLOW).shift(UP * 2.0)
        repeated = formula(r"\ell=\lceil A\log N\rceil,\quad A\log2>3\Longrightarrow\Pr[j\text{ uncovered}]\leq2^{-\ell}\leq N^{-A\log2}", 23, YELLOW).shift(DOWN * 1.0)
        union = formula(r"\nu=O(N^\gamma),\ \gamma<1\quad\Longrightarrow\quad\Pr[\exists j\text{ uncovered}]=o(1)", 24, TEAL_B).shift(DOWN * 1.9)
        self.play(Write(coverage_head2), run_time=0.55)
        self.play(Write(repeated), run_time=0.75)
        self.play(Write(union), run_time=0.7)
        self.wait(4)

    def chapter_label_cover(self):
        # A bipartite Label Cover star is generated by a walk on the local
        # expander whose vertices are the center's incident constraint positions.
        u = LEFT * 4.6 + UP * 0.65
        right_vs = [LEFT * 2.6 + UP * y for y in (1.35, 0.55, -0.25)]
        g_edges = VGroup(*[Line(u, p, color=GREY_B, stroke_width=2.1) for p in right_vs])
        g_nodes = VGroup(Circle(radius=0.2, color=YELLOW, fill_color=YELLOW, fill_opacity=0.8).move_to(u),
                         *[Circle(radius=0.18, color=TEAL_B, fill_color=TEAL_B, fill_opacity=0.8).move_to(p) for p in right_vs])
        g_labels = VGroup(formula(r"u\in A", 18, YELLOW).next_to(u, LEFT, buff=0.12),
                          *[formula(rf"v_{i}\in B", 18, TEAL_B).next_to(p, RIGHT, buff=0.12)
                            for i, p in enumerate(right_vs, 1)])
        e_labels = VGroup(*[formula(rf"e_{i}", 17, GREY_A).move_to((u + p) / 2 + UP * 0.12) for i, p in enumerate(right_vs, 1)])
        graph_title = formula(r"e_i=(u,v_i)\in E", 22, TEAL_B).move_to(LEFT * 3.55 + DOWN * 1.1)
        self.play(ShowCreation(g_edges), FadeIn(g_nodes), Write(g_labels), Write(e_labels), Write(graph_title), run_time=1.2)
        self.wait(4)

        # Explicit local expander example on the three constraint positions.
        exp_pts = [LEFT * 0.1 + UP * 1.25, RIGHT * 1.3 + UP * 0.25, LEFT * 0.1 + DOWN * 0.75]
        exp_edges = VGroup(Line(exp_pts[0], exp_pts[1], color=GREY_B, stroke_width=2.1),
                           Line(exp_pts[1], exp_pts[2], color=GREY_B, stroke_width=2.1),
                           Line(exp_pts[2], exp_pts[0], color=GREY_B, stroke_width=2.1))
        exp_nodes = VGroup(*[Circle(radius=0.2, color=BLUE_B, fill_color=BLUE_B, fill_opacity=0.8).move_to(p) for p in exp_pts])
        exp_names = VGroup(*[formula(rf"e_{i}", 19).move_to(p) for i, p in enumerate(exp_pts, 1)])
        exp_title = prose("toy walk on positions; theorem uses a Delta-regular expander", 17, BLUE_B).move_to(RIGHT * 0.7 + DOWN * 1.2)
        walk_arrows = VGroup(Arrow(exp_pts[0], exp_pts[1], color=YELLOW, buff=0.23, stroke_width=3),
                             Arrow(exp_pts[1], exp_pts[2], color=YELLOW, buff=0.23, stroke_width=3))
        walk_formula = formula(r"\sigma=(e_1,e_2,e_3)\quad\text{(two walk steps)}", 22, YELLOW).shift(UP * 2.05 + RIGHT * 0.6)
        star_formula = formula(r"W_\sigma=(u,e_1,e_2,e_3)", 24, WHITE).shift(DOWN * 2.0 + RIGHT * 0.6)
        self.play(ShowCreation(exp_edges), FadeIn(exp_nodes), Write(exp_names), Write(exp_title), run_time=0.9)
        self.play(ShowCreation(walk_arrows), Write(walk_formula), run_time=0.8)
        self.play(Write(star_formula), Indicate(g_nodes[0], color=YELLOW), run_time=0.7)
        self.wait(4)

        # A witness for this ordered star depends on a compatible label bundle
        # for its center and for the right endpoint of every listed constraint.
        self.clear()
        star_head = formula(r"\text{Witness dependencies for }\sigma=(e_1,e_2,e_3)", 28, YELLOW).shift(UP * 2.4)
        compatibility = formula(r"a\in D_{e_i},\qquad \pi_{e_i}(a)=b_i\quad(i=1,2,3)", 30, WHITE).shift(UP * 1.65)
        boxes = [RoundedRectangle(width=2.0, height=0.58, corner_radius=0.06, color=TEAL_B).move_to(LEFT * 3.6 + UP * 0.6),
                 RoundedRectangle(width=2.0, height=0.58, corner_radius=0.06, color=BLUE_B).move_to(LEFT * 1.2 + UP * 1.15),
                 RoundedRectangle(width=2.0, height=0.58, corner_radius=0.06, color=BLUE_B).move_to(LEFT * 1.2 + UP * 0.35),
                 RoundedRectangle(width=2.0, height=0.58, corner_radius=0.06, color=BLUE_B).move_to(LEFT * 1.2 + DOWN * 0.45)]
        bundles = VGroup(*boxes)
        b_labels = VGroup(formula(r"B_{u,a}", 22).move_to(boxes[0]),
                          *[formula(rf"B_{{v_{i},b_{i}}}", 21).move_to(boxes[i]) for i in range(1, 4)])
        witness = RoundedRectangle(width=2.1, height=0.65, corner_radius=0.07, color=YELLOW).move_to(RIGHT * 3.0 + DOWN * 0.05)
        witness_label = formula(r"E_\sigma", 28, YELLOW).move_to(witness)
        deps = VGroup(*[Arrow(box.get_right(), witness.get_left(), color=YELLOW, buff=0.08, stroke_width=2) for box in boxes])
        dependency_note = formula(r"\text{all four bundles precede }E_\sigma", 24, TEAL_B).shift(DOWN * 1.2)
        self.play(Write(star_head), Write(compatibility), FadeIn(bundles), Write(b_labels), run_time=1.0)
        self.play(FadeIn(witness), Write(witness_label), ShowCreation(deps), Write(dependency_note), run_time=0.9)
        self.wait(4)
        self.clear()

        yes_head = formula(r"\text{Completeness: Label Cover value }1", 29, TEAL_B).shift(UP * 2.25)
        yes_steps = VGroup(
            formula(r"\text{choose the bundle for each assigned vertex label}", 26).shift(UP * 1.25),
            formula(r"\text{then select every star witness }E_\sigma", 26).shift(UP * 0.45),
            formula(r"\text{every constraint on every star is compatible}", 26, YELLOW).shift(DOWN * 0.35),
        )
        self.play(Write(yes_head), LaggedStart(*[Write(x) for x in yes_steps], lag_ratio=0.25), run_time=1.2)
        self.wait(4)
        self.clear()

        no_head = formula(r"\text{Soundness: a cheap partial cover would imply a good labeling}", 27, ORANGE).shift(UP * 2.25)
        heavy = formula(r"B_0=\frac{2T}{\theta H},\qquad |L_v|>B_0\;\Longrightarrow\;v\text{ is heavy}", 24).shift(UP * 1.75)
        mass = formula(r"\sum_{v\text{ heavy}}w_v\leq\frac{T}{B_0}=\frac{\theta H}{2}", 28, YELLOW).shift(UP * 1.0)
        light = formula(r"\theta H\text{ covered stars}\;\Longrightarrow\;\geq\theta H/2\text{ use only light vertices}", 22, TEAL_B).shift(UP * 0.25)
        walk_bound = formula(r"\lambda=s^{1/(t+1)},\quad\Pr[\text{one label covers a }t\text{-walk}]\leq p(p+\lambda)^{t-1}", 23, WHITE).shift(DOWN * 0.55)
        random_round = formula(r"\mathbb E[\mathrm{val}]\geq B_0^{-1}\sum_u(d_u/h)p_u,\quad\mathbb E[\mathrm{val}]\leq s", 23, WHITE).shift(DOWN * 1.25)
        conclusion = formula(r"s\geq\frac{\theta}{2C_t(B_0^{1+1/t}+B_0^2\lambda^{t-1})}\quad\Longrightarrow\quad T\geq c_t\theta^{p_t}H s^{-q_t}", 21, ORANGE).shift(DOWN * 2.0)
        self.play(Write(no_head), run_time=0.6)
        for item in [heavy, mass, light]:
            self.play(Write(item), run_time=0.6)
        self.wait(4)
        self.clear()
        self.chapter_header(9, self.TITLES[8])
        expander_head = prose("Expander walk and random rounding", 30, YELLOW).shift(UP * 2.2)
        walk_bound = formula(r"\lambda=s^{1/(t+1)},\quad\Pr[\text{one label covers a }t\text{-walk}]\leq p(p+\lambda)^{t-1}", 24, WHITE).shift(UP * 1.2)
        random_round = formula(r"\mathbb E[\mathrm{val}]\geq B_0^{-1}\sum_u(d_u/h)p_u,\quad\mathbb E[\mathrm{val}]\leq s", 23, WHITE).shift(UP * 0.1)
        conclusion = formula(r"s\geq\frac{\theta}{2C_t(B_0^{1+1/t}+B_0^2\lambda^{t-1})}", 27, TEAL_B).shift(DOWN * 0.85)
        conclusion2 = formula(r"\Longrightarrow\quad T\geq c_t\theta^{p_t}H s^{-q_t}", 29, ORANGE).shift(DOWN * 1.65)
        self.play(Write(expander_head), run_time=0.55)
        for item in [walk_bound, random_round, conclusion, conclusion2]:
            self.play(Write(item), run_time=0.65)
        self.wait(4)
        self.clear()
        self.chapter_header(9, self.TITLES[8])
        params = formula(r"p_t=\frac{2t+1}{t+1},\qquad q_t=\frac{t}{t+1}", 32, YELLOW).shift(UP * 1.85)
        sc = formula(r"T\geq c_t\theta^{p_t}H s^{-q_t}\quad\text{sets for }\theta H\text{ covered stars}", 25, ORANGE).shift(UP * 0.8)
        latency = formula(r"\sum_\sigma\tau(\sigma)\geq c_t\theta^{p_t}H^2s^{-q_t}\quad\text{for a sequence}", 24, TEAL_B).shift(DOWN * 0.05)
        shape = formula(r"\text{precedence height}=2,\qquad |S|\leq1\text{ for every set }S", 26, WHITE).shift(DOWN * 1.0)
        self.play(Write(params), run_time=0.6)
        self.play(Write(sc), run_time=0.7)
        self.play(Write(latency), run_time=0.7)
        self.play(Write(shape), run_time=0.7)
        self.wait(4)
        self.footer("This is the theorem-level gap: it applies to every fixed partial-coverage target theta.")

    def chapter_summary(self):
        nodes = [
            (r"\text{decision tree}", LEFT * 4.5 + UP * 0.65),
            (r"\text{separator cover}", LEFT * 1.5 + UP * 0.65),
            (r"\text{partial cover}", RIGHT * 1.5 + UP * 0.65),
            (r"\text{recursion}", RIGHT * 4.3 + UP * 0.65),
        ]
        boxes = VGroup(*[RoundedRectangle(width=2.5, height=0.78, corner_radius=0.1, color=TEAL_B).move_to(p) for _, p in nodes])
        labels = VGroup(*[formula(name, 21).move_to(box) for (name, _), box in zip(nodes, boxes)])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), color=YELLOW, buff=0.08) for i in range(3)])
        self.play(FadeIn(boxes), Write(labels), ShowCreation(arrows), run_time=1.2)
        approx = formula(r"O(m^{1/3}\log^{4/3}m\log^2 n)", 32, TEAL_B).shift(DOWN * 0.75)
        hard1 = formula(r"\text{PDS: }n^{1/2-\epsilon},\ m^{1/4-\epsilon}\quad(\text{bicriteria})", 26, ORANGE).shift(DOWN * 1.5)
        hard2 = formula(r"\text{outforest: }\log^{2-\epsilon}n\text{ hardness for PCSC}", 24, ORANGE).shift(DOWN * 2.1)
        self.play(Write(approx), run_time=0.65)
        self.play(Write(hard1), run_time=0.65)
        self.play(Write(hard2), run_time=0.65)
        self.footer("The same cover structure drives the approximation reductions and the lower-bound constructions.")

