#!/usr/bin/env python3
"""Check the docs, work out the evidence, and write the views in docs/_generated/.

    python scripts/evidence.py                 # check, then write the views
    python scripts/evidence.py --check         # check only; exit 1 on any error
    python scripts/evidence.py --root example  # run on another folder that has a docs/

What it reads, and what each score means, is in docs/scales.md. It needs PyYAML
(pip install pyyaml). It never edits a source file: everything it works out goes
in docs/_generated/.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("This script needs PyYAML. Install it with: pip install pyyaml")

HERE = Path(__file__).resolve().parent
EVIDENCE_STANCES = {"supports", "contradicts", "mixed"}
DECISION_STATUSES = {"accepted", "proposed", "open", "parked", "superseded", "partly-superseded"}
LIVE_DECISIONS = {"accepted", "proposed"}
HYPOTHESIS_STATUSES = {"active", "retired", "superseded"}
FINDING_STATUSES = {"active", "archived"}
KIND_FOLDERS = {"product": "PRD", "design": "DES", "tech": "TECH", "business": "BIZ"}
ID_PATTERN = re.compile(r"^[A-Z]+-\d+$")
GATE_PATTERN = re.compile(r"^G\d+$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TYPE_NAMES = {"decision": "Decision", "hypothesis": "Hypothesis", "finding": "Finding",
              "objective": "Objective", "kpi": "KPI"}


# ---------------------------------------------------------------- reading

def is_placeholder(value):
    return isinstance(value, str) and ("{{" in value or value.strip() in {"YYYY-MM-DD", ""})


def clean(value):
    """Turn placeholders into None, dates into strings, and drop placeholders from lists."""
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [clean(v) for v in value if not is_placeholder(v)]
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if is_placeholder(value):
        return None
    return value


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        return None, text
    data = yaml.safe_load(match.group(1)) or {}
    return {k: clean(v) for k, v in data.items()}, match.group(2)


def parse_tables(text):
    """Every Markdown table in the text, as a list of row dicts keyed by header."""
    tables, lines, i = [], text.splitlines(), 0
    while i < len(lines) - 1:
        line, below = lines[i].strip(), lines[i + 1].strip()
        if line.startswith("|") and re.match(r"^\|[\s:|-]+\|$", below):
            header = [c.strip() for c in line.strip("|").split("|")]
            rows, i = [], i + 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(dict(zip(header, cells)))
                i += 1
            tables.append((header, rows))
        else:
            i += 1
    return tables


def find_id(cell, prefix):
    match = re.search(rf"\b{prefix}-\d+\b", cell or "")
    return match.group(0) if match else None


def cell_text(cell):
    """A table cell without Markdown links, backticks or bold, or None if it's a placeholder."""
    if cell is None or is_placeholder(cell):
        return None
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cell)
    text = text.replace("`", "").replace("**", "").strip()
    return text or None


def holder(value):
    return {"client": "the client", "ustwo": "ustwo"}.get(value, value or "?")


def num(value):
    return f"{value:g}" if isinstance(value, (int, float)) else str(value)


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


# ---------------------------------------------------------------- the model

