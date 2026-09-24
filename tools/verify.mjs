/**
 * Gate the film contract. Everything downstream assumes these hold.
 *
 *   node verify.mjs <film.html> [--times 0.3,1.8,3.0]
 *
 * Samples repeatability on consecutive and reordered seeks, and against a fresh page drawn in
 * reverse, in both browsers. On failure, names what poisons the first failing time.
 * Reports cross-engine hashes; antialiasing differences are not failures.
 * This does not prove continuity, absence of time-seeded crawl, or artistic quality;
 * `review.mjs --mp4` measures stillness.
 */
import crypto from 'node:crypto';
import { launch, openFilm, frameAt, args } from './lib/browser.mjs';

const a = args(process.argv.slice(2));
const film = a._[0];
if (!film) { console.error('usage: node verify.mjs <film.html> [--times ...]'); process.exit(1); }
const explicitTimes = a.times ? a.times.split(',').map(Number) : null;
const size = Number(a.size || 1080);
const sum = (b) => crypto.createHash('sha256').update(b).digest('hex').slice(0, 12);

let failures = 0;
const fail = (m) => { failures++; console.log(`  FAIL ${m}`); };

/** Hashes of `ts` drawn in order on a newly loaded page, with no state left by earlier seeks. */
async function drawFresh(browser, ts) {
  const { page } = await openFilm(browser, film, { size });
  try {
    const out = [];
    for (const t of ts) out.push(sum(await frameAt(page, t)));
    return out;
  } finally { await page.close(); }
}

/**
 * Name the cause of a failing time. Drawing t twice on a fresh page isolates state that advances
 * per seek. Drawing one candidate before t, each on its own fresh page, finds the frame whose
 * drawing changes t: a cache filled by whichever frame came first. Stops at the first culprit,
 * since each candidate costs a page load and bake.
 */
async function diagnose(browser, t, candidates) {
  const [cold, again] = await drawFresh(browser, [t, t]);
  if (again !== cold)
    return `t=${t} changes when drawn twice on a fresh page: something advances per seek (a counter, an undrawn canvas, an rng not re-seeded from its key)`;
  for (const p of candidates) {
    if (p !== t && (await drawFresh(browser, [p, t]))[1] !== cold)
      return `t=${t} changes when t=${p} is drawn first: a cache or variable written at ${p} is read at ${t}; a cache key must name everything its pixels depend on`;
  }
  return `t=${t} matches its fresh-page draw after each single candidate; the failure needs a longer seek history`;
}

const chromeHashes = {};
for (const engine of ['chromium', 'firefox']) {
  const browser = await launch(engine);
  const { page, duration, errors } = await openFilm(browser, film, { size });
  if (!(duration > 0 && Number.isFinite(duration))) throw Error('duration must be finite and positive');
  const shotTimes = await page.evaluate(() => (window.__riso.shots || []).flatMap(s =>
    [s.start, s.readAt, s.end - 1/30]).filter(Number.isFinite));
  // Cover the actual duration: the old defaults silently stopped at 27 seconds.
  const times = explicitTimes || [...new Set([
    ...[0,.07,.2,.4,.6,.8,1].map(u => Math.min(duration-1/30, u*duration)),
    ...shotTimes,
  ].map(t => Number(Math.max(0,t).toFixed(6))))].sort((x,y)=>x-y);
  if (times.some(t => !Number.isFinite(t) || t<0 || t>duration))
    throw Error(`Inspection times must be within 0..${duration}`);
  console.log(`${engine}: duration ${duration}s`);
  if (errors.length) fail(`${errors.length} page error(s): ${errors[0]}`);

  const base = {}, bad = [];
  const failAt = (t, m) => { fail(m); if (!bad.includes(t)) bad.push(t); };
  const wander = (t) => [(t + 9.3) % duration, (t + 17.1) % duration];
  for (const t of times) {
    base[t] = sum(await frameAt(page, t));
    // Consecutive repeats catch short state cycles that a whole-list repeat can alias.
    if (sum(await frameAt(page, t)) !== base[t]) failAt(t, `t=${t} not repeatable on consecutive seeks`);
  }

  for (const t of times) {                       // repeat seek
    if (sum(await frameAt(page, t)) !== base[t]) failAt(t, `t=${t} not repeatable`);
  }
  for (const t of times) {                       // cold jump after wandering
    for (const w of wander(t)) await frameAt(page, w);
    if (sum(await frameAt(page, t)) !== base[t]) failAt(t, `t=${t} depends on seek history`);
  }
  // Within one page, a cache filled by the first frame drawn agrees with itself forever.
  // A new page drawn in reverse order fills it from the other end.
  const reversed = [...times].reverse(), fresh = await drawFresh(browser, reversed);
  reversed.forEach((t, i) => { if (fresh[i] !== base[t]) failAt(t, `t=${t} differs on a fresh page drawn in reverse order`); });
  if (bad.length) console.log(`  DIAGNOSIS ${await diagnose(browser, bad[0], [...times, ...wander(bad[0])])}`);
  if (engine === 'chromium') Object.assign(chromeHashes, base);
  else {
    const same = times.filter(t => chromeHashes[t] === base[t]).length;
    console.log(`  cross-engine: ${same}/${times.length} frames pixel-identical to chromium`);
  }
  console.log(`  ${times.map(t => `${t}:${base[t].slice(0, 6)}`).join('  ')}`);
  if (errors.length) fail(`page error during inspection: ${errors.at(-1)}`);
  await browser.close();
}
console.log(failures ? `\n${failures} failure(s)` : '\nseek is pure in t; contract holds');
process.exit(failures ? 1 : 0);
