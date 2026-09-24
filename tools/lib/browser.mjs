import { chromium, firefox } from 'playwright-core';
import path from 'node:path';
import url from 'node:url';

export const ENGINES = { chromium, firefox };

export async function launch(engine = 'chromium') {
  const type = ENGINES[engine];
  if (!type) throw new Error(`unknown engine "${engine}" (use: ${Object.keys(ENGINES).join(', ')})`);
  try {
    return await type.launch();
  } catch (e) {
    if (/Executable doesn't exist/.test(e.message)) {
      throw new Error(`${engine} is not installed for playwright-core; run \`npm run setup\` in tools/`);
    }
    throw e;
  }
}

/**
 * Open a film and wait for its bake to finish.
 * The film must expose window.__riso = { duration, ready, seek(t) }.
 */
export async function openFilm(browser, filmPath, { size = 1080, css = 720, query = '', timeout = 180000 } = {}) {
  // The film styles its canvas at `css` px but renders a larger backing store.
  // Screenshotting at CSS size would downscale it and destroy the halftone dots,
  // so scale the viewport up to capture the backing store 1:1.
  const page = await browser.newPage({
    viewport: { width: css, height: css },
    deviceScaleFactor: size / css,
  });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  // A deliverable makes no network calls. Abort instead of allowing, so every tool renders
  // what an offline viewer sees and reports the request as a page error.
  await page.route(u => !/^(file|data|blob|about):/.test(u.href), r => {
    errors.push(`network request blocked: ${r.request().url()}`);
    return r.abort();
  });

  const href = url.pathToFileURL(path.resolve(filmPath)).href + (query ? '?' + query : '');
  await page.goto(href, { waitUntil: 'load' });
  await page.waitForFunction(
    () => window.__riso && window.__riso.ready === true,
    null,
    { timeout },
  ).catch(() => {
    const hint = errors.length ? `\n  page errors:\n   - ${errors.join('\n   - ')}` : '';
    throw new Error(`film never reported window.__riso.ready within ${timeout}ms${hint}`);
  });

  const duration = await page.evaluate(() => window.__riso.duration);
  return { page, duration, errors };
}

/** Render one exact frame and return its PNG buffer. */
export async function frameAt(page, t) {
  await page.evaluate(time => window.__riso.seek(time), t);
  return page.screenshot({ type: 'png' });
}

/** Parse --range a:b:step or --times a,b,c into a sorted time list. */
export function parseTimes({ range, times }, duration) {
  if (times) return times.split(',').map(Number).filter(n => !Number.isNaN(n));
  if (range) {
    const [a, b, step = 0.25] = range.split(':').map(Number);
    const out = [];
    for (let t = a; t <= b + 1e-9; t += step) out.push(Number(t.toFixed(4)));
    return out;
  }
  const out = [];
  for (let t = 0; t < duration; t += 1) out.push(t);
  return out;
}

/** Minimal --flag value / --flag=value parser. */
export function args(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) { out._.push(a); continue; }
    const eq = a.indexOf('=');
    if (eq > -1) out[a.slice(2, eq)] = a.slice(eq + 1);
    else if (argv[i + 1] && !argv[i + 1].startsWith('--')) out[a.slice(2)] = argv[++i];
    else out[a.slice(2)] = true;
  }
  return out;
}