class Docs:
    def __init__(self, root, config):
        self.root = root
        self.docs = root / "docs"
        self.cfg = config
        self.items = {}
        self.errors = []
        self.warnings = []
        self.gates = {}

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")

    def rel(self, path):
        return path.relative_to(self.docs).as_posix()

    def add(self, item):
        if item["id"] in self.items:
            self.error(item["path"], f"{item['id']} is already used by {self.items[item['id']]['path']}")
            return
        self.items[item["id"]] = item

    # -- loading

    def load(self):
        self.load_gates()
        self.load_sources()
        self.load_success()
        self.load_files("decisions", "decision", nested=True)
        self.load_files("hypotheses", "hypothesis")
        self.load_files("findings", "finding")

    def load_gates(self):
        path = self.docs / "gates.md"
        if not path.exists():
            return
        for header, rows in parse_tables(path.read_text(encoding="utf-8")):
            if "Gate" not in header or "Stage" not in header:
                continue
            for row in rows:
                gate = (row.get("Gate") or "").strip()
                if not GATE_PATTERN.match(gate):
                    continue
                stage = cell_text(row.get("Stage"))
                if stage not in self.cfg["stages"]:
                    self.error("gates.md", f"{gate} has stage '{stage}', which isn't one of {', '.join(self.cfg['stages'])}")
                self.gates[gate] = {"id": gate, "name": cell_text(row.get("Name")) or gate, "stage": stage}

    def load_sources(self):
        path = self.docs / "sources.md"
        if not path.exists():
            return
        for header, rows in parse_tables(path.read_text(encoding="utf-8")):
            if "ID" not in header:
                continue
            for row in rows:
                sid = find_id(row.get("ID"), "SRC")
                if sid:
                    self.add({"id": sid, "type": "source", "path": "sources.md",
                              "title": cell_text(row.get("Source")) or sid,
                              "audience": cell_text(row.get("Audience"))})

    def load_success(self):
        path = self.docs / "success.md"
        if not path.exists():
            return
        for header, rows in parse_tables(path.read_text(encoding="utf-8")):
            if "Rank" in header:
                for row in rows:
                    oid = find_id(row.get("ID"), "OBJ")
                    if not oid:
                        continue
                    rank = cell_text(row.get("Rank"))
                    if rank and rank not in self.cfg["ranks"]:
                        self.error("success.md", f"{oid} has rank '{rank}', which isn't one of {', '.join(self.cfg['ranks'])}")
                        rank = None
                    self.add({"id": oid, "type": "objective", "path": "success.md",
                              "title": cell_text(row.get("Objective")) or oid,
                              "goal": cell_text(row.get("Goal")), "rank": rank,
                              "stage": cell_text(row.get("Stage")), "gate": cell_text(row.get("Gate")),
                              "label": cell_text(row.get("Label"))})
            elif "Readiness" in header:
                for row in rows:
                    kid = find_id(row.get("ID"), "KPI")
                    if not kid:
                        continue
                    self.add({"id": kid, "type": "kpi", "path": "success.md",
                              "title": cell_text(row.get("KPI")) or kid,
                              "objective": find_id(row.get("Objective"), "OBJ"),
                              "baseline": cell_text(row.get("Baseline")),
                              "target": cell_text(row.get("Target")),
                              "readiness": cell_text(row.get("Readiness")),
                              "stage": cell_text(row.get("Stage")), "gate": cell_text(row.get("Gate")),
                              "label": cell_text(row.get("Label"))})

    def load_files(self, folder, kind, nested=False):
        base = self.docs / folder
        if not base.exists():
            return
        paths = base.glob("*/*.md") if nested else base.glob("*.md")
        for path in sorted(paths):
            if path.name.startswith("_") or path.name == "README.md":
                continue
            where = self.rel(path)
            try:
                fm, body = read_frontmatter(path)
            except yaml.YAMLError as exc:
                self.error(where, f"the frontmatter isn't valid YAML ({exc.__class__.__name__})")
                continue
            if fm is None:
                self.error(where, "has no frontmatter")
                continue
            iid = fm.get("id")
            if not iid or not ID_PATTERN.match(str(iid)):
                self.error(where, f"has no valid id (found '{iid}')")
                continue
            if path.stem != iid:
                self.error(where, f"the file name should match its id, {iid}.md")
            item = {
                "id": iid, "type": kind, "path": where, "body": body,
                "title": fm.get("title") or iid, "status": fm.get("status"), "date": fm.get("date"),
                "stage": fm.get("stage"), "gate": fm.get("gate"),
                "moves": as_list(fm.get("moves")), "links": as_list(fm.get("links")),
                "supersedes": as_list(fm.get("supersedes")), "superseded_by": as_list(fm.get("superseded_by")),
                "impact": fm.get("impact"), "impact_reason": fm.get("impact_reason"),
            }
            if kind == "decision":
                folder_name = path.parent.name
                prefix = iid.split("-")[0]
                if folder_name in KIND_FOLDERS and KIND_FOLDERS[folder_name] != prefix:
                    self.error(where, f"{iid} is in {folder_name}/, which holds {KIND_FOLDERS[folder_name]} decisions")
                item.update(kind=fm.get("kind"), owner=fm.get("owner"), needed_by=fm.get("needed_by"))
            elif kind == "hypothesis":
                item.update(held_by=fm.get("held_by"), stated_confidence=fm.get("stated_confidence"))
            elif kind == "finding":
                item.update(sources=as_list(fm.get("sources")), evidence=fm.get("evidence"),
                            trust=fm.get("trust"), frames=as_list(fm.get("frames")),
                            observed=fm.get("observed"), measurement=fm.get("measurement"),
                            drafted_by=fm.get("drafted_by"), reviewed=fm.get("reviewed"))
                if item["status"] is None:
                    item["status"] = "active"
            self.add(item)

    # -- checks

    def check(self):
        for item in self.items.values():
            where = item["path"] if item["path"] != "success.md" else f"success.md ({item['id']})"
            self.check_place(item, where)
            t = item["type"]
            if t == "decision":
                self.check_decision(item, where)
            elif t == "hypothesis":
                self.check_hypothesis(item, where)
            elif t == "finding":
                self.check_finding(item, where)
            elif t == "kpi":
                if not item["objective"]:
                    self.error(where, "names no objective. Every KPI ladders into one")
                elif item["objective"] not in self.items:
                    self.error(where, f"names {item['objective']}, which isn't in success.md")
            if t in ("decision", "hypothesis", "finding"):
                for mid in item["moves"]:
                    target = self.items.get(mid)
                    if not target or target["type"] not in ("objective", "kpi"):
                        self.error(where, f"moves {mid}, which isn't an objective or KPI in success.md")
                if item["impact"] is not None:
                    if item["impact"] not in (1, 2, 3, 4, 5):
                        self.error(where, f"impact should be 1 to 5, not {item['impact']}")
                    elif not item.get("impact_reason"):
                        self.warn(where, "sets impact by hand without an impact_reason")
            if t in ("decision", "hypothesis"):
                self.check_supersedes(item, where)
        self.check_hypothesis_lines()

    def check_place(self, item, where):
        stage, gate = item.get("stage"), item.get("gate")
        if stage and stage not in self.cfg["stages"]:
            self.error(where, f"stage '{stage}' isn't one of {', '.join(self.cfg['stages'])}")
        if gate:
            if gate not in self.gates:
                self.error(where, f"gate '{gate}' isn't in gates.md")
            elif stage and self.gates[gate]["stage"] and self.gates[gate]["stage"] != stage:
                self.error(where, f"is tagged {stage}, but {gate} is in {self.gates[gate]['stage']}")

    def check_decision(self, item, where):
        if item["status"] not in DECISION_STATUSES:
            self.error(where, f"status '{item['status']}' isn't one of {', '.join(sorted(DECISION_STATUSES))}")
        if item["status"] == "open" and item.get("needed_by") and ISO_DATE.match(str(item["needed_by"])):
            if str(item["needed_by"]) < date.today().isoformat():
                self.warn(where, f"is still open, and was needed by {item['needed_by']}")
        index = self.docs / "decisions" / "README.md"
        if index.exists() and item["id"] not in index.read_text(encoding="utf-8"):
            self.warn(where, f"{item['id']} isn't in the index, decisions/README.md")

    def check_hypothesis(self, item, where):
        if item["status"] not in HYPOTHESIS_STATUSES:
            self.error(where, f"status '{item['status']}' isn't one of {', '.join(sorted(HYPOTHESIS_STATUSES))}")
        if item["held_by"] not in self.cfg["held_by"]:
            self.error(where, f"held_by should be {' or '.join(self.cfg['held_by'])}, not '{item['held_by']}'")
        if item["stated_confidence"] not in (1, 2, 3, 4, 5):
            self.error(where, f"stated_confidence should be 1 to 5, not '{item['stated_confidence']}'")

    def check_finding(self, item, where):
        if item["status"] not in FINDING_STATUSES:
            self.error(where, f"status '{item['status']}' isn't one of {', '.join(sorted(FINDING_STATUSES))}")
        if not item["sources"]:
            self.error(where, "cites no source. Every finding needs at least one SRC ID")
        for sid in item["sources"]:
            if sid not in self.items or self.items[sid]["type"] != "source":
                self.error(where, f"cites {sid}, which isn't in sources.md")
        if item["trust"] not in (1, 2, 3, 4, 5):
            self.error(where, f"trust should be 1 to 5, not '{item['trust']}'")
        if item["evidence"] not in self.cfg["evidence_types"]:
            self.error(where, f"evidence should be one of {', '.join(self.cfg['evidence_types'])}, not '{item['evidence']}'")
        for frame in item["frames"]:
            if frame not in self.cfg["frames"]:
                self.error(where, f"frame '{frame}' isn't one of {', '.join(self.cfg['frames'])}")
        m = item["measurement"]
        if m:
            kid = m.get("kpi") if isinstance(m, dict) else None
            if not kid or kid not in self.items or self.items[kid]["type"] != "kpi":
                self.error(where, f"its measurement names '{kid}', which isn't a KPI in success.md")
        if item["drafted_by"] == "agent" and item["reviewed"] is not True:
            self.warn(where, "is an AI draft nobody has reviewed yet")

    def check_supersedes(self, item, where):
        for other in item["supersedes"]:
            target = self.items.get(other)
            if not target:
                self.error(where, f"supersedes {other}, which doesn't exist")
            elif item["id"] not in target.get("superseded_by", []):
                self.error(where, f"supersedes {other}, but {other} doesn't list it in superseded_by")
        for other in item["superseded_by"]:
            target = self.items.get(other)
            if not target:
                self.error(where, f"is superseded_by {other}, which doesn't exist")
            elif item["id"] not in target.get("supersedes", []):
                self.error(where, f"is superseded_by {other}, but {other} doesn't list it in supersedes")

    def check_hypothesis_lines(self):
        paths = list((self.docs / "prd").glob("*.md")) + [self.docs / "architecture.md"]
        for path in paths:
            if not path.exists():
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "**Hypothesis**" in line and "HYP" not in line:
                    self.warn(f"{self.rel(path)}:{n}", "a Hypothesis line with no HYP ID yet. Log it, and cite it")

    # -- the graph

    def build_graph(self):
        self.evidence = defaultdict(dict)     # claim id -> {finding id: stance}
        self.depends = defaultdict(set)       # item -> what it depends on
        self.dependents = defaultdict(set)    # item -> what depends on it
        self.finding_links = defaultdict(dict)
        for item in list(self.items.values()):
            for link in item.get("links", []):
                self.add_link(item, link)
        self.find_cycles()

    def add_link(self, item, link):
        where = item["path"]
        if not isinstance(link, dict) or not link.get("id"):
            self.error(where, f"has a link without an id: {link}")
            return
        tid, stance = link["id"], link.get("stance")
        target = self.items.get(tid)
        if not target:
            self.error(where, f"links to {tid}, which doesn't exist")
            return
        a, b = item["type"], target["type"]
        claims = ("hypothesis", "decision")
        if a == "finding" and b in claims or b == "finding" and a in claims:
            if stance not in EVIDENCE_STANCES:
                self.error(where, f"links {tid} with stance '{stance}'. Between a finding and a claim, use supports, contradicts or mixed")
                return
            fid, cid = (item["id"], tid) if a == "finding" else (tid, item["id"])
            previous = self.evidence[cid].get(fid)
            if previous and previous != stance:
                self.error(where, f"{fid} and {cid} are linked from both sides with different stances ({previous}, {stance})")
            self.evidence[cid][fid] = stance
        elif a == "finding" and b == "finding":
            if stance not in EVIDENCE_STANCES:
                self.error(where, f"links {tid} with stance '{stance}'. Between findings, use supports, contradicts or mixed")
                return
            self.finding_links[item["id"]][tid] = stance
        elif a in claims and b in claims:
            if stance != "depends":
                self.error(where, f"links {tid} with stance '{stance}'. Between hypotheses and decisions, use depends")
                return
            self.depends[item["id"]].add(tid)
            self.dependents[tid].add(item["id"])
        else:
            self.error(where, f"links to {tid}, a {b}. Use moves for objectives and KPIs, and sources for sources")

    def find_cycles(self):
        state = {}

        def visit(node, path):
            state[node] = "visiting"
            for nxt in sorted(self.depends.get(node, ())):
                if state.get(nxt) == "visiting":
                    cycle = path[path.index(nxt):] + [nxt] if nxt in path else [node, nxt]
                    self.error(self.items[node]["path"], "circular dependency: " + " → ".join(cycle))
                elif nxt not in state:
                    visit(nxt, path + [nxt])
            state[node] = "done"

        for node in sorted(self.depends):
            if node not in state:
                visit(node, [node])

    def closure(self, start, edges):
        seen, stack = set(), list(edges.get(start, ()))
        while stack:
            node = stack.pop()
            if node not in seen:
                seen.add(node)
                stack.extend(edges.get(node, ()))
        return seen

    # -- what gets worked out

    def compute(self):
        cfg = self.cfg
        rank_impact = {k: v for k, v in cfg["impact_from_rank"].items()}
        for item in self.items.values():
            if item["type"] == "objective":
                item["computed_impact"] = rank_impact.get(item["rank"])
            elif item["type"] == "kpi":
                obj = self.items.get(item["objective"] or "")
                item["computed_impact"] = rank_impact.get(obj["rank"]) if obj else None

        def base_impact(item):
            best, why = None, None
            targets = list(item.get("moves", []))
            m = item.get("measurement")
            if isinstance(m, dict) and m.get("kpi"):
                targets.append(m["kpi"])
            for mid in targets:
                target = self.items.get(mid)
                if target and target.get("computed_impact") and (best is None or target["computed_impact"] > best):
                    best, why = target["computed_impact"], f"from {mid}"
            if item.get("impact") in (1, 2, 3, 4, 5) and (best is None or item["impact"] > best):
                best, why = item["impact"], "set by hand"
            return best, why

        memo = {}

        def claim_impact(cid, trail=()):
            if cid in memo:
                return memo[cid]
            if cid in trail:
                return (None, None)
            best, why = base_impact(self.items[cid])
            for dep in sorted(self.dependents.get(cid, ())):
                value, _ = claim_impact(dep, trail + (cid,))
                if value and (best is None or value > best):
                    best, why = value, f"from what rests on it ({dep})"
            memo[cid] = (best, why)
            return memo[cid]

        claims = [i for i in self.items.values() if i["type"] in ("hypothesis", "decision")]
        for item in claims:
            item["computed_impact"], item["impact_from"] = claim_impact(item["id"])

        for item in self.items.values():
            if item["type"] != "finding":
                continue
            best, why = base_impact(item)
            for cid, found in self.evidence.items():
                if item["id"] in found:
                    value = self.items[cid].get("computed_impact")
                    if value and (best is None or value > best):
                        best, why = value, f"from {cid}"
            item["computed_impact"], item["impact_from"] = best, why
            item["seed"] = item["status"] == "active" and not self.is_linked(item)

        weights = {int(k): float(v) for k, v in cfg["trust_weights"].items()}
        for item in claims:
            item.update(self.weigh(item, weights))

        for item in claims:
            if item["type"] != "decision" or item["status"] not in LIVE_DECISIONS:
                continue
            impact = item["computed_impact"] or cfg["default_impact"]
            if impact >= 4 and item["status"] in LIVE_DECISIONS:
                missing = [s for s in ("Drivers", "Alternatives", "Consequences") if f"## {s}" not in item.get("body", "")]
                if missing:
                    self.warn(item["path"], f"is impact {impact}, so it needs {', '.join(missing)} (depth follows the stakes)")

        for item in self.items.values():
            if item["type"] == "finding" and item.get("seed") and item.get("date") and ISO_DATE.match(str(item["date"])):
                age = (date.today() - date.fromisoformat(str(item["date"]))).days
                if age > cfg["seed_review_days"]:
                    self.warn(item["path"], f"has been a seed for {age} days. Link it, turn it into a hypothesis, or archive it")

    def is_linked(self, finding):
        fid = finding["id"]
        if finding["moves"] or (isinstance(finding.get("measurement"), dict) and finding["measurement"].get("kpi")):
            return True
        return any(fid in found for found in self.evidence.values())

    def counts(self, finding):
        if finding["status"] != "active" or finding.get("trust") not in (1, 2, 3, 4, 5):
            return False
        return finding.get("reviewed") is not False or self.cfg["count_unreviewed"]

    def weigh(self, claim, weights):
        cfg = self.cfg
        groups = defaultdict(lambda: [0.0, 0.0])
        lines, unreviewed = [], 0
        for fid, stance in sorted(self.evidence.get(claim["id"], {}).items()):
            finding = self.items[fid]
            if not self.counts(finding):
                if finding["status"] == "active" and finding.get("reviewed") is False:
                    unreviewed += 1
                continue
            w = weights[finding["trust"]]
            s, c = {"supports": (w, 0), "contradicts": (0, w), "mixed": (w / 2, w / 2)}[stance]
            key = finding["sources"][0] if finding["sources"] else fid
            groups[key][0] = max(groups[key][0], s)
            groups[key][1] = max(groups[key][1], c)
            lines.append((stance, fid))
        support = sum(g[0] for g in groups.values())
        against = sum(g[1] for g in groups.values())
        total = support + against
        if not lines:
            verdict = "untested"
        else:
            share = support / total if total else 0.5
            if share >= cfg["supported_from"]:
                verdict = "supported"
            elif share <= cfg["contradicted_below"]:
                verdict = "contradicted"
            else:
                verdict = "contested"
        return {"strength": round(min(cfg["strength_cap"], total), 1), "verdict": verdict,
                "support_weight": round(support, 2), "against_weight": round(against, 2),
                "evidence_lines": lines, "unreviewed": unreviewed}

    def is_live(self, item):
        if item["type"] == "hypothesis":
            return item["status"] == "active"
        if item["type"] == "decision":
            return item["status"] in LIVE_DECISIONS
        return False

    def lists(self):
        cfg = self.cfg
        default = cfg["default_impact"]
        live = [i for i in self.items.values() if i["type"] in ("hypothesis", "decision") and self.is_live(i)]
        respond = []
        for item in live:
            if item["verdict"] == "contradicted" or (
                    item["verdict"] == "contested" and item["against_weight"] >= cfg["respond_from_contradicting"]):
                impact = item["computed_impact"] or default
                respond.append((impact * item["against_weight"], item))
        respond.sort(key=lambda x: (-x[0], x[1]["id"]))
        flagged = {i["id"] for _, i in respond}
        resting = []
        for _, item in respond:
            for dep in sorted(self.closure(item["id"], self.dependents)):
                d = self.items[dep]
                if self.is_live(d) and dep not in flagged:
                    resting.append((d, item["id"]))
        hyps = [i for i in live if i["type"] == "hypothesis"]
        test_next = sorted(
            [((i["computed_impact"] or default) * (cfg["strength_cap"] - i["strength"]), i) for i in hyps
             if i["strength"] < cfg["test_next_below_strength"] and i["id"] not in flagged],
            key=lambda x: (-x[0], x[1]["id"]))
        build_on = sorted(
            [((i["computed_impact"] or default) * i["strength"], i) for i in hyps
             if i["verdict"] == "supported" and i["strength"] >= cfg["build_on_from_strength"]],
            key=lambda x: (-x[0], x[1]["id"]))
        n = cfg["list_length"]
        return respond[:n], resting, test_next[:n], build_on[:n]

    def notes(self, item):
        out = []
        if item["type"] == "hypothesis" and item.get("stated_confidence"):
            conf = item["stated_confidence"]
            if conf >= self.cfg["conviction_flag_from"] and item["verdict"] == "contradicted":
                out.append(f"Starting confidence {conf}, but the evidence has moved against it.")
            elif conf >= self.cfg["conviction_flag_from"] and item["verdict"] == "contested":
                out.append(f"Starting confidence {conf}, and the evidence is mixed.")
        if item.get("unreviewed"):
            n = item["unreviewed"]
            out.append(f"{n} more finding{' is' if n == 1 else 's are'} waiting for review, and not counted yet.")
        return out


