const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

// Minimal, focused recorder for the three identity rolling demos.
// Captures transparent PNG frames for each targeted container.

// Switch to local standalone to avoid app styling/scrolling side effects
const TARGET_URL = 'http://127.0.0.1:3000/capture-identity.html';
const OUT_DIR = path.join(__dirname, 'frames');

const targets = [
  { selector: '.js-rolling-container-1', name: 'roll-once' },
  { selector: '.js-rolling-container-2', name: 'roll-twice' },
  { selector: '.js-rolling-container-3', name: 'roll-thrice' },
];

async function ensureDir(dir) {
  await fs.promises.mkdir(dir, { recursive: true });
}

async function captureContainer(page, selector, name) {
  await page.waitForSelector(selector, { visible: true, timeout: 30000 });
  const container = await page.$(selector);
  if (!container) {
    throw new Error(`Container ${selector} not found on page`);
  }

  // Scroll into view
  await container.evaluate((el) => el.scrollIntoView({ behavior: 'instant', block: 'center' }));

  // Add CSS to slow transitions so playback isn't too fast during capture
  await page.addStyleTag({
    content: `
      body.capture-slow #js-rolling-one,
      body.capture-slow #js-rolling-two,
      body.capture-slow #js-rolling-three {
        transition: transform 2400ms ease-in-out !important;
      }
    `,
  });
  await page.evaluate(() => document.body.classList.add('capture-slow'));

  // Trigger reset then start if present
  await page.evaluate((sel) => {
    const root = document.querySelector(sel);
    if (!root) return;
    // Find nearest button inside the same demo card
    const card = root.closest('.animation-container-js');
    if (card) {
      const buttons = Array.from(card.querySelectorAll('button'));
      const resetBtn = buttons.find(b => /reset/i.test(b.textContent || ''));
      if (resetBtn) resetBtn.click();
      const startBtn = buttons.find(b => b.classList.contains('btn-primary')) || buttons[0];
      if (startBtn) setTimeout(() => startBtn.click(), 150);
    }
  }, selector);

  const dir = path.join(OUT_DIR, name);
  await ensureDir(dir);

  const FPS = 30;
  const seconds = 5; // capture length
  const frames = FPS * seconds;
  for (let i = 0; i < frames; i++) {
    const file = path.join(dir, `frame_${String(i).padStart(4, '0')}.png`);
    await container.screenshot({ path: file, omitBackground: true });
    await page.waitForTimeout(Math.round(1000 / FPS));
  }
}

async function launchBrowser() {
  const executablePath = process.env.PUPPETEER_EXECUTABLE_PATH || undefined;
  const common = {
    defaultViewport: { width: 1280, height: 1000 },
    ignoreHTTPSErrors: true,
    dumpio: true,
    executablePath,
    timeout: 120000,
  };
  // Try default first, then fallback with no-sandbox flags if Chromium crashes
  const attempts = [
    { headless: 'new', args: [] },
    { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'] },
  ];
  let lastErr;
  for (const opts of attempts) {
    try {
      return await puppeteer.launch({ ...common, ...opts });
    } catch (e) {
      lastErr = e;
    }
  }
  throw lastErr;
}

async function main() {
  await ensureDir(OUT_DIR);
  const browser = await launchBrowser();
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 1000, deviceScaleFactor: 3 });
    await page.goto(TARGET_URL, { waitUntil: 'networkidle2', timeout: 120000 });
    await page.waitForSelector('.js-rolling-container-1, .js-rolling-container-2, .js-rolling-container-3', { timeout: 30000 });

    // Give CSS/JS time to settle
    await page.waitForTimeout(500);

    for (const t of targets) {
      console.log(`Recording ${t.name} (${t.selector})`);
      await captureContainer(page, t.selector, t.name);
    }

    console.log('Recording complete. Frames saved in cubrick/frames/<name>/');
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});


