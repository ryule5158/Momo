const fs = require('fs');
const path = require('path');
const sharp = require('C:/Users/LENOVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.cjs');

const root = 'C:/Users/LENOVO/Desktop/Momo';
const source = path.join(root, 'current/svg/MOMO_R166_REQ146_PANEL.svg');
const preview = path.join(root, 'current/preview/MOMO_R166_REQ146_PANEL.png');
const detailSvg = path.join(root, 'verification/MOMO_SKETCH_CAT_DETAIL.svg');
const detailPng = path.join(root, 'verification/MOMO_SKETCH_CAT_DETAIL.png');

async function main() {
  const svg = fs.readFileSync(source, 'utf8');
  const match = svg.match(/<g id="req156-flow-cat-mark"[\s\S]*?<\/g>/);
  if (!match) throw new Error('req156 flow cat group was not found');

  await sharp(Buffer.from(svg), { density: 250 })
    .resize({ height: 1518 })
    .png()
    .toFile(preview);

  const detail = `<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="700" viewBox="480 0 180 100">
  <rect x="480" y="0" width="180" height="100" fill="#f2f0e9"/>
  ${match[0]}
</svg>`;
  fs.writeFileSync(detailSvg, detail, 'utf8');
  await sharp(Buffer.from(detail)).png().toFile(detailPng);
  const review = path.join(root, 'verification/req156_flow_cat');
  fs.mkdirSync(review, { recursive: true });
  fs.copyFileSync(detailPng, path.join(review, 'MOMO_LINEART_DETAIL.png'));
  fs.copyFileSync(preview, path.join(review, 'MOMO_PANEL_PREVIEW.png'));
  await sharp(path.join(review, 'FAMILY_LOGO_COMPARISON.svg')).png().toFile(path.join(review, 'FAMILY_LOGO_COMPARISON.png'));
  const header = svg.replace(/width="[^"]+"/, 'width="1422.4"')
    .replace(/height="[^"]+"/, 'height="260"')
    .replace(/viewBox="[^"]+"/, 'viewBox="0 0 711.2 130"');
  await sharp(Buffer.from(header)).png().toFile(path.join(review, 'MOMO_HEADER_PREVIEW.png'));

  const [previewMeta, detailMeta] = await Promise.all([
    sharp(preview).metadata(),
    sharp(detailPng).metadata(),
  ]);
  console.log(JSON.stringify({
    status: 'PASS',
    preview: { path: preview, width: previewMeta.width, height: previewMeta.height },
    detail: { path: detailPng, width: detailMeta.width, height: detailMeta.height },
  }, null, 2));
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