# ---------------------------------------------------------------- writing the views

class Views:
    def __init__(self, docs):
        self.d = docs
        self.out = docs.docs / "_generated"

    def ref(self, target, text):
        """A link to a page in docs/, or plain text if this docs/ doesn't have it."""
        path = target.split("#")[0]
        return f"[{text}](../{target})" if (self.d.docs / path).exists() else text

    def link(self, iid):
        item = self.d.items.get(iid)
        if not item or item["type"] == "source":
            return iid
        return f"[{iid}](../{item['path']})"

    def links(self, ids):
        return ", ".join(self.link(i) for i in ids) if ids else "none"

    def impact(self, item):
        value = item.get("computed_impact")
        if not value:
            return f"{self.d.cfg['default_impact']} (default)"
        return f"{value} ({item['impact_from']})" if item.get("impact_from") else str(value)

    def evidence_cell(self, item):
        if item["verdict"] == "untested":
            return "untested"
        return f"{item['verdict']} · {num(item['strength'])}"

    def status_cell(self, item):
        t = item["type"]
        if t == "hypothesis":
            return f"{item['status']} · {self.evidence_cell(item)}"
        if t == "decision":
            return item["status"] or ""
        if t == "finding":
            parts = [f"trust {item['trust']}"]
            if item.get("seed"):
                parts.append("seed")
            if item["status"] == "archived":
                parts.append("archived")
            return " · ".join(parts)
        if t == "objective":
            return item.get("rank") or ""
        if t == "kpi":
            return item.get("readiness") or ""
        return ""

    @staticmethod
    def esc(text):
        return str(text or "").replace("|", "\\|").replace("\n", " ")

    def write(self, name, lines):
        self.out.mkdir(parents=True, exist_ok=True)
        header = ["<!-- Generated by scripts/evidence.py. Don't edit by hand: your changes will be overwritten. -->", ""]
        (self.out / name).write_text("\n".join(header + lines).rstrip() + "\n", encoding="utf-8")

    def all(self):
        self.readme()
        self.evidence()
        self.seeds()
        self.findings()
        self.by_stage()
        self.by_objective()
        self.timeline()
        self.index_json()

    def readme(self):
        items = self.d.items.values()
        count = lambda t, f=lambda i: True: sum(1 for i in items if i["type"] == t and f(i))
        self.write("README.md", [
            "# Generated views",
            "",
            f"Worked out from the docs by `scripts/evidence.py`, on every push to `main`. Nothing here is edited by hand: change the source files, and these follow. How each value is worked out is in {self.ref('scales.md', 'scales')}.",
            "",
            "| View | What it shows |",
            "|---|---|",
            "| [Evidence](evidence.md) | Needs a response, Test next, Build on, and the evidence on every hypothesis and decision |",
            "| [Seeds](seeds.md) | Findings nothing links to yet |",
            "| [Findings](findings.md) | Every finding, by frame: user, product, business and market |",
            "| [By stage](by-stage.md) | Everything tagged with each stage and gate |",
            "| [By objective](by-objective.md) | Each objective, its KPIs and their measurements, and everything that moves it |",
            "| [Timeline](timeline.md) | What we learned and decided, newest first |",
            "| `index.json` | All of it, for agents |",
            "",
            "## In numbers",
            "",
            "| | Count |",
            "|---|---|",
            f"| Decisions | {count('decision')} ({count('decision', lambda i: i['status'] == 'open')} open) |",
            f"| Hypotheses | {count('hypothesis', lambda i: i['status'] == 'active')} active |",
            f"| Findings | {count('finding', lambda i: i['status'] == 'active')} active, of which {count('finding', lambda i: i.get('seed'))} are seeds |",
            f"| Objectives and KPIs | {count('objective')} and {count('kpi')} |",
            f"| Sources | {count('source')} |",
        ])

    def claim_block(self, item):
        d = self.d
        lines = [f"### {item['id']} · {self.esc(item['title'])}", ""]
        if item["type"] == "hypothesis":
            lines.append(f"- Held by {holder(item.get('held_by'))} · starting confidence {item.get('stated_confidence') or '?'} · {item['status']}")
        else:
            lines.append(f"- Decision · {item['status']}")
        lines.append(f"- Impact {self.impact(item)}")
        lines.append(f"- Evidence: **{item['verdict']}** · strength {num(item['strength'])}")
        for stance, fid in item["evidence_lines"]:
            f = d.items[fid]
            lines.append(f"  - {stance}: {self.link(fid)} · {f.get('evidence') or '?'} · trust {f.get('trust')} · {self.esc(f['title'])}")
        lines.append(f"- Rests on: {self.links(sorted(d.depends.get(item['id'], ())))}")
        lines.append(f"- What rests on it: {self.links(sorted(d.dependents.get(item['id'], ())))}")
        for note in d.notes(item):
            lines.append(f"- ⚑ {note}")
        lines.append("")
        return lines

    def evidence(self):
        d = self.d
        respond, resting, test_next, build_on = d.lists()
        lines = ["# Evidence", "",
                 f"What the findings say about each hypothesis and decision. Strength is how much evidence there is (0 to 5). The verdict is which way it points. How both are worked out is in {self.ref('scales.md#what-the-script-works-out', 'scales')}.",
                 "", "## Needs a response", "",
                 "Live hypotheses and decisions the evidence has moved against, most important first.", ""]
        if respond:
            lines += ["| ID | What | Impact | Evidence | Note |", "|---|---|---|---|---|"]
            for _, i in respond:
                lines.append(f"| {self.link(i['id'])} | {self.esc(i['title'])} | {self.impact(i)} | {self.evidence_cell(i)} | {self.esc(' '.join(d.notes(i)))} |")
        else:
            lines.append("Nothing at the moment.")
        lines += ["", "### Resting on something the evidence has moved against", ""]
        if resting:
            lines += ["| ID | What | Rests on |", "|---|---|---|"]
            for item, on in resting:
                lines.append(f"| {self.link(item['id'])} | {self.esc(item['title'])} | {self.link(on)} |")
        else:
            lines.append("Nothing at the moment.")
        lines += ["", "## Test next", "",
                  "Important hypotheses with little evidence either way. The best candidates for a study or a KPI.", ""]
        if test_next:
            lines += ["| ID | Hypothesis | Held by | Impact | Evidence |", "|---|---|---|---|---|"]
            for _, i in test_next:
                lines.append(f"| {self.link(i['id'])} | {self.esc(i['title'])} | {i.get('held_by') or ''} | {self.impact(i)} | {self.evidence_cell(i)} |")
        else:
            lines.append("Nothing at the moment.")
        lines += ["", "## Build on", "", "Hypotheses that are supported and well evidenced.", ""]
        if build_on:
            lines += ["| ID | Hypothesis | Impact | Evidence |", "|---|---|---|---|"]
            for _, i in build_on:
                lines.append(f"| {self.link(i['id'])} | {self.esc(i['title'])} | {self.impact(i)} | {self.evidence_cell(i)} |")
        else:
            lines.append("Nothing yet.")
        hyps = sorted((i for i in d.items.values() if i["type"] == "hypothesis"), key=lambda i: i["id"])
        lines += ["", "## Every hypothesis", ""]
        if not hyps:
            lines.append("None logged yet.")
        for item in hyps:
            lines += self.claim_block(item)
        decisions = sorted((i for i in d.items.values() if i["type"] == "decision"
                            and (i["evidence_lines"] or d.depends.get(i["id"]) or d.dependents.get(i["id"]))),
                           key=lambda i: i["id"])
        lines += ["", "## Decisions with evidence or dependencies", ""]
        if not decisions:
            lines.append("None yet.")
        for item in decisions:
            lines += self.claim_block(item)
        self.write("evidence.md", lines)

    def finding_row(self, f, bears=True):
        bears_on = sorted(cid for cid, found in self.d.evidence.items() if f["id"] in found)
        cells = [self.link(f["id"]), self.esc(f["title"]), str(f.get("trust")), f.get("evidence") or "",
                 ", ".join(f.get("sources", []))]
        if bears:
            cells.append(self.links(bears_on + f.get("moves", [])) if (bears_on or f.get("moves")) else "seed")
        return "| " + " | ".join(cells) + " |"

    def seeds(self):
        seeds = sorted((i for i in self.d.items.values() if i["type"] == "finding" and i.get("seed")), key=lambda i: i["id"])
        lines = ["# Seeds", "",
                 f"Findings nothing links to yet. Each one usually means a hypothesis or decision is waiting to be written. At the weekly review, each seed sparks a hypothesis, earns a link, or is archived. See {self.ref('findings/README.md#seeds', 'findings')}.", ""]
        if seeds:
            lines += ["| ID | Claim | Trust | Evidence | Sources | Logged |", "|---|---|---|---|---|---|"]
            for f in seeds:
                lines.append(f"| {self.link(f['id'])} | {self.esc(f['title'])} | {f.get('trust')} | {f.get('evidence') or ''} | {', '.join(f.get('sources', []))} | {f.get('date') or ''} |")
        else:
            lines.append("No seeds at the moment.")
        self.write("seeds.md", lines)

    def findings(self):
        findings = sorted((i for i in self.d.items.values() if i["type"] == "finding"), key=lambda i: i["id"])
        active = [f for f in findings if f["status"] == "active"]
        lines = ["# Findings by frame", "",
                 "Every active finding, grouped by frame. A finding in more than one frame appears in each.", ""]
        head = ["| ID | Claim | Trust | Evidence | Sources | Bears on |", "|---|---|---|---|---|---|"]
        for frame in self.d.cfg["frames"] + [None]:
            group = [f for f in active if (frame in f.get("frames", [])) or (frame is None and not f.get("frames"))]
            lines += [f"## {frame.capitalize() if frame else 'No frame'}", ""]
            lines += (head + [self.finding_row(f) for f in group]) if group else ["None."]
            lines.append("")
        archived = [f for f in findings if f["status"] == "archived"]
        if archived:
            lines += ["## Archived", "", self.links([f["id"] for f in archived])]
        self.write("findings.md", lines)

    def place(self, item):
        gate = item.get("gate")
        stage = item.get("stage") or (self.d.gates.get(gate, {}).get("stage") if gate else None)
        return stage, gate

    def tagged_table(self, group):
        lines = ["| ID | What | Kind | Status |", "|---|---|---|---|"]
        order = {"objective": 0, "kpi": 1, "decision": 2, "hypothesis": 3, "finding": 4}
        for item in sorted(group, key=lambda i: (order[i["type"]], i["id"])):
            lines.append(f"| {self.link(item['id'])} | {self.esc(item['title'])} | {TYPE_NAMES[item['type']]} | {self.status_cell(item)} |")
        return lines

    def by_stage(self):
        d = self.d
        tagged = [i for i in d.items.values() if i["type"] in TYPE_NAMES
                  and not (i["type"] == "finding" and i["status"] == "archived")]
        lines = ["# By stage and gate", "",
                 f"Everything tagged with a stage or gate, from {self.ref('gates.md', 'gates')}. Tags are optional, so this shows only what's been tagged.", ""]
        for stage in d.cfg["stages"]:
            lines += [f"## {stage.capitalize()}", ""]
            in_stage = [i for i in tagged if self.place(i)[0] == stage]
            whole = [i for i in in_stage if not i.get("gate")]
            lines += (self.tagged_table(whole) if whole else ["Nothing tagged with the stage alone."])
            lines.append("")
            for gate in sorted((g for g in d.gates.values() if g["stage"] == stage), key=lambda g: int(g["id"][1:])):
                lines += [f"### {gate['id']} · {self.esc(gate['name'])}", ""]
                group = [i for i in in_stage if i.get("gate") == gate["id"]]
                lines += (self.tagged_table(group) if group else ["Nothing tagged yet."])
                lines.append("")
        self.write("by-stage.md", lines)

    def by_objective(self):
        d = self.d
        ranks = {r: n for n, r in enumerate(d.cfg["ranks"])}
        objectives = sorted((i for i in d.items.values() if i["type"] == "objective"),
                            key=lambda o: (ranks.get(o.get("rank"), 99), o["id"]))
        kpis = [i for i in d.items.values() if i["type"] == "kpi"]
        movers = [i for i in d.items.values() if i["type"] in ("decision", "hypothesis", "finding")
                  and not (i["type"] == "finding" and i["status"] == "archived")]
        lines = ["# By objective", "",
                 f"Each objective in {self.ref('success.md', 'success')}, its KPIs, their measurements over time, and everything tagged as moving it.", ""]
        if not objectives:
            lines.append("No objectives yet.")
        for obj in objectives:
            lines += [f"## {obj['id']} · {self.esc(obj['title'])}", "",
                      f"Goal: {self.esc(obj.get('goal') or 'not set')} · Rank: {obj.get('rank') or 'not set'}", ""]
            own = sorted((k for k in kpis if k.get("objective") == obj["id"]), key=lambda k: k["id"])
            if own:
                lines += ["| KPI | Measures | Baseline | Target | Readiness |", "|---|---|---|---|---|"]
                for k in own:
                    lines.append(f"| {k['id']} | {self.esc(k['title'])} | {self.esc(k.get('baseline'))} | {self.esc(k.get('target'))} | {self.esc(k.get('readiness'))} |")
                lines.append("")
                for k in own:
                    readings = sorted((f for f in movers if f["type"] == "finding" and isinstance(f.get("measurement"), dict)
                                       and f["measurement"].get("kpi") == k["id"]),
                                      key=lambda f: (str(f["measurement"].get("period") or ""), f["id"]))
                    if readings:
                        lines += [f"**{k['id']} over time**", "", "| Period | Value | Segment | Finding | Trust |", "|---|---|---|---|---|"]
                        for f in readings:
                            m = f["measurement"]
                            lines.append(f"| {self.esc(m.get('period'))} | {self.esc(m.get('value'))} | {self.esc(m.get('segment'))} | {self.link(f['id'])} | {f.get('trust')} |")
                        lines.append("")
            else:
                lines += ["No KPIs yet.", ""]
            ids = {obj["id"]} | {k["id"] for k in own}
            moving = [(i, sorted(set(i.get("moves", [])) & ids)) for i in movers]
            moving = [(i, via) for i, via in moving if via]
            lines += ["**What moves it**", ""]
            if moving:
                lines += ["| ID | What | Kind | Via | Status |", "|---|---|---|---|---|"]
                order = {"decision": 0, "hypothesis": 1, "finding": 2}
                for i, via in sorted(moving, key=lambda x: (order[x[0]["type"]], x[0]["id"])):
                    lines.append(f"| {self.link(i['id'])} | {self.esc(i['title'])} | {TYPE_NAMES[i['type']]} | {', '.join(via)} | {self.status_cell(i)} |")
            else:
                lines.append("Nothing tagged yet.")
            lines.append("")
        self.write("by-objective.md", lines)

    def timeline(self):
        events = []
        for i in self.d.items.values():
            when = str(i.get("date") or "")
            if not ISO_DATE.match(when):
                continue
            if i["type"] == "decision":
                what = f"Decision {i['status']}"
            elif i["type"] == "hypothesis":
                what = f"Hypothesis logged, held by {holder(i.get('held_by'))}" + ("" if i["status"] == "active" else f" ({i['status']})")
            elif i["type"] == "finding":
                what = "Finding logged" + (f", observed {i['observed']}" if i.get("observed") else "") + (" (seed)" if i.get("seed") else "")
            else:
                continue
            events.append((when, i["id"], what, i["title"]))
        events.sort(key=lambda e: (e[0], e[1]), reverse=True)
        lines = ["# Timeline", "",
                 "What was logged or decided, newest first, by each item's date. For what we believed on a given day, check out the repo as it was on that day: `git checkout $(git rev-list -1 --before=2026-11-01 main)`.", ""]
        if events:
            lines += ["| Date | ID | What happened | About |", "|---|---|---|---|"]
            for when, iid, what, title in events:
                lines.append(f"| {when} | {self.link(iid)} | {what} | {self.esc(title)} |")
        else:
            lines.append("Nothing dated yet.")
        self.write("timeline.md", lines)

    def index_json(self):
        keep = ("id", "type", "path", "title", "status", "date", "stage", "gate", "moves", "held_by",
                "stated_confidence", "computed_impact", "impact_from", "strength", "verdict", "support_weight",
                "against_weight", "trust", "evidence", "frames", "sources", "observed", "measurement", "seed",
                "rank", "goal", "objective", "baseline", "target", "readiness", "audience")
        out = {}
        for iid in sorted(self.d.items):
            item = self.d.items[iid]
            entry = {k: item[k] for k in keep if k in item and item[k] not in (None, [], "")}
            if item["type"] in ("hypothesis", "decision"):
                entry["evidence_from"] = [{"finding": f, "stance": s} for s, f in item.get("evidence_lines", [])]
                entry["rests_on"] = sorted(self.d.depends.get(iid, ()))
                entry["rested_on_by"] = sorted(self.d.dependents.get(iid, ()))
                entry["notes"] = self.d.notes(item)
            out[iid] = entry
        respond, resting, test_next, build_on = self.d.lists()
        data = {"items": out, "gates": self.d.gates,
                "lists": {"needs_a_response": [i["id"] for _, i in respond],
                          "resting_on_moved_evidence": [i["id"] for i, _ in resting],
                          "test_next": [i["id"] for _, i in test_next],
                          "build_on": [i["id"] for _, i in build_on]}}
        self.out.mkdir(parents=True, exist_ok=True)
        (self.out / "index.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- running

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="check only, and don't write the views")
    parser.add_argument("--root", default=str(HERE.parent), help="the folder that holds docs/ (default: the repo)")
    parser.add_argument("--quiet", action="store_true", help="print errors only")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / "docs").is_dir():
        sys.exit(f"No docs/ folder in {root}")
    config = yaml.safe_load((HERE / "config.yaml").read_text(encoding="utf-8"))

    docs = Docs(root, config)
    docs.load()
    docs.check()
    docs.build_graph()
    docs.compute()

    if not args.check:
        Views(docs).all()

    for e in docs.errors:
        print(f"ERROR    {e}")
    if not args.quiet:
        for w in docs.warnings:
            print(f"warning  {w}")
        kinds = defaultdict(int)
        for item in docs.items.values():
            kinds[item["type"]] += 1
        plurals = {"decision": "decisions", "hypothesis": "hypotheses", "finding": "findings",
                   "objective": "objectives", "kpi": "KPIs", "source": "sources"}
        summary = ", ".join(f"{kinds[k]} {k if kinds[k] == 1 and k != 'kpi' else plurals[k] if kinds[k] != 1 else 'KPI'}"
                            for k in plurals if kinds[k])
        print(f"\nRead {summary or 'nothing yet'}. {len(docs.errors)} error(s), {len(docs.warnings)} warning(s).")
        if not args.check:
            print(f"Views written to {(docs.docs / '_generated').relative_to(root)}/")
    sys.exit(1 if docs.errors else 0)


if __name__ == "__main__":
    main()
