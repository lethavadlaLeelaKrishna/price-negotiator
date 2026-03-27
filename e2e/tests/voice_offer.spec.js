const { test, expect, chromium } = require('@playwright/test');
const path = require('path');

// NOTE: Update productId and sessionId to match a test session on your dev server
const PRODUCT_ID = process.env.E2E_PRODUCT_ID || 1;
const BASE_URL = process.env.E2E_BASE_URL || 'http://localhost:8000';

// Path to fixture audio (relative to this file)
const fixtureAudio = path.resolve(__dirname, '..', 'fixtures', 'test_audio.wav');

// This test launches Chromium with fake-media flags so we can emulate microphone input
test('voice offer: record and get transcript', async () => {
  const browser = await chromium.launch({
    headless: false, // set to true for headless runs
    args: [
      '--use-fake-ui-for-media-stream',
      '--use-fake-device-for-media-stream',
      `--use-file-for-fake-audio-capture=${fixtureAudio}`
    ]
  });

  const context = await browser.newContext({
    permissions: ['microphone']
  });

  const page = await context.newPage();

  // Navigate to negotiation page
  await page.goto(`${BASE_URL}/negotiate/${PRODUCT_ID}/`);

  // Wait for voice tab button and click it
  await page.click('#voiceTab');
  await page.waitForSelector('#voiceRecordBtn');

  // Click the microphone (this will use the fake audio file)
  await page.click('#voiceRecordBtn');

  // Wait for the UI to indicate listening, then for transcript/processing UI to show result
  await page.waitForTimeout(2500); // let the fake audio be "spoken"

  // Manual stop: click mic again (some browsers stop automatically after file finished)
  await page.click('#voiceRecordBtn');

  // Wait for the captured UI message or transcript text
  await page.waitForSelector('#voiceStatus .fa-check-circle, #transcriptText', { timeout: 5000 });

  // Check that a transcript appears or the success message is shown
  const transcriptText = await page.$eval('#transcriptText', el => el.textContent).catch(() => '');
  const voiceStatusHtml = await page.$eval('#voiceStatus', el => el.innerHTML).catch(() => '');

  expect((transcriptText && transcriptText.length > 0) || voiceStatusHtml.includes('Microphone OFF - Audio Captured')).toBeTruthy();

  await browser.close();
});
