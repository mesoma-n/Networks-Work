
"""Homework 2, Exercise 4: Network Reconciliation."""

from collections import defaultdict
from typing import Dict, List, Tuple
import networkx as nx


def load(g1_path, g2_path, initial_links_path):
    g1 = nx.read_edgelist(g1_path)
    g2 = nx.read_edgelist(g2_path)

    with open(initial_links_path) as f:
        seeds = [
            tuple(line.split())
            for line in f if line.strip()
        ]

    assert len({x for x, _ in seeds}) == len(seeds)
    assert len({y for _, y in seeds}) == len(seeds)

    a = {u: set(g1.neighbors(u)) for u in g1}
    b = {v: set(g2.neighbors(v)) for v in g2}

    return a, b, seeds


def scores(a, b, links,
           used1=frozenset(), used2=frozenset()):
    counts = defaultdict(int)

    for u, v in links:
        for x in a.get(u, ()):
            if x in used1:
                continue

            for y in b.get(v, ()):
                if y not in used2:
                    counts[x, y] += 1

    return counts


def exercise_4_1(g1_path, g2_path, initial_links_path):
    a, b, seeds = load(
        g1_path, g2_path, initial_links_path
    )

    pairs = sorted(
        (u, v)
        for (u, v), s in scores(a, b, seeds).items()
        if s >= 25
    )

    print("Exercise 4.1:", len(pairs), "pairs")

    for u, v in pairs:
        print(u, v)

    return [[u, v] for u, v in pairs]


def iterative(a, b, seeds, threshold):
    links = list(seeds)
    used1 = {u for u, _ in links}
    used2 = {v for _, v in links}
    added = []

    while True:
        ranked = sorted(
            (
                (s, u, v)
                for (u, v), s in scores(
                    a, b, links, used1, used2
                ).items()
                if s >= threshold
            ),
            reverse=True
        )

        batch = []

        for _, u, v in ranked:
            if u not in used1 and v not in used2:
                batch.append((u, v))
                used1.add(u)
                used2.add(v)

        if not batch:
            return added

        added.extend(batch)
        links.extend(batch)


def write_pairs(path, pairs):
    with open(path, "w") as f:
        for u, v in pairs:
            f.write(f"{u} {v}\n")


def exercise_4_2(
    g1_path, g2_path, initial_links_path,
    thresholds, output_prefix="Ex4-2"
):
    a, b, seeds = load(
        g1_path, g2_path, initial_links_path
    )

    results = {}

    for t in thresholds:
        results[t] = iterative(a, b, seeds, t)

        write_pairs(
            f"{output_prefix}-{t}",
            results[t]
        )

        print(
            "Threshold", t, ":",
            len(results[t]), "additional matches"
        )

    return results


def exercise_4_3(
    g1_path, g2_path, initial_links_path,
    output_path="Ex4-3"
):
    a, b, seeds = load(
        g1_path, g2_path, initial_links_path
    )

    links = list(seeds)
    used1 = {u for u, _ in links}
    used2 = {v for _, v in links}
    added = []

    # Begin with high-confidence matches.
    bootstrap = iterative(a, b, seeds, 13)

    for u, v in bootstrap:
        links.append((u, v))
        used1.add(u)
        used2.add(v)
        added.append((u, v))

    # Gradually lower the threshold.
    for threshold in [11, 9]:
        while True:
            sc = scores(
                a, b, links, used1, used2
            )

            best1 = {}
            best2 = {}

            for (u, v), s in sc.items():
                if s < threshold:
                    continue

                if s > best1.get(u, (-1, ""))[0]:
                    best1[u] = (s, v)

                if s > best2.get(v, (-1, ""))[0]:
                    best2[v] = (s, u)

            runners1 = defaultdict(list)
            runners2 = defaultdict(list)

            for (x, y), z in sc.items():
                runners1[x].append((z, y))
                runners2[y].append((z, x))

            for vals in runners1.values():
                vals.sort(reverse=True)

            for vals in runners2.values():
                vals.sort(reverse=True)

            candidates = []

            for u, (s, v) in best1.items():
                if best2.get(v) != (s, u):
                    continue

                runner_u = next(
                    (
                        z for z, y in runners1[u]
                        if y != v
                    ),
                    0
                )

                runner_v = next(
                    (
                        z for z, x in runners2[v]
                        if x != u
                    ),
                    0
                )

                margin = max(
                    2, int(s * 0.25)
                )

                if s - max(runner_u, runner_v) < margin:
                    continue

                d1 = len(a[u])
                d2 = len(b[v])

                if min(d1, d2) / max(d1, d2) < 0.5:
                    continue

                candidates.append((s, u, v))

            batch = []

            for _, u, v in sorted(
                candidates, reverse=True
            ):
                if u not in used1 and v not in used2:
                    batch.append((u, v))
                    used1.add(u)
                    used2.add(v)

            if not batch:
                break

            links.extend(batch)
            added.extend(batch)

        print(
            "Adaptive threshold", threshold,
            ": total", len(added)
        )

    write_pairs(output_path, added)
    return added


if __name__ == "__main__":
    exercise_4_1(
        "g1", "g2", "linked_pairs"
    )

    exercise_4_2(
        "g1", "g2", "linked_pairs",
        [13, 16, 11]
    )

    exercise_4_3(
        "g1", "g2", "linked_pairs"
    )
