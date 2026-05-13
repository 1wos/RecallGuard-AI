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
                self.send_text(render_page())
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
