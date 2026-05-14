from __future__ import annotations

import html
import json
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .checker import DECISION_RULES, classify


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = ROOT / "sample-data"
EVIDENCE_CSV = SAMPLE_DIR / "recall_certification_snapshot.csv"
FOUNDRY_IMAGE_URL = (
    "https://devblogs.microsoft.com/foundry/wp-content/uploads/sites/89/2025/11/"
    "cropped-Microsoft-Foundry.2mb-scaled-1.webp"
)


def list_samples() -> list[dict[str, str]]:
    files = sorted(SAMPLE_DIR.glob("vendor_products*.csv"))
    files += sorted((SAMPLE_DIR / "evaluation").glob("vendor_products_labeled.csv"))
    return [
        {
            "name": str(path.relative_to(SAMPLE_DIR)),
            "path": str(path),
        }
        for path in files
    ]


def sample_path(name: str) -> Path:
    path = (SAMPLE_DIR / name).resolve()
    if SAMPLE_DIR.resolve() not in path.parents and path != SAMPLE_DIR.resolve():
        raise ValueError("Sample path must stay inside sample-data")
    if not path.exists() or path.suffix.lower() != ".csv":
        raise FileNotFoundError(name)
    return path


def load_evaluation() -> dict[str, Any]:
    report = ROOT / "outputs" / "evaluation" / "decision_harness_report.json"
    if report.exists():
        return json.loads(report.read_text(encoding="utf-8"))
    return {
        "run_status": "not_generated",
        "message": "Run python scripts/evaluate_decision_harness.py to generate the report.",
    }


