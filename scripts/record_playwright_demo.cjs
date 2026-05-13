#!/usr/bin/env node

const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const FINAL_DIR = path.join(ROOT, "final");
const ASSET_DIR = path.join(FINAL_DIR, "playwright_demo_assets");
const RUNTIME_DIR = path.join(ROOT, ".playwright-runtime");
const OUTPUT_MP4 = path.join(FINAL_DIR, "RecallGuard_AI_Playwright_Demo_Somi.mp4");
const HTML_PATH = path.join(ASSET_DIR, "recallguard_playwright_demo.html");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function extractOutputText(responseJson) {
  const parts = [];
  for (const item of responseJson.output || []) {
    if (item.type !== "message") continue;
    for (const content of item.content || []) {
      if (content.type === "output_text") parts.push(content.text || "");
    }
  }
  return parts.join("\n").trim();
}

function ensurePlaywright() {
  const modulePath = path.join(RUNTIME_DIR, "node_modules", "playwright");
  if (!fs.existsSync(modulePath)) {
    fs.mkdirSync(RUNTIME_DIR, { recursive: true });
    execFileSync("npm", ["install", "--prefix", RUNTIME_DIR, "playwright"], {
      cwd: ROOT,
      stdio: "inherit",
    });
  }
  return require(modulePath);
}

