# End-to-End Testing — Voice Offer (Manual + Automated)

This document describes how to manually test the voice recording/transcription flow and includes a Playwright sample E2E test you can run locally to verify microphone handling (using a fake audio file).

---

## Quick findings
- The frontend uses the Web Speech API (SpeechRecognition) to transcribe live microphone audio into text and then sends the text to the backend.
- The server endpoint `/shop/send-voice-offer/<session_id>/` accepts uploaded `audio` files (WAV) and handles them correctly (existing unit test covers direct POST uploads).

---

## Manual Test Checklist ✅
1. Start the Django dev server:
   - `python manage.py runserver`
2. Open the product negotiation page in a modern browser (Chrome/Edge recommended):
   - `http://localhost:8000/negotiate/<product_id>/` (click "Start Negotiation" from a product page).
3. Open the **Voice Offer** tab.
4. Click the microphone button and allow the browser to access your microphone when prompted.
5. Speak naturally ("I will pay 19.99" or "nineteen ninety nine rupees").
6. Wait for the transcript to appear under *Audio Transcript* and confirm the parsed price fills the Price field.
7. Click **Send Voice Message** and verify the chat updates with a user message and bot response.
8. Confirm the negotiation state updates (accepted/counter/rejected) and DB entries are created (`ChatMessage` with `message_type='user_voice'` if audio upload path used, or `user_text` if only transcription used).
9. (Optional) Check `media/chat_audio/` for any stored audio files.

Troubleshooting:
- If microphone access is denied, ensure browser site permissions allow microphone and you're on `localhost` or HTTPS.
- If SpeechRecognition isn't supported, use Chrome/Edge or switch to the manual audio upload (server endpoint accepts `audio` file posts).

---

## Automated E2E (Playwright) — Sample
This repository includes a sample Playwright test that emulates a microphone using Chromium's fake audio flags and a pre-recorded WAV file.

Prerequisites:
- Node.js (v16+)
- Install Playwright in project folder (recommended to create `e2e` folder):
  ```bash
  cd e2e
  npm init -y
  npm i -D @playwright/test
  npx playwright install
  ```

Important Chrome args used by test:
- `--use-fake-ui-for-media-stream` — auto-accepts permission prompt
- `--use-fake-device-for-media-stream` — uses a fake device
- `--use-file-for-fake-audio-capture=<path-to-wav>` — feeds a WAV file as microphone input

How to use the sample test:
1. Put a short WAV file (mono, 16-bit PCM) at `e2e/fixtures/test_audio.wav` (a short phrase containing a numeric price helps).
2. Start the Django dev server: `python manage.py runserver`
3. Run the test from `e2e/`:
   ```bash
   npx playwright test tests/voice_offer.spec.js --headed --project=chromium
   ```

If successful, the test will:
- Launch Chromium with fake audio and microphone permission granted
- Visit the negotiation page for a provided `productId` and `sessionId`
- Click the microphone and assert that the transcript UI displays a captured message or transcript

Limitations:
- The test requires a running dev server and a valid negotiation session for the visited product. The sample test includes comments on how to initialize test data manually or adapt it to spin up fixtures via the Django test server.

---

## Files added
- `e2e/tests/voice_offer.spec.js` — Playwright sample test (see `e2e/`)
- `e2e/fixtures/README.md` — small guidance about audio fixture placement

---

If you'd like, I can:
- Add a `Makefile`/npm script to run Playwright tests easily, or
- Add an automated step to create a temporary negotiation session via the Django admin API so the test can run fully unattended.

Which follow-up would you prefer? (add scripts to create session automatically, or keep manual test setup instructions?)