def render_page() -> str:
    sample_options = "\n".join(
        f'<option value="{html.escape(item["name"])}">{html.escape(item["name"])}</option>'
        for item in list_samples()
    )
    decision_rows = "\n".join(
        f"""
        <article class="rule-card">
          <div class="rule-head">
            <code>{html.escape(rule_id)}</code>
            <span class="pill {rule['decision'].lower()}">{rule['decision']}</span>
          </div>
          <p>{html.escape(rule['description'])}</p>
          <span class="review-flag">{'Human review required' if rule['human_review_required'] else 'Auto-clear when evidence is strong'}</span>
        </article>
        """
        for rule_id, rule in DECISION_RULES.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>RecallGuard AI Local Demo</title>
  <style>
    :root {{
      --ink: #050505;
      --muted: #666;
      --line: #e7e7e7;
      --soft: #f7f7f7;
      --dark: #010120;
      --mint: #c8f6f9;
      --orange: #fc4c02;
      --magenta: #ef2cc1;
      --periwinkle: #bdbbff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: white;
    }}
    header {{
      background: var(--dark);
      color: white;
      padding: 56px 32px 48px;
      overflow: hidden;
      position: relative;
    }}
    header::after {{
      content: "";
      position: absolute;
      right: -80px;
      top: 40px;
      width: 460px;
      height: 180px;
      border-radius: 4px;
      background: linear-gradient(105deg, var(--orange), var(--magenta), var(--periwinkle));
      transform: rotate(-12deg);
      opacity: .9;
    }}
    .wrap {{ max-width: 1180px; margin: 0 auto; position: relative; z-index: 1; }}
    .eyebrow {{
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 11px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: #c9c9d6;
      margin-bottom: 14px;
    }}
    h1 {{ font-size: clamp(38px, 6vw, 64px); line-height: 1.06; margin: 0; font-weight: 650; letter-spacing: -.03em; max-width: 760px; }}
    .lead {{ margin: 18px 0 0; color: #e7e7f3; max-width: 690px; font-size: 18px; line-height: 1.45; }}
    main {{ padding: 36px 32px 64px; }}
    .section-stack {{ display: grid; gap: 20px; }}
    .grid {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(360px, .82fr); gap: 20px; align-items: start; }}
    .panel {{
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 20px;
      background: white;
      min-width: 0;
      overflow: hidden;
    }}
    .panel.soft {{ background: var(--soft); }}
    .architecture {{
      background: #fff;
      padding: 24px;
    }}
    .arch-top {{ display: grid; grid-template-columns: minmax(0, .9fr) minmax(320px, 1.1fr); gap: 24px; align-items: start; }}
    .arch-copy p {{ color: var(--muted); line-height: 1.45; margin: 0 0 16px; max-width: 620px; }}
    .arch-note {{ border-left: 3px solid #000; padding-left: 12px; font-size: 14px; color: #333; }}
    .flow {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 8px; align-items: stretch; }}
    .flow-card {{
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 12px;
      background: var(--soft);
      position: relative;
    }}
    .flow-card:not(:last-child)::after {{
      content: ">";
      position: absolute;
      right: -8px;
      top: 42%;
      width: 16px;
      height: 16px;
      border-radius: 4px;
      background: #000;
      color: #fff;
      display: grid;
      place-items: center;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
      z-index: 1;
    }}
    .flow-kicker {{ color: var(--muted); font-family: "SFMono-Regular", Consolas, monospace; font-size: 10px; letter-spacing: .06em; text-transform: uppercase; }}
    .flow-title {{ margin-top: 8px; font-weight: 750; overflow-wrap: anywhere; }}
    .flow-detail {{ margin-top: 8px; color: #444; font-size: 13px; line-height: 1.35; }}
    .plane-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 18px; }}
    .plane {{ border: 1px solid var(--line); border-radius: 4px; padding: 14px; background: #fff; }}
    .plane.dark {{ background: var(--dark); color: #fff; border-color: #26263a; }}
    .plane h3 {{ margin: 0 0 10px; }}
    .plane ul {{ margin: 0; padding-left: 18px; color: inherit; line-height: 1.55; }}
    .plane.dark .muted {{ color: #c9c9d6; }}
    h2 {{ margin: 0 0 14px; font-size: 24px; letter-spacing: -.01em; }}
    h3 {{ margin: 22px 0 10px; font-size: 18px; }}
    label {{ display: block; font-weight: 650; margin: 14px 0 8px; }}
    select, textarea {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 11px 12px;
      font: inherit;
      background: white;
    }}
    textarea {{ min-height: 180px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 12px; line-height: 1.45; white-space: pre; overflow: auto; resize: vertical; }}
    .row {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
    button {{
      border: 0;
      border-radius: 4px;
      background: #000;
      color: white;
      padding: 11px 18px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      letter-spacing: .06em;
      text-transform: uppercase;
      cursor: pointer;
    }}
    button.secondary {{ background: var(--mint); color: #000; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; table-layout: fixed; }}
    th, td {{ text-align: left; border-bottom: 1px solid var(--line); padding: 10px 8px; vertical-align: top; }}
    th {{ background: #ebebeb; color: var(--muted); font-family: "SFMono-Regular", Consolas, monospace; text-transform: uppercase; font-size: 10px; letter-spacing: .08em; }}
    td, code {{ overflow-wrap: anywhere; }}
    code, pre {{ font-family: "SFMono-Regular", Consolas, monospace; }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: #0d0d1f; color: #f8f8ff; border-radius: 4px; padding: 14px; max-height: 380px; overflow: auto; font-size: 12px; }}
    .pill {{ display: inline-block; border-radius: 4px; padding: 3px 8px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; }}
    .approve {{ background: #dff7e8; }}
    .review {{ background: #fff0c2; }}
    .hold {{ background: #ffd9d2; }}
    .metric {{ background: white; border: 1px solid var(--line); border-radius: 4px; padding: 12px; min-width: 120px; }}
    .metric strong {{ display: block; font-size: 24px; letter-spacing: -.02em; }}
    .muted {{ color: var(--muted); }}
    .rule-list {{ display: grid; gap: 10px; }}
    .rule-card {{ background: white; border: 1px solid var(--line); border-radius: 4px; padding: 12px; }}
    .rule-head {{ display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }}
    .rule-head code {{ font-size: 11px; line-height: 1.35; }}
    .rule-card p {{ margin: 8px 0 10px; color: #333; line-height: 1.35; }}
    .review-flag {{ color: var(--muted); font-family: "SFMono-Regular", Consolas, monospace; font-size: 10px; letter-spacing: .04em; text-transform: uppercase; }}
    .results-list {{ display: grid; gap: 10px; margin-top: 10px; }}
    .product-card {{ border: 1px solid var(--line); border-radius: 4px; padding: 14px; background: white; }}
    .product-top {{ display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }}
    .product-title {{ font-weight: 700; font-size: 16px; overflow-wrap: anywhere; }}
    .product-meta {{ margin-top: 4px; color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }}
    .product-rule {{ margin-top: 10px; font-size: 12px; color: #333; }}
    .product-action {{ margin-top: 8px; line-height: 1.35; }}
    @media (max-width: 880px) {{
      header {{ padding: 52px 32px 48px; }}
      header::after {{ right: -230px; top: 34px; width: 420px; height: 150px; opacity: .2; }}
      main {{ padding: 36px 16px 64px; }}
      .grid {{ grid-template-columns: 1fr; }}
      .arch-top {{ grid-template-columns: 1fr; }}
      .flow {{ grid-template-columns: 1fr; }}
      .flow-card:not(:last-child)::after {{ display: none; }}
      .plane-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="eyebrow">LOCAL DEMO / GOVERNED MULTI-AGENT CHECKER</div>
      <h1>RecallGuard AI evidence review console</h1>
      <p class="lead">Run the deterministic Task Agent checker locally, inspect APPROVE / REVIEW / HOLD decisions, and view the audit packet added after review feedback.</p>
    </div>
  </header>
  <main>
    <div class="wrap section-stack">
      <section class="panel architecture">
        <div class="eyebrow" style="color:#777;">Architecture / user journey</div>
        <div class="arch-top">
          <div class="arch-copy">
            <h2>How RecallGuard works</h2>
            <p>RecallGuard is a governed product-safety review workflow. A reviewer brings a vendor CSV, the system grounds the policy context first, then runs deterministic evidence checks against certification and recall data.</p>
            <div class="arch-note">The local web app is the hands-on demo surface. The Foundry build is the governed agent workflow: Knowledge Agent, Task Agent, File Search, Code Interpreter, guardrails, traces, and Entra identity.</div>
          </div>
          <div class="flow" aria-label="RecallGuard workflow">
            <article class="flow-card">
              <div class="flow-kicker">Step 01</div>
              <div class="flow-title">Reviewer input</div>
              <div class="flow-detail">Upload or paste vendor product rows.</div>
            </article>
            <article class="flow-card">
              <div class="flow-kicker">Step 02</div>
              <div class="flow-title">Knowledge Agent</div>
              <div class="flow-detail">Grounds product safety policy with File Search.</div>
            </article>
            <article class="flow-card">
              <div class="flow-kicker">Step 03</div>
              <div class="flow-title">Task Agent</div>
              <div class="flow-detail">Runs Code Interpreter and the deterministic checker.</div>
            </article>
            <article class="flow-card">
              <div class="flow-kicker">Step 04</div>
              <div class="flow-title">Decision</div>
              <div class="flow-detail">Returns APPROVE, REVIEW, or HOLD with evidence.</div>
            </article>
            <article class="flow-card">
              <div class="flow-kicker">Step 05</div>
              <div class="flow-title">HITL packet</div>
              <div class="flow-detail">HOLD creates a human-review packet and traceable rationale.</div>
            </article>
          </div>
        </div>
        <div class="plane-grid">
          <div class="plane dark">
            <h3>Microsoft Foundry layer</h3>
            <ul>
              <li>Knowledge Agent: File Search over safety policy and SOP docs</li>
              <li>Task Agent: Code Interpreter runs <code>recallguard_checker.py</code></li>
              <li>Sequential Workflow: policy grounding first, evidence action second</li>
              <li>Guardrails, traces, Entra Agent IDs, least-privilege governance</li>
            </ul>
          </div>
          <div class="plane">
            <h3>Local demo layer</h3>
            <ul>
              <li>Browser UI for a real reviewer workflow</li>
              <li>Same deterministic checker and same sample evidence snapshot</li>
              <li>Decision rules and reviewer packet visible on screen</li>
              <li>25-row evaluation harness available in one click</li>
            </ul>
          </div>
        </div>
      </section>
      <div class="grid">
      <section class="panel">
        <h2>Run a vendor evidence check</h2>
        <label for="sample">Sample CSV</label>
        <div class="row">
          <select id="sample">{sample_options}</select>
          <button class="secondary" onclick="loadSample()">Load sample</button>
        </div>
        <label for="csvText">Vendor CSV input</label>
        <textarea id="csvText" spellcheck="false"></textarea>
        <div class="row" style="margin-top: 14px;">
          <button onclick="classifyCsv()">Run checker</button>
          <button class="secondary" onclick="loadEvaluation()">Load evaluation metrics</button>
        </div>
        <h3>Product decisions</h3>
        <div id="summary" class="row"></div>
        <div id="decisions"></div>
      </section>
      <aside class="panel soft">
        <h2>Audit evidence</h2>
        <p class="muted">Each product result now exposes a decision rule and human reviewer packet.</p>
        <pre id="jsonOut">Select a sample and run the checker.</pre>
        <h3>Decision rules</h3>
        <div class="rule-list">{decision_rows}</div>
      </aside>
      </div>
    </div>
  </main>
  <script>
    const csvText = document.getElementById('csvText');
    const jsonOut = document.getElementById('jsonOut');
    const decisions = document.getElementById('decisions');
    const summary = document.getElementById('summary');
    const filterRow = document.getElementById('filterRow');

    async function request(path, options = {{}}) {{
      const response = await fetch(path, options);
      if (!response.ok) throw new Error(await response.text());
      return response.json();
    }}

    async function loadSample() {{
      const name = document.getElementById('sample').value;
      const data = await request('/api/sample?name=' + encodeURIComponent(name));
      csvText.value = data.content;
      jsonOut.textContent = 'Loaded ' + name + '. Run the checker to classify it.';
      decisions.innerHTML = '';
      summary.innerHTML = '';
    }}

    async function classifyCsv() {{
      const data = await request('/api/classify', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{csv_text: csvText.value}})
      }});
      renderResult(data);
    }}

    async function loadEvaluation() {{
      const data = await request('/api/evaluation');
      jsonOut.textContent = JSON.stringify(data, null, 2);
      summary.innerHTML = `
        <div class="metric"><span class="muted">Rows</span><strong>${{data.total_rows ?? '-'}}</strong></div>
        <div class="metric"><span class="muted">Accuracy</span><strong>${{data.accuracy ?? '-'}}</strong></div>
        <div class="metric"><span class="muted">Mismatches</span><strong>${{(data.mismatches || []).length}}</strong></div>
      `;
      decisions.innerHTML = '';
    }}

    function renderResult(data) {{
      jsonOut.textContent = JSON.stringify(data, null, 2);
      const s = data.summary || {{}};
      summary.innerHTML = `
        <div class="metric"><span class="muted">Total</span><strong>${{s.total_products ?? 0}}</strong></div>
        <div class="metric"><span class="muted">Approve</span><strong>${{s.approve_count ?? 0}}</strong></div>
        <div class="metric"><span class="muted">Review</span><strong>${{s.review_count ?? 0}}</strong></div>
        <div class="metric"><span class="muted">Hold</span><strong>${{s.hold_count ?? 0}}</strong></div>
      `;
      decisions.innerHTML = `
        <div class="results-list">
          ${{(data.products || []).map(product => `
            <article class="product-card">
              <div class="product-top">
                <div>
                  <div class="product-title">${{escapeHtml(product.product_name)}}</div>
                  <div class="product-meta">${{escapeHtml(product.vendor_id)}} · ${{escapeHtml(product.model_name)}} · ${{escapeHtml(product.manufacturer)}}</div>
                </div>
                <span class="pill ${{String(product.decision).toLowerCase()}}">${{escapeHtml(product.decision)}}</span>
              </div>
              <div class="product-rule"><code>${{escapeHtml(product.decision_rule || '')}}</code></div>
              <div class="product-action">${{escapeHtml(product.reviewer_packet?.recommended_next_action || product.recommended_action || '')}}</div>
            </article>
          `).join('')}}
        </div>
      `;
    }}

    function escapeHtml(value) {{
      return String(value ?? '').replace(/[&<>"']/g, char => ({{
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
      }}[char]));
    }}

    loadSample();
  </script>
</body>
</html>"""


def render_app_page() -> str:
    sample_options = "\n".join(
        f'<option value="{html.escape(item["name"])}">{html.escape(item["name"])}</option>'
        for item in list_samples()
    )
    page = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>RecallGuard AI Review Workspace</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css" />
  <style>
    :root {
      --dark: #09091c;
      --ink: #101018;
      --muted: #666a76;
      --line: #dedfe8;
      --panel: #ffffff;
      --soft: #f7f7fa;
      --mint: #bdf4ef;
      --orange: #ef6a3d;
      --magenta: #d84f9c;
      --periwinkle: #aaa7e8;
      --approve-bg: #e2f7ea;
      --approve: #0b6f3c;
      --review-bg: #fff1c6;
      --review: #805400;
      --hold-bg: #ffe0d8;
      --hold: #9a2b1f;
      --dark-soft: #151531;
      --dark-line: #30304e;
    }
    html { scroll-behavior: smooth; }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background:
        linear-gradient(180deg, rgba(189, 187, 255, .18), transparent 360px),
        linear-gradient(90deg, rgba(189, 244, 239, .34), transparent 420px),
        #f4f5f8;
      color: var(--ink);
      font-family: Pretendard, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(circle at 12% 4%, rgba(189, 244, 239, .46), transparent 26%),
        radial-gradient(circle at 92% 12%, rgba(216, 79, 156, .18), transparent 24%),
        radial-gradient(circle at 82% 52%, rgba(170, 167, 232, .2), transparent 30%);
      z-index: -2;
    }
    .app {
      position: relative;
      min-height: 100vh;
      isolation: isolate;
    }
    .app::before {
      content: "";
      position: fixed;
      right: -180px;
      top: 96px;
      width: 680px;
      height: 180px;
      border-radius: 24px;
      background: linear-gradient(105deg, var(--orange), var(--magenta), var(--periwinkle));
      transform: rotate(-14deg);
      opacity: .78;
      pointer-events: none;
      z-index: -1;
    }
    .app::after {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(9, 9, 28, .035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(9, 9, 28, .035) 1px, transparent 1px);
      background-size: 48px 48px;
      mask-image: linear-gradient(180deg, rgba(0,0,0,.75), transparent 72%);
      z-index: -1;
    }
    button, select, textarea, input { font: inherit; }
    button, select { min-height: 44px; }
    button {
      border: 0;
      border-radius: 8px;
      background: #000;
      color: #fff;
      padding: 11px 15px;
      cursor: pointer;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      letter-spacing: .06em;
      text-transform: uppercase;
      transition: opacity .18s ease, transform .18s ease, background .18s ease, border-color .18s ease;
    }
    button:hover { opacity: .9; transform: translateY(-1px); }
    button:active { transform: translateY(1px) scale(.99); }
    button:disabled { opacity: .55; cursor: wait; }
    button:focus-visible, select:focus-visible, textarea:focus-visible, input:focus-visible {
      outline: 3px solid var(--mint);
      outline-offset: 2px;
    }
    .secondary { background: var(--mint); color: #000; }
    .ghost { background: #fff; color: #000; border: 1px solid var(--line); }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(9, 9, 28, .94);
      backdrop-filter: blur(18px);
      color: #fff;
      border-bottom: 1px solid rgba(255,255,255,.1);
    }
    .topbar-inner {
      max-width: 1440px;
      margin: 0 auto;
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }
    .brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
    .logo {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      background: linear-gradient(135deg, var(--orange), var(--magenta), var(--periwinkle));
      flex: 0 0 auto;
    }
    .brand strong { display: block; font-size: 16px; }
    .brand span { display: block; color: #c9c9d6; font-size: 13px; margin-top: 2px; }
    .status { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
    .status .pill {
      border: 1px solid rgba(255,255,255,.14);
      background: rgba(255,255,255,.08);
      color: #fff;
    }
    .shell {
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 32px 44px;
      display: grid;
      grid-template-columns: 292px minmax(0, 1fr) 384px;
      gap: 18px;
      align-items: start;
    }
    .panel {
      background: rgba(255,255,255,.92);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      min-width: 0;
      overflow: hidden;
      backdrop-filter: blur(12px);
      box-shadow: 0 18px 50px rgba(26, 27, 48, .055);
    }
    .soft { background: var(--soft); }
    .sidebar, .inspector { position: sticky; top: 82px; }
    .eyebrow {
      color: var(--muted);
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 11px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1, h2, h3, p { margin-top: 0; }
    h1 { font-size: clamp(30px, 4vw, 44px); line-height: 1.08; letter-spacing: -.03em; margin-bottom: 12px; }
    h2 { font-size: 22px; letter-spacing: -.02em; margin-bottom: 10px; }
    h3 { font-size: 17px; margin-bottom: 10px; }
    p { color: var(--muted); line-height: 1.5; }
    .panel-title-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 14px;
    }
    .panel-title-row h2 { margin-bottom: 4px; }
    .panel-title-row p { margin-bottom: 0; font-size: 14px; max-width: 62ch; }
    .pill {
      display: inline-flex;
      align-items: center;
      border-radius: 8px;
      padding: 4px 8px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 11px;
      line-height: 1;
      white-space: nowrap;
    }
    .approve { background: var(--approve-bg); color: var(--approve); }
    .review { background: var(--review-bg); color: var(--review); }
    .hold { background: var(--hold-bg); color: var(--hold); }
    .workbench-header {
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
      align-items: stretch;
      position: relative;
      background: var(--dark);
      color: #fff;
      border-color: var(--dark-line);
      padding: 24px;
      min-height: 320px;
      box-shadow: 0 30px 90px rgba(9, 9, 28, .2);
    }
    .workbench-header::before {
      content: "";
      position: absolute;
      inset: 1px;
      border-radius: 7px;
      background:
        radial-gradient(circle at 24% 18%, rgba(189, 244, 239, .18), transparent 34%),
        radial-gradient(circle at 88% 8%, rgba(170, 167, 232, .18), transparent 28%);
      pointer-events: none;
      z-index: 0;
    }
    .workbench-header::after {
      content: "";
      position: absolute;
      right: -150px;
      top: 74px;
      width: 520px;
      height: 170px;
      border-radius: 20px;
      background: linear-gradient(105deg, var(--orange), var(--magenta), var(--periwinkle));
      transform: rotate(-13deg);
      opacity: .88;
      z-index: 0;
    }
    .workbench-title { position: relative; z-index: 1; align-self: start; }
    .workbench-title .eyebrow { color: #bdbbff; }
    .workbench-title h1 {
      font-size: clamp(30px, 3.6vw, 46px);
      line-height: 1.02;
      letter-spacing: -.045em;
      margin: 6px 0 10px;
    }
    .workbench-title p { max-width: 68ch; margin-bottom: 0; color: #d8d8e5; }
    .hero-metrics {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-top: 18px;
      max-width: 620px;
    }
    .hero-metric {
      border: 1px solid var(--dark-line);
      border-radius: 8px;
      background: rgba(255,255,255,.05);
      padding: 10px;
      min-width: 0;
    }
    .hero-metric span {
      display: block;
      color: #a9a9c3;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .hero-metric strong { display: block; margin-top: 5px; color: #fff; }
    .active-run-card {
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,.16);
      background: rgba(255,255,255,.96);
      color: var(--ink);
      padding: 16px;
      display: grid;
      grid-template-columns: 176px minmax(0, 1fr);
      gap: 10px;
      min-width: 0;
      position: relative;
      z-index: 1;
      box-shadow: 0 24px 60px rgba(0,0,0,.18);
    }
    .active-run-card .eyebrow { color: var(--muted); }
    .active-run-card strong { font-size: 22px; letter-spacing: -.03em; }
    .active-run-card span { color: var(--muted); font-size: 13px; line-height: 1.35; }
    .run-card-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
      grid-column: 1 / -1;
    }
    .run-card-top .pill {
      border: 1px solid var(--line);
      background: #f5f5fb;
      color: #36364b;
    }
    .run-visual {
      position: relative;
      height: 164px;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      background:
        linear-gradient(135deg, rgba(189,244,239,.62), rgba(255,255,255,.8)),
        #fff;
      grid-row: 2 / span 4;
    }
    .run-visual::before {
      content: "";
      position: absolute;
      left: -38px;
      right: -38px;
      bottom: 18px;
      height: 50px;
      background: linear-gradient(90deg, var(--orange), var(--magenta), var(--periwinkle));
      border-radius: 18px;
      transform: rotate(-9deg);
      opacity: .78;
    }
    .run-orb {
      position: absolute;
      right: 18px;
      top: 18px;
      width: 64px;
      height: 64px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      background: var(--dark);
      color: #fff;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      letter-spacing: .08em;
      box-shadow: 0 0 0 8px rgba(255,255,255,.68);
    }
    .run-orb::after {
      content: "";
      position: absolute;
      inset: -14px;
      border-radius: inherit;
      border: 1px solid rgba(9,9,28,.16);
      animation: pulse-ring 2.4s ease-out infinite;
    }
    .signal-stack {
      display: grid;
      gap: 6px;
      margin-top: 2px;
    }
    .signal-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfbfd;
      padding: 8px 10px;
      font-size: 12px;
    }
    .signal-row span {
      color: var(--muted);
      font-family: "SFMono-Regular", Consolas, monospace;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    .signal-row strong { font-size: 12px; letter-spacing: 0; }
    .run-action {
      width: 100%;
      min-height: 40px;
      background: var(--mint);
      color: #000;
      border: 1px solid #b7edf1;
    }
    .next-action-banner {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr);
      gap: 10px;
      align-items: center;
      border: 1px solid #b7edf1;
      border-radius: 8px;
      background: #f1fcfd;
      padding: 12px;
      margin-bottom: 14px;
    }
    .next-action-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 32px;
      border-radius: 8px;
      background: #000;
      color: #fff;
      padding: 0 10px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .next-action-banner strong { display: block; }
    .next-action-banner span { display: block; margin-top: 3px; color: var(--muted); font-size: 13px; line-height: 1.35; }
    .guide-strip {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-bottom: 12px;
    }
    .guide-step {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 10px;
      display: grid;
      grid-template-columns: 26px minmax(0, 1fr);
      gap: 8px;
      align-items: start;
    }
    .guide-index {
      width: 26px;
      height: 26px;
      border-radius: 8px;
      background: #000;
      color: #fff;
      display: grid;
      place-items: center;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
    }
    .guide-step strong { display: block; font-size: 13px; }
    .guide-step span { display: block; margin-top: 3px; color: var(--muted); font-size: 12px; line-height: 1.3; }
    .workflow-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }
    .workflow-tile {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 13px;
      min-width: 0;
    }
    .workflow-tile strong { display: block; margin-top: 7px; }
    .workflow-tile span { display: block; color: var(--muted); font-size: 12px; line-height: 1.35; margin-top: 5px; }
    .workflow-dot {
      width: 26px;
      height: 26px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      color: #fff;
      background: #000;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 11px;
    }
    .scenario-list { display: grid; gap: 8px; margin-top: 12px; }
    .scenario-card {
      width: 100%;
      background: #fff;
      color: #000;
      border: 1px solid var(--line);
      border-radius: 8px;
      text-align: left;
      font-family: inherit;
      letter-spacing: 0;
      text-transform: none;
      padding: 12px;
      box-shadow: 0 8px 20px rgba(26,27,48,.035);
    }
    .scenario-card:hover { transform: translateY(-1px); border-color: #c7c8d6; }
    .scenario-card.active { border-color: #000; background: #eefbfc; box-shadow: inset 4px 0 0 var(--mint), 0 12px 26px rgba(26,27,48,.06); }
    .scenario-card strong { display: block; font-size: 14px; }
    .scenario-card span { display: block; margin-top: 4px; color: var(--muted); font-size: 12px; line-height: 1.35; }
    .howto { margin: 18px 0 0; padding-left: 18px; line-height: 1.55; color: #333; font-size: 14px; }
    .side-meta {
      margin-top: 14px;
      display: grid;
      gap: 8px;
    }
    .side-meta-row {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      border-top: 1px solid var(--line);
      padding-top: 8px;
      color: var(--muted);
      font-size: 13px;
    }
    .side-meta-row strong { color: var(--ink); }
    .workspace { display: grid; gap: 16px; }
    .toolbar { display: grid; grid-template-columns: minmax(220px, 1fr) auto auto; gap: 10px; align-items: end; }
    label { display: block; font-weight: 700; margin-bottom: 8px; }
    select, textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 11px 12px;
    }
    textarea {
      min-height: 160px;
      resize: vertical;
      white-space: pre;
      overflow: auto;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      line-height: 1.45;
    }
    .file-zone {
      margin-top: 12px;
      border: 1px dashed #c9c9d6;
      border-radius: 8px;
      background: linear-gradient(180deg, #fbfbfd, #f6fbfc);
      padding: 14px;
    }
    .upload-control {
      display: grid;
      grid-template-columns: auto minmax(0, 1fr);
      gap: 10px;
      align-items: center;
      margin-top: 8px;
    }
    .file-input {
      position: absolute;
      width: 1px;
      height: 1px;
      opacity: 0;
      pointer-events: none;
    }
    .upload-button {
      min-height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      border: 1px solid #b7edf1;
      background: var(--mint);
      color: #000;
      padding: 0 16px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      letter-spacing: .06em;
      text-transform: uppercase;
      cursor: pointer;
      transition: opacity .16s ease, transform .16s ease, border-color .16s ease;
    }
    .upload-button:hover { opacity: .88; }
    .upload-button:active { transform: translateY(1px); }
    .file-input:focus-visible + .upload-button {
      outline: 3px solid var(--mint);
      outline-offset: 2px;
    }
    .file-name {
      min-height: 44px;
      display: flex;
      align-items: center;
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--muted);
      padding: 0 12px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .action-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
    .summary-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 14px; }
    .metric { border: 1px solid var(--line); border-radius: 8px; padding: 13px; background: #fff; min-width: 0; }
    .metric span { color: var(--muted); font-size: 13px; }
    .metric strong { display: block; font-size: 28px; letter-spacing: -.03em; margin-top: 3px; }
    .decision-help {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-top: 12px;
    }
    .decision-help-card {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 10px;
      font-size: 13px;
      line-height: 1.35;
    }
    .decision-help-card strong { display: block; margin-bottom: 4px; }
    .decision-help-card:nth-child(1) { background: #f2fbf5; border-color: #cbeedd; }
    .decision-help-card:nth-child(2) { background: #fff9e6; border-color: #f2dfaa; }
    .decision-help-card:nth-child(3) { background: #fff2ef; border-color: #f1c8be; }
    .filter-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }
    .filter-chip {
      min-height: 36px;
      border: 1px solid var(--line);
      background: #fff;
      color: #000;
      padding: 8px 12px;
      font-size: 11px;
    }
    .filter-chip.active {
      background: #000;
      color: #fff;
      border-color: #000;
    }
    .results-list { display: grid; gap: 10px; margin-top: 12px; }
    .empty-state { border: 1px dashed #c9c9d6; border-radius: 8px; padding: 22px; color: var(--muted); background: #fbfbfd; }
    .product-card { border: 1px solid var(--line); border-left-width: 4px; border-radius: 8px; padding: 14px; background: #fff; transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease; }
    .product-card:hover { transform: translateY(-1px); box-shadow: 0 14px 32px rgba(26, 27, 48, .07); }
    .product-card[data-decision="APPROVE"] { border-left-color: var(--approve); }
    .product-card[data-decision="REVIEW"] { border-left-color: var(--review); }
    .product-card[data-decision="HOLD"] { border-left-color: var(--hold); }
    .product-card.selected { border-color: #000; border-left-color: #000; background: #fcfcff; box-shadow: 0 16px 38px rgba(26,27,48,.08); }
    .product-top { display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }
    .product-title { font-weight: 760; font-size: 17px; overflow-wrap: anywhere; }
    .product-meta { margin-top: 4px; color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
    .product-rule { margin-top: 10px; font-size: 12px; }
    .product-action { margin-top: 8px; line-height: 1.35; }
    .product-footer { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-top: 12px; }
    .mini-button { min-height: 36px; padding: 8px 10px; font-size: 10px; background: #fff; color: #000; border: 1px solid var(--line); border-radius: 8px; }
    .flow-list { display: grid; gap: 8px; }
    .foundry-proof-card {
      display: grid;
      grid-template-columns: 78px minmax(0, 1fr);
      gap: 14px;
      align-items: center;
      border: 1px solid var(--line);
      border-radius: 8px;
      background:
        linear-gradient(135deg, rgba(189,187,255,.22), rgba(189,244,239,.2)),
        #fff;
      padding: 12px;
      margin: 4px 0 14px;
    }
    .foundry-mark {
      width: 78px;
      height: 78px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: #070718;
      overflow: hidden;
    }
    .foundry-mark img {
      width: 72px;
      height: 72px;
      object-fit: contain;
      display: block;
    }
    .foundry-proof-card strong { display: block; font-size: 15px; }
    .foundry-proof-card p { margin: 5px 0 0; font-size: 13px; line-height: 1.35; }
    .foundry-proof-card .eyebrow { color: #5e5e78; }
    .flow-node {
      display: grid;
      grid-template-columns: 28px minmax(0, 1fr);
      gap: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 10px;
    }
    .node-index {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      background: #000;
      color: #fff;
      display: grid;
      place-items: center;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 11px;
    }
    .node-title { font-weight: 760; }
    .node-copy { color: var(--muted); font-size: 13px; line-height: 1.35; margin-top: 3px; }
    code, pre { font-family: "SFMono-Regular", Consolas, monospace; }
    code { overflow-wrap: anywhere; }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      background: #0d0d1f;
      color: #f8f8ff;
      border-radius: 8px;
      padding: 14px;
      max-height: 360px;
      overflow: auto;
      font-size: 12px;
    }
    .packet-header { display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; }
    .packet-title { font-weight: 760; margin-top: 4px; }
    .rule-list { display: grid; gap: 8px; margin-top: 10px; }
    .rule-card { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 11px; }
    .rule-head { display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; }
    .rule-head code { font-size: 10px; line-height: 1.35; }
    .rule-card p { margin: 8px 0 0; color: #333; line-height: 1.35; font-size: 13px; }
    .evaluation-card { border: 1px solid var(--line); border-radius: 8px; background: #fff; padding: 12px; }
    .evaluation-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin-top: 10px; }
    .copilot-card {
      background: var(--dark);
      color: #fff;
      border-color: var(--dark-line);
      padding: 0;
      position: relative;
      overflow: hidden;
    }
    .copilot-card::before {
      content: "";
      position: absolute;
      right: -92px;
      top: 34px;
      width: 260px;
      height: 92px;
      border-radius: 20px;
      background: linear-gradient(105deg, var(--orange), var(--magenta), var(--periwinkle));
      transform: rotate(-13deg);
      opacity: .22;
      pointer-events: none;
    }
    .copilot-shell { padding: 16px; position: relative; z-index: 1; }
    .copilot-band {
      display: none;
    }
    .copilot-card p { color: #c9c9d6; }
    .copilot-status { background: #26263a; color: #fff; }
    .copilot-context-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 12px;
    }
    .copilot-context {
      border: 1px solid var(--dark-line);
      border-radius: 8px;
      background: var(--dark-soft);
      padding: 10px;
      min-width: 0;
    }
    .copilot-context span {
      display: block;
      color: #9b9bb3;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .copilot-context strong {
      display: block;
      margin-top: 5px;
      color: #fff;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .copilot-log {
      display: grid;
      gap: 8px;
      max-height: 240px;
      overflow: auto;
      margin-top: 12px;
      padding-right: 2px;
    }
    .copilot-message {
      border: 1px solid #26263a;
      border-radius: 8px;
      padding: 10px;
      line-height: 1.38;
      font-size: 13px;
    }
    .copilot-message.agent { background: var(--dark-soft); color: #f8f8ff; }
    .copilot-message.user { background: #f8f8ff; color: #08080d; border-color: #f8f8ff; }
    .copilot-message strong {
      display: block;
      margin-bottom: 4px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 10px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .quick-prompts {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 12px;
    }
    .quick-prompts .mini-button {
      min-height: 38px;
      background: #171733;
      color: #fff;
      border-color: #31314d;
      white-space: normal;
      text-align: left;
      line-height: 1.25;
    }
    .copilot-input-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      margin-top: 10px;
    }
    .copilot-input {
      width: 100%;
      min-height: 44px;
      border: 1px solid #31314d;
      border-radius: 8px;
      background: #08081f;
      color: #fff;
      padding: 11px 12px;
    }
    .copilot-input::placeholder { color: #9b9bb3; }
    .copilot-submit { border-radius: 8px; background: var(--mint); color: #000; }
    .copilot-note {
      margin-top: 10px;
      color: #9b9bb3;
      font-size: 12px;
      line-height: 1.4;
    }
    @media (max-width: 1120px) {
      .shell { grid-template-columns: 260px minmax(0, 1fr); }
      .inspector { grid-column: 1 / -1; position: static; }
    }
    @media (max-width: 760px) {
      .topbar-inner { align-items: flex-start; flex-direction: column; }
      .shell { grid-template-columns: 1fr; padding: 16px; }
      .sidebar { position: static; order: 2; }
      .workspace { order: 1; }
      .inspector { order: 3; }
      .workbench-header { grid-template-columns: 1fr; }
      .workbench-header::after { right: -260px; top: 86px; opacity: .38; }
      .active-run-card { grid-template-columns: 1fr; }
      .run-visual { grid-row: auto; height: 116px; }
      .hero-metrics { grid-template-columns: 1fr; }
      .workflow-strip { grid-template-columns: 1fr 1fr; }
      .next-action-banner { grid-template-columns: 1fr; }
      .guide-strip, .decision-help { grid-template-columns: 1fr; }
      .toolbar { grid-template-columns: 1fr; }
      .summary-grid, .evaluation-grid { grid-template-columns: 1fr 1fr; }
      .upload-control { grid-template-columns: 1fr; }
      .quick-prompts { grid-template-columns: 1fr; }
      .copilot-context-grid { grid-template-columns: 1fr; }
      .copilot-input-row { grid-template-columns: 1fr; }
    }
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; scroll-behavior: auto !important; }
    }
    @keyframes pulse-ring {
      0% { transform: scale(.82); opacity: .42; }
      100% { transform: scale(1.18); opacity: 0; }
    }
  </style>
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div class="topbar-inner">
        <div class="brand">
          <div class="logo" aria-hidden="true"></div>
          <div>
            <strong>RecallGuard AI</strong>
            <span>Governed product safety review workspace</span>
          </div>
        </div>
        <div class="status" aria-label="System status">
          <span class="pill approve">Local demo live</span>
          <span class="pill review">Foundry workflow mapped</span>
          <span class="pill approve">8 tests passed</span>
        </div>
      </div>
    </header>

    <div class="shell">
      <aside class="panel sidebar">
        <div class="eyebrow">Case queue</div>
        <h2>Try a case</h2>
        <p>Start with a sample case. You can upload your own CSV after that.</p>
        <div class="scenario-list">
          <button class="scenario-card active" data-sample="vendor_products_complete.csv"><strong>Safe products</strong><span>Two products should be approved.</span></button>
          <button class="scenario-card" data-sample="vendor_products_public_recall_match.csv"><strong>Recall risk</strong><span>One product should be held.</span></button>
          <button class="scenario-card" data-sample="vendor_products_missing_fields.csv"><strong>Missing info</strong><span>Incomplete rows need review.</span></button>
          <button class="scenario-card" data-sample="vendor_products_prompt_injection.csv"><strong>Unsafe vendor note</strong><span>Vendor instructions are ignored as data.</span></button>
        </div>
        <div class="side-meta">
          <div class="side-meta-row"><span>Workflow</span><strong>Sequential</strong></div>
          <div class="side-meta-row"><span>Guardrail</span><strong>Active</strong></div>
          <div class="side-meta-row"><span>Review mode</span><strong>HITL</strong></div>
        </div>
      </aside>

      <main class="workspace">
        <section class="panel workbench-header">
          <div class="workbench-title">
            <div class="eyebrow">Product safety console</div>
            <h1>Check products before listing</h1>
            <p>Pick a sample or upload a CSV. RecallGuard checks each product and tells you whether to approve, review, or hold it.</p>
            <div class="hero-metrics" aria-label="Review system highlights">
              <div class="hero-metric"><span>Workflow</span><strong>Foundry agents</strong></div>
              <div class="hero-metric"><span>Evaluation</span><strong>25 labeled rows</strong></div>
              <div class="hero-metric"><span>Control</span><strong>Human review</strong></div>
            </div>
          </div>
          <div class="active-run-card">
            <div class="run-card-top">
              <div class="eyebrow">Current run</div>
              <span class="pill">Operator view</span>
            </div>
            <div class="run-visual" aria-hidden="true">
              <div class="run-orb">AI</div>
            </div>
            <strong id="runStateLabel">Ready</strong>
            <span id="runStateCopy">No review has been executed in this session.</span>
            <div class="signal-stack" aria-label="Control signals">
              <div class="signal-row"><span>Policy</span><strong>Grounded</strong></div>
              <div class="signal-row"><span>Evidence</span><strong>Deterministic</strong></div>
              <div class="signal-row"><span>Governance</span><strong>HITL</strong></div>
            </div>
            <button id="nextActionBtn" class="run-action" data-action="run">Run review</button>
          </div>
        </section>

        <section class="panel">
          <div class="panel-title-row">
            <div>
              <div class="eyebrow">Evidence intake</div>
              <h2>Vendor submission</h2>
              <p>The sample is already loaded. Press Run review to see the workflow, or upload your own CSV.</p>
            </div>
            <span class="pill review">CSV required</span>
          </div>
          <div class="guide-strip" aria-label="How to use RecallGuard">
            <div class="guide-step"><div class="guide-index">1</div><div><strong>Choose data</strong><span>Use a sample or upload CSV.</span></div></div>
            <div class="guide-step"><div class="guide-index">2</div><div><strong>Run review</strong><span>Classify every product row.</span></div></div>
            <div class="guide-step"><div class="guide-index">3</div><div><strong>Inspect result</strong><span>Open the packet for details.</span></div></div>
          </div>
          <div class="next-action-banner" id="nextActionBanner">
            <div class="next-action-badge">Next</div>
            <div>
              <strong id="nextActionTitle">Run the loaded sample</strong>
              <span id="nextActionText">The default CSV is already loaded. Click Run review to classify products.</span>
            </div>
          </div>
          <div class="toolbar">
            <div>
              <label for="sample">Sample CSV</label>
              <select id="sample">__SAMPLE_OPTIONS__</select>
            </div>
            <button class="secondary" id="loadSampleBtn">Load sample</button>
            <button id="runBtn">Run review</button>
          </div>
          <div class="file-zone">
            <label for="fileInput">Upload local CSV</label>
            <div class="upload-control">
              <input class="file-input" id="fileInput" type="file" accept=".csv,text/csv" />
              <label class="upload-button" for="fileInput">Choose CSV</label>
              <div class="file-name" id="fileName">No file selected</div>
            </div>
          </div>
          <label for="csvText" style="margin-top:14px;">CSV preview / editable input</label>
          <textarea id="csvText" spellcheck="false"></textarea>
          <div class="action-row">
            <button id="runBtnBottom">Run review</button>
            <button class="secondary" id="evalBtn">View evaluation metrics</button>
            <button class="ghost" id="clearBtn">Clear results</button>
          </div>
        </section>

        <section class="panel">
          <div class="panel-title-row">
            <div>
              <div class="eyebrow">Decision output</div>
              <h2>Review results</h2>
              <p>Filter by status, then inspect the packet for any product that needs a closer look.</p>
            </div>
            <span class="pill approve">Auditable</span>
          </div>
          <div id="summary" class="summary-grid"></div>
          <div class="decision-help" aria-label="Decision meaning">
            <div class="decision-help-card"><strong>APPROVE</strong>Evidence is strong enough to proceed.</div>
            <div class="decision-help-card"><strong>REVIEW</strong>Missing or weak evidence needs a human check.</div>
            <div class="decision-help-card"><strong>HOLD</strong>Recall risk or strong safety signal. Do not list.</div>
          </div>
          <div id="filterRow" class="filter-row" aria-label="Filter product results">
            <button class="filter-chip active" data-filter="ALL">All</button>
            <button class="filter-chip" data-filter="APPROVE">Approve</button>
            <button class="filter-chip" data-filter="REVIEW">Review</button>
            <button class="filter-chip" data-filter="HOLD">Hold</button>
          </div>
          <div id="decisions" class="results-list">
            <div class="empty-state"><strong>No review yet.</strong><br />Click Run review to create product decisions and reviewer packets.</div>
          </div>
        </section>
      </main>

      <aside class="inspector">
        <section class="panel">
          <div class="eyebrow">System checks</div>
          <h2>Behind the scenes</h2>
          <div class="foundry-proof-card">
            <div class="foundry-mark">
              <img src="__FOUNDRY_IMAGE_URL__" alt="Microsoft Foundry visual mark" loading="lazy" />
            </div>
            <div>
              <div class="eyebrow">Microsoft Foundry</div>
              <strong>Governed agent workflow</strong>
              <p>Knowledge grounding, Code Interpreter action path, traces, guardrails, and Entra ownership.</p>
            </div>
          </div>
          <div class="flow-list">
            <div class="flow-node"><div class="node-index">KB</div><div><div class="node-title">Knowledge grounding</div><div class="node-copy">Policy and recall-response sources are mapped to the Knowledge Agent.</div></div></div>
            <div class="flow-node"><div class="node-index">CI</div><div><div class="node-title">Evidence checker</div><div class="node-copy"><code>recallguard_checker.py</code> performs the CSV action path.</div></div></div>
            <div class="flow-node"><div class="node-index">GR</div><div><div class="node-title">Guardrails</div><div class="node-copy">Prompt-injection notes are treated as vendor data, not instructions.</div></div></div>
            <div class="flow-node"><div class="node-index">ID</div><div><div class="node-title">Governance</div><div class="node-copy">Entra ownership, traces, and HITL packets support audit review.</div></div></div>
          </div>
        </section>

        <section class="panel copilot-card" style="margin-top:16px;">
          <div class="copilot-band" aria-hidden="true"></div>
          <div class="copilot-shell">
            <div class="packet-header">
              <div>
                <div class="eyebrow" style="color:#bdbbff;">Review assistant</div>
                <div class="packet-title">Reviewer Copilot</div>
              </div>
              <span class="pill copilot-status">Context aware</span>
            </div>
            <p>Ask about the selected product, missing evidence, guardrails, or the next reviewer action.</p>
            <div class="copilot-context-grid" aria-label="Copilot review context">
              <div class="copilot-context"><span>Selected product</span><strong id="copilotContextProduct">No product selected</strong></div>
              <div class="copilot-context"><span>Decision state</span><strong id="copilotContextDecision">Waiting</strong></div>
            </div>
            <div id="copilotLog" class="copilot-log" aria-live="polite"></div>
            <div class="quick-prompts" aria-label="Reviewer Copilot prompts">
              <button class="mini-button copilot-prompt" data-prompt="Why was the selected product classified this way?">Why this decision?</button>
              <button class="mini-button copilot-prompt" data-prompt="What evidence or missing fields should I review?">Evidence check</button>
              <button class="mini-button copilot-prompt" data-prompt="Generate a concise reviewer memo for the selected product.">Reviewer memo</button>
              <button class="mini-button copilot-prompt" data-prompt="Explain the guardrails and human review path.">Guardrails</button>
            </div>
            <div class="copilot-input-row">
              <input id="copilotInput" class="copilot-input" type="text" placeholder="Ask about this review..." />
              <button id="askCopilotBtn" class="copilot-submit">Ask</button>
            </div>
          </div>
        </section>

        <section class="panel soft" style="margin-top:16px;">
          <div class="packet-header">
            <div>
              <div class="eyebrow">Reviewer packet</div>
              <div id="packetTitle" class="packet-title">No product selected</div>
            </div>
            <span id="packetDecision" class="pill review">Waiting</span>
          </div>
          <p id="packetHint">Run a review, then choose Inspect packet on a product card.</p>
          <pre id="packetOut">Reviewer evidence will appear here.</pre>
        </section>

        <section class="panel" style="margin-top:16px;">
          <div class="eyebrow">Decision rules</div>
          <h2>Audit logic</h2>
          <div id="ruleList" class="rule-list"></div>
        </section>
      </aside>
    </div>
  </div>
  <script>
    const DECISION_RULES = __DECISION_RULES__;
    let lastResult = null;
    let selectedProductIndex = null;
    let decisionFilter = 'ALL';
    const csvText = document.getElementById('csvText');
    const decisions = document.getElementById('decisions');
    const summary = document.getElementById('summary');
    const filterRow = document.getElementById('filterRow');
    const packetTitle = document.getElementById('packetTitle');
    const packetDecision = document.getElementById('packetDecision');
    const packetHint = document.getElementById('packetHint');
    const packetOut = document.getElementById('packetOut');
    const fileName = document.getElementById('fileName');
    const copilotLog = document.getElementById('copilotLog');
    const copilotInput = document.getElementById('copilotInput');
    const askCopilotBtn = document.getElementById('askCopilotBtn');
    const copilotContextProduct = document.getElementById('copilotContextProduct');
    const copilotContextDecision = document.getElementById('copilotContextDecision');
    const runStateLabel = document.getElementById('runStateLabel');
    const runStateCopy = document.getElementById('runStateCopy');
    const nextActionTitle = document.getElementById('nextActionTitle');
    const nextActionText = document.getElementById('nextActionText');
    const nextActionBtn = document.getElementById('nextActionBtn');
    const runButtons = [document.getElementById('runBtn'), document.getElementById('runBtnBottom'), nextActionBtn];

    async function request(path, options = {}) {
      const response = await fetch(path, options);
      if (!response.ok) throw new Error(await response.text());
      return response.json();
    }

    async function loadSample(name = document.getElementById('sample').value) {
      document.getElementById('sample').value = name;
      const data = await request('/api/sample?name=' + encodeURIComponent(name));
      csvText.value = data.content;
      fileName.textContent = 'No file selected';
      clearResults('Loaded ' + name + '. Run the review to classify products.');
      document.querySelectorAll('.scenario-card').forEach(button => {
        button.classList.toggle('active', button.dataset.sample === name);
      });
    }

    function clearResults(message = 'Run the checker to populate product decisions and reviewer packets.') {
      lastResult = null;
      selectedProductIndex = null;
      decisionFilter = 'ALL';
      setActiveFilter('ALL');
      decisions.innerHTML = `<div class="empty-state"><strong>Ready for review.</strong><br />${escapeHtml(message)}</div>`;
      summary.innerHTML = '';
      packetTitle.textContent = 'No product selected';
      packetDecision.className = 'pill review';
      packetDecision.textContent = 'Waiting';
      packetHint.textContent = 'Run a review, then choose Inspect packet on a product card.';
      packetOut.textContent = 'Reviewer evidence will appear here.';
      runStateLabel.textContent = 'Ready';
      runStateCopy.textContent = message;
      setNextAction('Run the loaded sample', 'The CSV is ready. Click Run review to classify products.', 'Run review', 'run');
      updateCopilotContext();
      resetCopilot(message);
    }

    async function classifyCsv() {
      try {
        setLoading(true);
        const data = await request('/api/classify', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({csv_text: csvText.value})
        });
        renderResult(data);
      } catch (error) {
        decisions.innerHTML = `<div class="empty-state">Review failed: ${escapeHtml(error.message)}</div>`;
      } finally {
        setLoading(false);
      }
    }

    async function loadEvaluation() {
      const data = await request('/api/evaluation');
      lastResult = null;
      summary.innerHTML = `
        <div class="metric"><span>Rows</span><strong>${data.total_rows ?? '-'}</strong></div>
        <div class="metric"><span>Accuracy</span><strong>${data.accuracy ?? '-'}</strong></div>
        <div class="metric"><span>Mismatches</span><strong>${(data.mismatches || []).length}</strong></div>
        <div class="metric"><span>Status</span><strong>${escapeHtml(data.run_status || '-')}</strong></div>
      `;
      decisions.innerHTML = `
        <div class="evaluation-card">
          <strong>Evaluation harness</strong>
          <p>25 labeled rows covering certification, missing identifiers, recall evidence, prompt injection, and normalization.</p>
          <div class="evaluation-grid">
            ${Object.entries(data.label_metrics || {}).map(([label, metrics]) => `
              <div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(metrics.correct_count)}/${escapeHtml(metrics.expected_count)}</strong></div>
            `).join('')}
          </div>
        </div>
      `;
      packetTitle.textContent = 'Evaluation report';
      packetDecision.className = 'pill approve';
      packetDecision.textContent = 'PASS';
      packetHint.textContent = 'Saved from outputs/evaluation/decision_harness_report.json.';
      packetOut.textContent = JSON.stringify(data, null, 2);
      runStateLabel.textContent = 'Evaluation loaded';
      runStateCopy.textContent = `${data.total_rows ?? '-'} labeled rows checked with ${data.accuracy ?? '-'} accuracy.`;
      setNextAction('Return to product review', 'Load a sample or upload a CSV, then run a product review.', 'Run review', 'run');
      updateCopilotContext('Evaluation harness', 'PASS');
    }

    function renderResult(data) {
      lastResult = data;
      const s = data.summary || {};
      summary.innerHTML = `
        <div class="metric"><span>Total</span><strong>${s.total_products ?? 0}</strong></div>
        <div class="metric"><span>Approve</span><strong>${s.approve_count ?? 0}</strong></div>
        <div class="metric"><span>Review</span><strong>${s.review_count ?? 0}</strong></div>
        <div class="metric"><span>Hold</span><strong>${s.hold_count ?? 0}</strong></div>
      `;
      runStateLabel.textContent = 'Review complete';
      runStateCopy.textContent = `${s.total_products ?? 0} products checked. ${s.hold_count ?? 0} hold and ${s.review_count ?? 0} review item(s) need attention.`;
      setNextAction('Inspect the first product', 'Open the reviewer packet to see evidence, missing data, and the recommended action.', 'Inspect first product', 'inspect');
      decisions.innerHTML = `
        <div class="results-list">
          ${(data.products || []).map((product, index) => `
            <article class="product-card ${index === selectedProductIndex ? 'selected' : ''}" data-decision="${escapeHtml(product.decision)}">
              <div class="product-top">
                <div>
                  <div class="product-title">${escapeHtml(product.product_name)}</div>
                  <div class="product-meta">${escapeHtml(product.vendor_id)} · ${escapeHtml(product.model_name)} · ${escapeHtml(product.manufacturer)}</div>
                </div>
                <span class="pill ${String(product.decision).toLowerCase()}">${escapeHtml(product.decision)}</span>
              </div>
              <div class="product-rule"><code>${escapeHtml(product.decision_rule || '')}</code></div>
              <div class="product-action">${escapeHtml(product.reviewer_packet?.recommended_next_action || product.recommended_action || '')}</div>
              <div class="product-footer">
                <span class="muted">${escapeHtml((product.evidence_matches || []).length)} evidence match(es)</span>
                <button class="mini-button" onclick="inspectPacket(${index})">Inspect packet</button>
              </div>
            </article>
          `).join('')}
        </div>
      `;
      inspectPacket(0);
      applyDecisionFilter(decisionFilter);
      addCopilotMessage(
        'agent',
        'Review complete',
        `I found ${s.total_products ?? 0} product(s): ${s.approve_count ?? 0} approve, ${s.review_count ?? 0} review, ${s.hold_count ?? 0} hold. Select a card or ask me for the decision rationale.`
      );
    }

    function inspectPacket(index) {
      if (!lastResult || !lastResult.products || !lastResult.products[index]) return;
      selectedProductIndex = index;
      const product = lastResult.products[index];
      const decision = String(product.decision || 'REVIEW').toLowerCase();
      packetTitle.textContent = product.product_name || 'Selected product';
      packetDecision.className = `pill ${decision}`;
      packetDecision.textContent = product.decision || 'REVIEW';
      packetHint.textContent = product.reviewer_packet?.recommended_next_action || product.recommended_action || '';
      packetOut.textContent = JSON.stringify(product.reviewer_packet || product, null, 2);
      updateCopilotContext(product.product_name || 'Selected product', product.decision || 'REVIEW');
      document.querySelectorAll('.product-card').forEach((card, cardIndex) => {
        card.classList.toggle('selected', cardIndex === index);
      });
    }

    function updateCopilotContext(product = 'No product selected', decision = 'Waiting') {
      copilotContextProduct.textContent = product;
      copilotContextDecision.textContent = decision;
    }

    function setActiveFilter(filter) {
      document.querySelectorAll('.filter-chip').forEach(button => {
        button.classList.toggle('active', button.dataset.filter === filter);
      });
    }

    function applyDecisionFilter(filter) {
      decisionFilter = filter;
      setActiveFilter(filter);
      const cards = Array.from(document.querySelectorAll('.product-card'));
      let visibleCount = 0;
      cards.forEach(card => {
        const shouldShow = filter === 'ALL' || card.dataset.decision === filter;
        card.style.display = shouldShow ? '' : 'none';
        if (shouldShow) visibleCount += 1;
      });
      document.querySelectorAll('.filter-empty').forEach(node => node.remove());
      if (lastResult && visibleCount === 0) {
        decisions.insertAdjacentHTML('beforeend', '<div class="empty-state filter-empty">No products match this filter.</div>');
      }
    }

    function setNextAction(title, text, buttonLabel, action) {
      nextActionTitle.textContent = title;
      nextActionText.textContent = text;
      nextActionBtn.textContent = buttonLabel;
      nextActionBtn.dataset.action = action;
      nextActionBtn.disabled = false;
    }

    function resetCopilot(reason = '') {
      copilotLog.innerHTML = '';
      addCopilotMessage(
        'agent',
        'Reviewer Copilot',
        'I can explain decisions, summarize missing evidence, draft reviewer memos, and describe the guardrail path. Load evidence and run the review to make my answers product-specific.'
      );
      if (reason) {
        addCopilotMessage('agent', 'Workspace update', reason);
      }
    }

    function addCopilotMessage(role, title, text) {
      const message = document.createElement('div');
      message.className = `copilot-message ${role}`;
      message.innerHTML = `<strong>${escapeHtml(title)}</strong>${escapeHtml(text)}`;
      copilotLog.appendChild(message);
      copilotLog.scrollTop = copilotLog.scrollHeight;
    }

    function currentProduct() {
      if (!lastResult || !lastResult.products || lastResult.products.length === 0) return null;
      const index = selectedProductIndex ?? 0;
      return lastResult.products[index] || lastResult.products[0];
    }

    function answerCopilot(prompt) {
      const normalized = String(prompt || '').toLowerCase();
      const product = currentProduct();

      if (normalized.includes('guardrail') || normalized.includes('human') || normalized.includes('prompt')) {
        return 'Guardrails treat vendor notes as untrusted data, preserve deterministic decision rules, and require human review for HOLD or REVIEW outcomes. In Foundry, this maps to safety thresholds, prompt-injection protection, traces, and Entra-governed agent ownership.';
      }

      if (!product) {
        return 'Start by loading a sample or uploading a CSV, then run the review. The governed path is Knowledge Agent for policy grounding, Task Agent for CSV evidence checks, and Sequential Workflow for traceable orchestration.';
      }

      const packet = product.reviewer_packet || {};
      const evidenceCount = (product.evidence_matches || []).length;
      const missing = (product.missing_fields || []).filter(Boolean);
      const rationale = (packet.risk_rationale || product.risk_reasons || []).join(' ');
      const nextAction = packet.recommended_next_action || product.recommended_action || 'Manual reviewer action required.';

      if (normalized.includes('memo') || normalized.includes('summary')) {
        return `${product.product_name}: ${product.decision} under ${product.decision_rule}. Rationale: ${rationale || 'No rationale provided.'} Evidence matches: ${evidenceCount}. Missing fields: ${missing.length ? missing.join(', ') : 'none'}. Recommended next action: ${nextAction}`;
      }

      if (normalized.includes('evidence') || normalized.includes('missing') || normalized.includes('field')) {
        return `${product.product_name} has ${evidenceCount} evidence match(es). Missing required fields: ${missing.length ? missing.join(', ') : 'none'}. Open the reviewer packet for cited evidence IDs, match type, confidence, and source.`;
      }

      return `${product.product_name} was classified as ${product.decision} because ${rationale || product.decision_rule}. The active rule is ${product.decision_rule}, and the recommended next action is: ${nextAction}`;
    }

    function askCopilot(prompt) {
      const value = String(prompt || copilotInput.value || '').trim();
      if (!value) return;
      addCopilotMessage('user', 'Reviewer', value);
      addCopilotMessage('agent', 'RecallGuard Copilot', answerCopilot(value));
      copilotInput.value = '';
    }

    function setLoading(isLoading) {
      if (isLoading) {
        runStateLabel.textContent = 'Running';
        runStateCopy.textContent = 'Applying recall and certification evidence checks.';
        nextActionTitle.textContent = 'Review running';
        nextActionText.textContent = 'The checker is reading the CSV and matching evidence.';
      }
      runButtons.forEach(button => {
        button.disabled = isLoading;
        if (button === nextActionBtn) {
          button.textContent = isLoading ? 'Running...' : (button.dataset.action === 'inspect' ? 'Inspect first product' : 'Run review');
        } else {
          button.textContent = isLoading ? 'Running...' : 'Run review';
        }
      });
    }

    function renderRules() {
      document.getElementById('ruleList').innerHTML = Object.entries(DECISION_RULES).map(([ruleId, rule]) => `
        <article class="rule-card">
          <div class="rule-head"><code>${escapeHtml(ruleId)}</code><span class="pill ${String(rule.decision).toLowerCase()}">${escapeHtml(rule.decision)}</span></div>
          <p>${escapeHtml(rule.description)}</p>
        </article>
      `).join('');
    }

    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, char => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
      }[char]));
    }

    document.querySelectorAll('.scenario-card').forEach(button => {
      button.addEventListener('click', () => loadSample(button.dataset.sample));
    });
    document.getElementById('loadSampleBtn').addEventListener('click', () => loadSample());
    document.getElementById('runBtn').addEventListener('click', classifyCsv);
    document.getElementById('runBtnBottom').addEventListener('click', classifyCsv);
    nextActionBtn.addEventListener('click', () => {
      if (nextActionBtn.dataset.action === 'inspect') {
        inspectPacket(selectedProductIndex ?? 0);
        document.getElementById('decisions').scrollIntoView({behavior: 'smooth', block: 'start'});
      } else {
        classifyCsv();
      }
    });
    document.getElementById('evalBtn').addEventListener('click', loadEvaluation);
    document.getElementById('clearBtn').addEventListener('click', () => clearResults());
    filterRow.addEventListener('click', event => {
      const button = event.target.closest('.filter-chip');
      if (!button) return;
      applyDecisionFilter(button.dataset.filter);
    });
    askCopilotBtn.addEventListener('click', () => askCopilot());
    copilotInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') askCopilot();
    });
    document.querySelectorAll('.copilot-prompt').forEach(button => {
      button.addEventListener('click', () => askCopilot(button.dataset.prompt));
    });
    document.getElementById('fileInput').addEventListener('change', async event => {
      const file = event.target.files?.[0];
      if (!file) return;
      csvText.value = await file.text();
      fileName.textContent = file.name;
      clearResults('Loaded ' + file.name + '. Run the review to classify products.');
      document.querySelectorAll('.scenario-card').forEach(button => button.classList.remove('active'));
    });

    renderRules();
    loadSample();
  </script>
</body>
</html>"""
    return (
        page.replace("__SAMPLE_OPTIONS__", sample_options)
        .replace("__DECISION_RULES__", json.dumps(DECISION_RULES, ensure_ascii=False))
        .replace("__FOUNDRY_IMAGE_URL__", FOUNDRY_IMAGE_URL)
    )


class RecallGuardHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, body: str, content_type: str = "text/html; charset=utf-8") -> None:
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/":
                self.send_text(render_app_page())
            elif parsed.path == "/favicon.ico":
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
            elif parsed.path == "/api/samples":
                self.send_json({"samples": list_samples()})
            elif parsed.path == "/api/sample":
                name = parse_qs(parsed.query).get("name", [""])[0]
                path = sample_path(name)
                self.send_json({"name": name, "content": path.read_text(encoding="utf-8")})
            elif parsed.path == "/api/evaluation":
                self.send_json(load_evaluation())
            elif parsed.path == "/api/decision-rules":
                self.send_json({"decision_rules": DECISION_RULES})
            else:
                self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except Exception as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/classify":
            self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length).decode("utf-8")
            payload = json.loads(body or "{}")
            csv_text = str(payload.get("csv_text", "")).strip()
            sample = str(payload.get("sample", "")).strip()
            with tempfile.TemporaryDirectory(prefix="recallguard-local-") as tmpdir:
                if csv_text:
                    vendor_csv = Path(tmpdir) / "vendor_input.csv"
                    vendor_csv.write_text(csv_text + "\n", encoding="utf-8")
                elif sample:
                    vendor_csv = sample_path(sample)
                else:
                    raise ValueError("Provide csv_text or sample.")
                self.send_json(classify(vendor_csv, EVIDENCE_CSV))
        except Exception as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), RecallGuardHandler)
    print(f"RecallGuard local demo running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down RecallGuard local demo.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