function buildHtml() {
  const implementation = readJson("outputs/foundry_live_implementation_summary_public_data.json");
  const liveSummary = readJson("outputs/live-runs/live_demo_summary.json");
  const publicRecall = readJson("outputs/live-runs/task_v6_public_recall_response.json");
  const publicRecallText = extractOutputText(publicRecall);

  const publicRun = liveSummary.task_public_recall || {};
  const workflowRun = liveSummary.workflow_v4_recall || {};
  const taskAgent = implementation.task_agent_public_data || {};
  const workflowAgent = implementation.workflow_agent_public_data || {};

  const evidenceJson = publicRecallText.match(/```json\n([\s\S]*?)```/)?.[1] || publicRecallText;
  const parsedEvidence = JSON.parse(evidenceJson);
  const holdProduct = parsedEvidence.products.find((product) => product.decision === "HOLD");
  const holdEvidence = holdProduct.evidence_matches[0];

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>RecallGuard AI Playwright Demo</title>
  <style>
    :root {
      --ink: #000000;
      --body: #747474;
      --canvas: #ffffff;
      --hairline: #ebebeb;
      --dark: #010120;
      --dark-soft: #313641;
      --mint: #c8f6f9;
      --orange: #fc4c02;
      --magenta: #ef2cc1;
      --periwinkle: #bdbbff;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background: var(--canvas);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }
    section {
      min-height: 720px;
      display: grid;
      align-items: center;
      padding: 78px 72px;
      overflow: hidden;
    }
    .dark { background: var(--dark); color: white; }
    .wrap { width: min(1140px, 100%); margin: 0 auto; }
    .eyebrow {
      font-family: "JetBrains Mono", "SFMono-Regular", ui-monospace, monospace;
      font-size: 12px;
      line-height: 1;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--body);
      margin-bottom: 22px;
      font-weight: 600;
    }
    .dark .eyebrow { color: #bfc3d1; }
    h1, h2 {
      margin: 0;
      font-weight: 500;
      letter-spacing: 0;
    }
    h1 {
      max-width: 760px;
      font-size: 64px;
      line-height: 1.06;
    }
    h2 {
      max-width: 870px;
      font-size: 46px;
      line-height: 1.12;
    }
    p {
      max-width: 720px;
      color: var(--body);
      font-size: 20px;
      line-height: 1.45;
    }
    .dark p { color: #d9dbea; }
    .hero-grid {
      display: grid;
      grid-template-columns: 1.04fr .96fr;
      gap: 64px;
      align-items: center;
    }
    .ribbon {
      height: 430px;
      position: relative;
      filter: saturate(1.08);
    }
    .ribbon::before,
    .ribbon::after {
      content: "";
      position: absolute;
      inset: 36px 6px;
      border-radius: 40% 60% 35% 65%;
      background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,.25), transparent 22%),
        linear-gradient(115deg, var(--orange), var(--magenta) 48%, var(--periwinkle));
      transform: rotate(-16deg) skew(-8deg);
    }
    .ribbon::after {
      inset: 116px 34px 44px 62px;
      opacity: .64;
      transform: rotate(12deg) skew(12deg);
      filter: blur(.2px);
    }
    .button-row { display: flex; gap: 12px; margin-top: 34px; }
    .button {
      border-radius: 4px;
      padding: 13px 22px;
      font-family: "JetBrains Mono", "SFMono-Regular", ui-monospace, monospace;
      font-size: 14px;
      letter-spacing: .06em;
      text-transform: uppercase;
      font-weight: 600;
      border: 1px solid transparent;
      color: var(--ink);
      background: var(--mint);
    }
    .button.black { background: white; color: var(--ink); }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
      margin-top: 42px;
    }
    .card {
      border: 1px solid var(--hairline);
      border-radius: 4px;
      padding: 24px;
      min-height: 196px;
      background: white;
    }
    .dark .card {
      background: var(--dark);
      border-color: var(--dark-soft);
      color: white;
    }
    .card strong {
      display: block;
      font-size: 25px;
      line-height: 1.14;
      font-weight: 500;
      margin-bottom: 16px;
    }
    .card span {
      color: var(--body);
      font-size: 16px;
      line-height: 1.4;
    }
    .dark .card span { color: #c8ccdc; }
    .data-strip {
      display: grid;
      grid-template-columns: .88fr 1.12fr;
      gap: 28px;
      margin-top: 42px;
    }
    .stat {
      background: var(--mint);
      border-radius: 4px;
      padding: 30px;
    }
    .stat b {
      display: block;
      font-size: 58px;
      line-height: 1;
      font-weight: 500;
      margin-bottom: 14px;
    }
    .table {
      border: 1px solid var(--hairline);
      border-radius: 4px;
      overflow: hidden;
      background: white;
    }
    .row {
      display: grid;
      grid-template-columns: 1fr 1.25fr;
      gap: 16px;
      padding: 15px 18px;
      border-top: 1px solid var(--hairline);
      font-size: 15px;
    }
    .row:first-child {
      border-top: 0;
      background: var(--hairline);
      font-family: "JetBrains Mono", "SFMono-Regular", ui-monospace, monospace;
      text-transform: uppercase;
      letter-spacing: .06em;
      color: var(--body);
      font-weight: 600;
    }
    .trace {
      margin-top: 40px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }
    .step {
      border: 1px solid var(--dark-soft);
      border-radius: 4px;
      padding: 20px;
      min-height: 130px;
    }
    .step b { display: block; font-size: 18px; margin-bottom: 14px; }
    .step small {
      color: #c8ccdc;
      font-family: "JetBrains Mono", "SFMono-Regular", ui-monospace, monospace;
      text-transform: uppercase;
      letter-spacing: .04em;
    }
    .decision {
      display: grid;
      grid-template-columns: .72fr 1.28fr;
      gap: 28px;
      align-items: stretch;
      margin-top: 38px;
    }
    .hold {
      background: linear-gradient(135deg, var(--orange), var(--magenta) 54%, var(--periwinkle));
      color: white;
      border-radius: 4px;
      padding: 34px;
    }
    .hold b {
      display: block;
      font-size: 76px;
      line-height: 1;
      font-weight: 500;
      margin-bottom: 24px;
    }
    pre {
      margin: 0;
      background: var(--dark);
      color: white;
      border-radius: 4px;
      padding: 24px;
      max-height: 370px;
      overflow: hidden;
      font-size: 14px;
      line-height: 1.46;
      white-space: pre-wrap;
      font-family: "JetBrains Mono", "SFMono-Regular", ui-monospace, monospace;
    }
    .footer-word {
      font-size: 92px;
      line-height: 1;
      color: var(--hairline);
      font-weight: 500;
      margin-top: 68px;
    }
  </style>
</head>
<body>
  <section class="dark" id="hero">
    <div class="wrap hero-grid">
      <div>
        <div class="eyebrow">Microsoft Foundry live demo</div>
        <h1>RecallGuard AI blocks recalled products before listing.</h1>
        <p>Automated with Playwright from live Foundry run artifacts: Knowledge Agent, Code Interpreter Task Agent, Sequential Workflow, guardrails, traces, and Entra Agent ID governance.</p>
        <div class="button-row">
          <div class="button">KATS public data</div>
          <div class="button black">Foundry workflow</div>
        </div>
      </div>
      <div class="ribbon" aria-hidden="true"></div>
    </div>
  </section>

  <section id="architecture">
    <div class="wrap">
      <div class="eyebrow">01 / multi-agent system</div>
      <h2>Knowledge first, then deterministic evidence checking.</h2>
      <p>The workflow grounds review criteria before invoking the task agent. The task agent uses Code Interpreter and a script, not vibes, to classify vendor products.</p>
      <div class="grid">
        <div class="card"><strong>Knowledge Agent</strong><span>File Search over product safety SOP, KC checklist, recall policy, and vendor requirements.</span></div>
        <div class="card"><strong>Task Agent</strong><span>${escapeHtml(taskAgent.name)} with Code Interpreter and recallguard_checker.py.</span></div>
        <div class="card"><strong>Workflow</strong><span>${escapeHtml(workflowAgent.name)} invokes policy grounding first, then evidence checks.</span></div>
      </div>
    </div>
  </section>

  <section id="dataset">
    <div class="wrap">
      <div class="eyebrow">02 / public data grounding</div>
      <h2>Real Korea Data Portal recall evidence, normalized for the task agent.</h2>
      <div class="data-strip">
        <div class="stat"><b>881</b><span>Rows downloaded from the KATS domestic product safety recall CSV and normalized to UTF-8.</span></div>
        <div class="table">
          <div class="row"><div>Field</div><div>Value</div></div>
          <div class="row"><div>Dataset</div><div>산업통상부_국가기술표준원_제품안전_국내리콜정보</div></div>
          <div class="row"><div>Source</div><div>data.go.kr / Korean Agency for Technology and Standards</div></div>
          <div class="row"><div>Evidence file</div><div>recall_certification_snapshot.csv + KATS-RECALL rows</div></div>
        </div>
      </div>
    </div>
  </section>

  <section class="dark" id="trace">
    <div class="wrap">
      <div class="eyebrow">03 / live Foundry trace evidence</div>
      <h2>Responses API completed the full governed workflow.</h2>
      <p>These output types are from the live run summary saved after invoking the Foundry agents.</p>
      <div class="trace">
        <div class="step"><b>Knowledge</b><small>${escapeHtml((liveSummary.knowledge.output_types || []).join(" -> "))}</small></div>
        <div class="step"><b>Task public recall</b><small>${escapeHtml((publicRun.output_types || []).join(" -> "))}</small></div>
        <div class="step"><b>Workflow recall</b><small>${escapeHtml((workflowRun.output_types || []).join(" -> "))}</small></div>
        <div class="step"><b>Status</b><small>all completed</small></div>
      </div>
    </div>
  </section>

  <section id="decision">
    <div class="wrap">
      <div class="eyebrow">04 / concrete action</div>
      <h2>The public KATS recall row creates a HOLD decision.</h2>
      <div class="decision">
        <div class="hold">
          <b>HOLD</b>
          <div>${escapeHtml(holdProduct.product_name)} / ${escapeHtml(holdProduct.model_name)}</div>
          <p style="color:white;margin-top:18px;">Evidence: ${escapeHtml(holdEvidence.evidence_id)} · ${escapeHtml(holdEvidence.recall_reason)}</p>
        </div>
        <pre>${escapeHtml(JSON.stringify({
  summary: parsedEvidence.summary,
  hold_product: {
    product_name: holdProduct.product_name,
    model_name: holdProduct.model_name,
    manufacturer: holdProduct.manufacturer,
    evidence_id: holdEvidence.evidence_id,
    source: holdEvidence.source,
    recommended_action: holdProduct.recommended_action,
  },
}, null, 2))}</pre>
      </div>
    </div>
  </section>

  <section class="dark" id="governance">
    <div class="wrap">
      <div class="eyebrow">05 / governed AI</div>
      <h2>Guardrails, HITL, and Entra Agent IDs keep this from becoming blind automation.</h2>
      <div class="grid">
        <div class="card"><strong>Prompt injection</strong><span>Vendor notes are treated as untrusted data and never as instructions.</span></div>
        <div class="card"><strong>Human-in-the-loop</strong><span>Any HOLD decision must be escalated to a compliance owner before listing.</span></div>
        <div class="card"><strong>Identity governance</strong><span>Task principal ${escapeHtml(taskAgent.principal_id)}. Workflow principal ${escapeHtml(workflowAgent.principal_id)}.</span></div>
      </div>
      <div class="footer-word">RecallGuard AI</div>
    </div>
  </section>
</body>
</html>`;
}

async function main() {
  fs.mkdirSync(ASSET_DIR, { recursive: true });
  fs.writeFileSync(HTML_PATH, buildHtml(), "utf8");

  const { chromium } = ensurePlaywright();
  const videoDir = path.join(ASSET_DIR, "video");
  fs.rmSync(videoDir, { recursive: true, force: true });
  fs.mkdirSync(videoDir, { recursive: true });

  let browser;
  try {
    browser = await chromium.launch({ channel: "chrome", headless: true });
  } catch {
    const playwrightBin = path.join(RUNTIME_DIR, "node_modules", ".bin", "playwright");
    execFileSync(playwrightBin, ["install", "chromium"], { cwd: ROOT, stdio: "inherit" });
    browser = await chromium.launch({ headless: true });
  }
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: { dir: videoDir, size: { width: 1280, height: 720 } },
  });
  const page = await context.newPage();
  await page.goto(`file://${HTML_PATH}`);
  await page.waitForTimeout(1600);

  for (const id of ["architecture", "dataset", "trace", "decision", "governance"]) {
    await page.evaluate((targetId) => {
      document.getElementById(targetId).scrollIntoView({ behavior: "smooth", block: "start" });
    }, id);
    await page.waitForTimeout(7000);
  }

  await page.waitForTimeout(1200);
  await context.close();
  await browser.close();

  const webm = fs.readdirSync(videoDir).find((file) => file.endsWith(".webm"));
  if (!webm) throw new Error("Playwright did not produce a WebM recording.");
  const inputWebm = path.join(videoDir, webm);

  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-i",
      inputWebm,
      "-c:v",
      "libx264",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      OUTPUT_MP4,
    ],
    { stdio: "inherit" },
  );

  console.log(JSON.stringify({ html: HTML_PATH, mp4: OUTPUT_MP4 }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
