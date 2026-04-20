import sharp from 'sharp';
import { readdir, mkdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const SRC = 'Assets';
const OUT = 'Assets/optimized';

const PHOTO_WIDTHS = [400, 800, 1600];
const LOGO_WIDTHS = [200, 400];

async function walk(dir, files = []) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name === 'optimized') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) await walk(full, files);
    else if (/\.(jpe?g|png)$/i.test(entry.name)) files.push(full);
  }
  return files;
}

async function ensureDir(p) {
  if (!existsSync(p)) await mkdir(p, { recursive: true });
}

function outBase(srcPath) {
  const rel = path.relative(SRC, srcPath);
  const parsed = path.parse(rel);
  const slug = path.join(parsed.dir, parsed.name).replace(/\\/g, '/');
  return slug;
}

async function convert(srcPath) {
  const isLogo = /Logo\.jpg$/i.test(srcPath);
  const widths = isLogo ? LOGO_WIDTHS : PHOTO_WIDTHS;
  const base = outBase(srcPath);
  const outDir = path.join(OUT, path.dirname(base));
  await ensureDir(outDir);

  const meta = await sharp(srcPath).metadata();
  const results = [];

  for (const w of widths) {
    if (meta.width && w > meta.width) continue;
    const outPath = path.join(OUT, `${base}-${w}.webp`);
    await sharp(srcPath)
      .resize({ width: w, withoutEnlargement: true })
      .webp({ quality: isLogo ? 90 : 78, effort: 5 })
      .toFile(outPath);
    const s = await stat(outPath);
    results.push({ w, kb: Math.round(s.size / 1024), path: outPath });
  }
  return { src: srcPath, srcKb: Math.round((await stat(srcPath)).size / 1024), results };
}

const files = await walk(SRC);
console.log(`Found ${files.length} source images.`);
let totalSrc = 0, totalOut = 0;
for (const f of files) {
  const r = await convert(f);
  totalSrc += r.srcKb;
  const outKb = r.results.reduce((a, b) => a + b.kb, 0);
  totalOut += outKb;
  const variants = r.results.map(x => `${x.w}w=${x.kb}KB`).join(' ');
  console.log(`${path.basename(f)}: ${r.srcKb}KB -> ${variants}`);
}
console.log(`\nTotal source: ${totalSrc}KB`);
console.log(`Total optimized (all variants combined): ${totalOut}KB`);
