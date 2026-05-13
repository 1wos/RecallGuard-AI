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
        <tr>
          <td><code>{html.escape(rule_id)}</code></td>
          <td><span class="pill {rule['decision'].lower()}">{rule['decision']}</span></td>
          <td>{html.escape(rule['description'])}</td>
          <td>{'Yes' if rule['human_review_required'] else 'No'}</td>
        </tr>
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
    .grid {{ display: grid; grid-template-columns: minmax(0, 1.08fr) minmax(320px, .92fr); gap: 20px; align-items: start; }}
    .panel {{
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 20px;
      background: white;
    }}
    .panel.soft {{ background: var(--soft); }}
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
    textarea {{ min-height: 180px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 12px; }}
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
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ text-align: left; border-bottom: 1px solid var(--line); padding: 10px 8px; vertical-align: top; }}
    th {{ background: #ebebeb; color: var(--muted); font-family: "SFMono-Regular", Consolas, monospace; text-transform: uppercase; font-size: 10px; letter-spacing: .08em; }}
    code, pre {{ font-family: "SFMono-Regular", Consolas, monospace; }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: #0d0d1f; color: #f8f8ff; border-radius: 4px; padding: 14px; max-height: 380px; overflow: auto; font-size: 12px; }}
    .pill {{ display: inline-block; border-radius: 4px; padding: 3px 8px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; }}
    .approve {{ background: #dff7e8; }}
    .review {{ background: #fff0c2; }}
    .hold {{ background: #ffd9d2; }}
    .metric {{ background: white; border: 1px solid var(--line); border-radius: 4px; padding: 12px; min-width: 120px; }}
    .metric strong {{ display: block; font-size: 24px; letter-spacing: -.02em; }}
    .muted {{ color: var(--muted); }}
    @media (max-width: 880px) {{ .grid {{ grid-template-columns: 1fr; }} header::after {{ opacity: .28; }} }}
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
    <div class="wrap grid">
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
        <h3>Decision table</h3>
        <table>
          <thead><tr><th>Rule</th><th>Decision</th><th>Trigger</th><th>Review</th></tr></thead>
          <tbody>{decision_rows}</tbody>
        </table>
      </aside>
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
        <table>
          <thead><tr><th>Vendor</th><th>Product</th><th>Decision</th><th>Rule</th><th>Next action</th></tr></thead>
          <tbody>
            ${{(data.products || []).map(product => `
              <tr>
                <td>${{escapeHtml(product.vendor_id)}}</td>
                <td>${{escapeHtml(product.product_name)}}<br><span class="muted">${{escapeHtml(product.model_name)}} / ${{escapeHtml(product.manufacturer)}}</span></td>
                <td><span class="pill ${{String(product.decision).toLowerCase()}}">${{escapeHtml(product.decision)}}</span></td>
                <td><code>${{escapeHtml(product.decision_rule || '')}}</code></td>
                <td>${{escapeHtml(product.reviewer_packet?.recommended_next_action || product.recommended_action || '')}}</td>
              </tr>
            `).join('')}}
          </tbody>
        </table>
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
