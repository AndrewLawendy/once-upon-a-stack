#!/usr/bin/env node
// Headless visual check of a built book, in light and dark, at laptop size.
// Usage: node check.mjs "<library>/<slug>--<topic>"
//        node check.mjs --preflight   (only confirms Node and a browser work, before any book exists)
// Writes screenshots to .source/check/, prints problems, exits 1 if there are any.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync, existsSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const arg = process.argv[2];
const preflight = arg === '--preflight';
if (!arg) { console.error('Usage: node check.mjs "<library>/<slug>--<topic>" or node check.mjs --preflight'); process.exit(2); }
const folder = preflight ? '' : resolve(arg.replace(/^~/, homedir()));
const file = join(folder, 'index.html');
const outDir = join(folder, '.source', 'check');
if (!preflight) {
  if (!existsSync(file)) { console.error(`No built book at ${file}`); process.exit(2); }
  rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });
}

const WIDTH = 1366, HEIGHT = 768;
// Any Chromium-based browser works (Chrome, Chromium, Edge, Brave). CHROME_PATH wins when set.
const env = process.env;
const winRoots = [env.PROGRAMFILES, env['PROGRAMFILES(X86)'], env.LOCALAPPDATA].filter(Boolean);
const CHROME = [
  env.CHROME_PATH,
  ...{
    darwin: ['Google Chrome', 'Chromium', 'Microsoft Edge', 'Brave Browser'].map((app) => `/Applications/${app}.app/Contents/MacOS/${app}`),
    win32: winRoots.flatMap((root) => [
      join(root, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      join(root, 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
      join(root, 'BraveSoftware', 'Brave-Browser', 'Application', 'brave.exe'),
    ]),
  }[process.platform] ?? [],
  'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'microsoft-edge', 'brave-browser',
].filter((p) => p && (!p.includes('/') && !p.includes('\\') || existsSync(p)));
if (typeof WebSocket === 'undefined') { console.error(`This check needs Node.js 22 or newer (it uses the built-in WebSocket). This is Node ${process.versions.node}: install Node.js 22 or newer.`); process.exit(2); }
const profile = mkdtempSync(join(tmpdir(), 'once-upon-a-stack-check-'));

function launch(names) {
  return new Promise((ok, fail) => {
    const [name, ...rest] = names;
    if (!name) return fail(new Error('No Chrome, Chromium, Edge or Brave found. Install one, or set CHROME_PATH to its executable.'));
    const proc = spawn(name, ['--headless=new', '--disable-gpu', '--no-first-run', '--remote-debugging-port=0',
      `--user-data-dir=${profile}`, 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
    let log = '';
    proc.on('error', () => launch(rest).then(ok, fail));
    proc.stderr.on('data', (chunk) => {
      log += chunk;
      const found = log.match(/DevTools listening on (\S+)/);
      if (found) ok({ proc, url: found[1], name });
    });
  });
}

function connect(url) {
  return new Promise((ok, fail) => {
    const ws = new WebSocket(url);
    let id = 0;
    const waiting = new Map(), listeners = [];
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && waiting.has(msg.id)) {
        const { res, rej } = waiting.get(msg.id);
        waiting.delete(msg.id);
        msg.error ? rej(new Error(msg.error.message)) : res(msg.result);
      } else listeners.forEach((fn) => fn(msg));
    };
    ws.onerror = fail;
    ws.onopen = () => ok({
      send: (method, params = {}, sessionId) => new Promise((res, rej) => {
        waiting.set(++id, { res, rej });
        ws.send(JSON.stringify({ id, method, params, sessionId }));
      }),
      listen: (fn) => listeners.push(fn),
      close: () => ws.close(),
    });
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Runs in the page: measures what's wrong with the current page.
const MEASURE = `(() => {
  const page = document.querySelector('.page.active');
  const out = [];
  const scroller = page.querySelector('.scroller');
  if (scroller && scroller.scrollHeight - scroller.clientHeight > 2)
    out.push('content needs scrolling by ' + (scroller.scrollHeight - scroller.clientHeight) + 'px at laptop size');
  if (scroller && scroller.scrollWidth - scroller.clientWidth > 2) out.push('content overflows sideways');
  page.querySelectorAll('svg').forEach((svg) => {
    if (svg.closest('.with')) return;
    const box = svg.getBoundingClientRect();
    if (!box.width) return;
    const tags = [...svg.querySelectorAll('.ntag')].filter((t) => getComputedStyle(t).opacity !== '0');
    const rects = tags.map((t) => ({ name: t.querySelector('.nt-n').textContent, rect: t.querySelector('rect').getBoundingClientRect(), text: [...t.querySelectorAll('text')].map((x) => x.getBoundingClientRect()) }));
    rects.forEach((a, i) => {
      a.text.forEach((tb) => { if (tb.width > a.rect.width + 1) out.push('text overflows name tag: ' + a.name); });
      if (a.rect.left < box.left - 1 || a.rect.right > box.right + 1 || a.rect.top < box.top - 1) out.push('name tag leaves the scene: ' + a.name);
      rects.slice(i + 1).forEach((b) => {
        const hit = a.rect.left < b.rect.right && b.rect.left < a.rect.right && a.rect.top < b.rect.bottom && b.rect.top < a.rect.bottom;
        if (hit) out.push('name tags overlap: ' + a.name + ' and ' + b.name);
      });
    });
  });
  // Hard-to-read text: WCAG contrast of each text element against its nearest solid background.
  const rgb = (c) => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const lum = ([r, g, b]) => [r, g, b].map((v) => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((t, v, i) => t + v * [.2126, .7152, .0722][i], 0);
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
  const backing = (el) => { for (let n = el; n; n = n.parentElement) { const s = getComputedStyle(n); if (s.backgroundImage !== 'none' && !n.classList.contains('page')) return null; const c = rgb(s.backgroundColor); if (c && (c[3] === undefined || c[3] > .9)) return c; } return null; };
  const low = new Set();
  [...page.querySelectorAll('h1,h2,h3,p,li,dt,dd,a,span,button,summary')].concat([...document.querySelectorAll('.nav button,.nav select')]).forEach((el) => {
    if (!el.getClientRects().length || el.closest('.note-src,svg,.compare input') || !(el.innerText || '').trim()) return;
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && el.tagName !== 'SELECT') return;
    const s = getComputedStyle(el), fg = rgb(s.color), bg = backing(el);
    if (!fg || !bg) return;
    const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.6 && +s.fontWeight >= 700);
    const r = ratio(fg, bg);
    if (r < (big ? 3 : 4.5)) low.add('hard-to-read text (' + r.toFixed(1) + ':1): ' + (el.innerText || '').trim().slice(0, 40));
  });
  page.querySelectorAll('.ntag').forEach((t) => {
    const fg = rgb(getComputedStyle(t.querySelector('text')).fill), bg = rgb(getComputedStyle(t.querySelector('rect')).fill);
    if (fg && bg && ratio(fg, bg) < 4.5) low.add('hard-to-read name tag: ' + t.querySelector('.nt-n').textContent);
  });
  out.push(...low);
  const hasNotes = !!page.querySelector('.note-src');
  const isPlain = page.classList.contains('plain');
  if (!hasNotes && !isPlain) out.push('story page has no For grown-ups notes');
  return JSON.stringify({ problems: out, hasNotes, plays: page.querySelectorAll('button[data-play]').length, steps: page.querySelectorAll('.journey .steps li').length });
})()`;

if (preflight) {
  try {
    const found = await launch(CHROME);
    console.log(`Ready: Node ${process.versions.node}, browser ${found.name}`);
    found.proc.kill();
  } catch (err) {
    console.error(`Not ready: ${err.message}`);
    process.exitCode = 2;
  }
  await sleep(200);
  rmSync(profile, { recursive: true, force: true });
  process.exit();
}

const report = [];
let chrome;
try {
  chrome = await launch(CHROME);
  const browser = await connect(chrome.url);
  const { targetId } = await browser.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await browser.send('Target.attachToTarget', { targetId, flatten: true });
  const send = (m, p) => browser.send(m, p, sessionId);
  const evaluate = async (expression) => (await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result?.value;
  const shot = async (name) => {
    const { data } = await send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(join(outDir, name), Buffer.from(data, 'base64'));
  };

  let label = 'load';
  browser.listen((msg) => {
    if (msg.method === 'Runtime.exceptionThrown') {
      const d = msg.params.exceptionDetails;
      report.push(`${label}: script error: ${d.exception?.description || d.text}`);
    }
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      report.push(`${label}: console error: ${msg.params.args.map((a) => a.value ?? a.description).join(' ')}`);
    }
    if (msg.method === 'Log.entryAdded' && msg.params.entry.level === 'error') {
      report.push(`${label}: ${msg.params.entry.text}`);
    }
  });
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: WIDTH, height: HEIGHT, deviceScaleFactor: 1, mobile: false });

  let total = 0;
  for (const theme of ['light', 'dark']) {
    // Reduced motion lets every scene settle at its final state for the screenshot.
    await send('Emulation.setEmulatedMedia', { features: [
      { name: 'prefers-color-scheme', value: theme },
      { name: 'prefers-reduced-motion', value: 'reduce' },
    ] });
    await send('Page.navigate', { url: `${pathToFileURL(file).href}#1` });
    await sleep(800);
    await evaluate(`localStorage.clear()`);
    total = await evaluate('window.__book.count');
    if (!total) throw new Error('window.__book is missing: the shell script did not start');
    for (let i = 0; i < total; i++) {
      const n = String(i + 1).padStart(2, '0');
      label = `${theme} page ${i + 1}`;
      await evaluate(`window.__book.go(${i})`);
      await sleep(250);
      const measured = JSON.parse(await evaluate(MEASURE));
      measured.problems.forEach((p) => report.push(`${label}: ${p}`));
      await shot(`${theme}-${n}.png`);
      if (measured.hasNotes) {
        await evaluate('window.__book.setNotesOpen(true)');
        await sleep(100);
        await shot(`${theme}-${n}-notes.png`);
        await evaluate('window.__book.setNotesOpen(false)');
      }
      if (measured.steps > 1) {
        for (let s = 1; s < measured.steps; s++) await evaluate(`document.querySelector('.page.active .journey-controls [data-step="1"]').click()`);
        await sleep(150);
        await shot(`${theme}-${n}-last-step.png`);
      }
      for (let b = 0; b < measured.plays; b++) {
        await evaluate(`document.querySelectorAll('.page.active button[data-play]')[${b}].click()`);
        await sleep(1200);
        await shot(`${theme}-${n}-play-${b + 1}.png`);
      }
    }
  }
  browser.close();
  const unique = [...new Set(report)];
  console.log(`Checked ${total} pages in light and dark at ${WIDTH}x${HEIGHT}. Screenshots: ${outDir}`);
  if (unique.length) {
    console.log(`${unique.length} problem(s):`);
    unique.forEach((p) => console.log(`- ${p}`));
    process.exitCode = 1;
  } else {
    console.log('No automatic problems. Automatic checks can\'t judge the art, so look at the screenshots.');
  }
} catch (err) {
  console.error(`Check could not finish: ${err.message}`);
  process.exitCode = 2;
} finally {
  chrome?.proc.kill();
  await sleep(200);
  rmSync(profile, { recursive: true, force: true });
}
