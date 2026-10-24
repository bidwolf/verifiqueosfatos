// Shares a fact check as a story image (1080x1920).
// Loaded on demand by index.html on the first click on a .story button.
(() => {
  // A retry after a partial network failure may run this file twice
  if (self.openShare) return;

  document.body.insertAdjacentHTML('beforeend', `
    <dialog class="sh" aria-labelledby="sh-title">
      <div class="sh-box">
        <button type="button" class="sh-close" aria-label="Fechar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>
        </button>
        <canvas class="sh-preview" width="1080" height="1920" role="img" aria-label="Prévia da imagem em formato story"></canvas>
        <div class="sh-side">
          <h2 id="sh-title">Compartilhar checagem</h2>
          <p class="sh-desc">Imagem em formato story (1080 × 1920), pronta para postar. Leva o nome, a fala, o resultado, a data e o endereço do site.</p>
          <span class="label sh-desc" id="sh-look">Aparência</span>
          <div class="sh-look" role="group" aria-labelledby="sh-look">
            <button type="button" class="sh-opt" data-dark="0" aria-pressed="true">Claro</button>
            <button type="button" class="sh-opt" data-dark="1" aria-pressed="false">Escuro</button>
          </div>
          <div class="sh-actions">
            <button type="button" class="sh-btn sh-main" data-act="share-image">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>
              Compartilhar imagem
            </button>
            <button type="button" class="sh-btn" data-act="share">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15V3m-4 4 4-4 4 4M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>
              <span>Compartilhar link</span>
            </button>
            <button type="button" class="sh-btn" data-act="copy" hidden>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/></svg>
              <span>Copiar imagem</span>
            </button>
          </div>
        </div>
      </div>
    </dialog>
  `);

  // Story colors (light, dark)
  const themes = [
    { bg: '#FAFAFA', ink: '#171717', ink2: '#404040', muted: '#525252', line: '#E5E5E5', soft: '#F0F0F0' },
    { bg: '#171717', ink: '#FAFAFA', ink2: '#D4D4D4', muted: '#A3A3A3', line: '#2E2E2E', soft: '#262626' },
  ];

  // Same tones as .badge in style.css (0 and 4 have no verdict: neutral)
  const tones = { 0: '#6B7280', 1: '#15803D', 2: '#B91C1C', 3: '#C2410C', 4: '#6B7280' };
  const SANS = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif';
  const SERIF = 'Georgia, "Times New Roman", serif';

  // Story layout (1080x1920). Top and bottom keep clear of the Instagram UI.
  const W = 1080, H = 1920, X = 84, R = W - X, TOP = 288, BOTTOM = H - 360;

  const dialog = document.querySelector('.sh');
  const canvas = dialog.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  const shareButton = dialog.querySelector('[data-act=share]');
  const copyButton = dialog.querySelector('[data-act=copy]');
  let opener, card, dark, photo, blob, canShareImage;

  // Same logo as the page header
  const logo = new Image();
  logo.src = '/icon.png';
  logo.decode().then(() => card && draw(), () => {});

  try {
    canShareImage = navigator.canShare({ files: [new File([''], 'a.png', { type: 'image/png' })] });
  } catch {}
  copyButton.hidden = !self.ClipboardItem;

  const font = (weight, size, family = SANS) => ctx.font = `${weight} ${size}px ${family}`;

  // Shrinks a single line until it fits the width
  function fit(text, weight, size, width, family) {
    do font(weight, size, family); while (ctx.measureText(text).width > width && --size > 20);
  }

  // Word wrap with measureText. Breaks words longer than a line (e.g. URLs)
  // and ends with an ellipsis when the text needs more than `max` lines.
  function wrap(text, width, max) {
    const lines = [];
    let line = '';
    for (let word of text.trim().split(/\s+/)) {
      while (ctx.measureText(word).width > width) {
        let i = word.length;
        while (i > 1 && ctx.measureText(word.slice(0, i)).width > width) i--;
        if (line) lines.push(line);
        lines.push(word.slice(0, i));
        line = '';
        word = word.slice(i);
      }
      const test = line ? `${line} ${word}` : word;
      if (line && ctx.measureText(test).width > width) {
        lines.push(line);
        line = word;
      } else {
        line = test;
      }
    }
    if (line) lines.push(line);
    if (lines.length > max) {
      lines.length = max;
      let last = lines[max - 1];
      while (last && ctx.measureText(`${last}…`).width > width) last = last.slice(0, -1);
      lines[max - 1] = `${last.trimEnd()}…`;
    }
    return lines;
  }

  // Small uppercase section label ("DISSE QUE", "VERIFICAÇÃO")
  function label(text, x, y, color) {
    font(600, 33);
    ctx.letterSpacing = '3px';
    ctx.fillStyle = color;
    ctx.fillText(text.toUpperCase(), x, y);
    ctx.letterSpacing = '0px';
  }

  function draw() {
    const t = themes[+dark];
    const name = card.querySelector('h2').textContent;
    const badge = card.querySelector('.badge');
    const result = badge.textContent;
    const cy = TOP + 72;

    blob = null;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillStyle = t.bg;
    ctx.fillRect(0, 0, W, H);

    // Author: same look as .card img in the feed (56px, 10px corners)
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(X, TOP, 144, 144, 26);
    ctx.fillStyle = t.line;
    ctx.fill();
    ctx.clip();
    if (photo) ctx.drawImage(photo, X, TOP, 144, 144);
    ctx.restore();

    // Result seal: same look as .badge in the feed, at 2.8x
    font(600, 42);
    const sealW = ctx.measureText(result).width + 90;
    const sealX = R - sealW;
    ctx.beginPath();
    ctx.roundRect(sealX, cy - 61.5, sealW, 123, 61.5);
    ctx.fillStyle = tones[badge.dataset.c];
    ctx.fill();
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#FFFFFF';
    ctx.fillText(result, sealX + 45, cy + 2);
    ctx.fillStyle = t.ink;

    // Name and date, never wrapping
    const colX = X + 180, colW = sealX - 24 - colX;
    ctx.textBaseline = 'alphabetic';
    fit(name, 600, 51, colW);
    ctx.fillText(name, colX, cy - 6);
    const date = `Gerado em ${new Date().toLocaleDateString('pt-BR')}`;
    fit(date, 400, 33, colW);
    ctx.fillStyle = t.muted;
    ctx.fillText(date, colX, cy + 44);

    // "Disse que": the quote shrinks until it fits in 5 lines
    const quote = card.querySelector('.said p').textContent;
    const quoteW = R - X - 108;
    let size = 66, lines;
    do {
      font(500, size, SERIF);
      lines = wrap(quote, quoteW, Infinity);
    } while (lines.length > 5 && (size -= 2) >= 48);
    if (size < 48) font(500, size = 48, SERIF);
    lines = wrap(quote, quoteW, 5);
    const lh = size * 1.3;
    const labelY = TOP + 204;
    const boxY = labelY + 33 + 24;
    const textY = boxY + 48;
    const boxH = 48 + (lines.length - 1) * lh + size + 48;
    ctx.textBaseline = 'top';
    label('Disse que:', X, labelY, t.muted);
    ctx.beginPath();
    ctx.roundRect(X, boxY, R - X, boxH, 48);
    ctx.fillStyle = t.soft;
    ctx.fill();
    font(500, size, SERIF);
    ctx.fillStyle = t.ink;
    lines.forEach((l, i) => ctx.fillText(l, X + 54, textY + i * lh));

    // Footer: divider, brand and address, right above the bottom safe zone
    const rowY = BOTTOM - 24 - 66;
    const lineY = rowY - 42;

    // "Verificação": up to 4 lines, never reaching the divider. When the card lists sources,
    // the last line names them (the image should never travel without its source)
    const checkY = boxY + boxH + 60;
    const checkTextY = checkY + 33 + 24;
    const sources = [...card.querySelectorAll('.sources a')].map(a => a.textContent).slice(0, 3);
    const room = Math.floor((lineY - 48 - checkTextY - 42) / 63) + 1 - (sources.length ? 1 : 0);
    label('Verificação:', X, checkY, t.muted);
    font(400, 42);
    ctx.fillStyle = t.ink2;
    const checkLines = wrap(card.querySelector(':scope > p').textContent, R - X, Math.max(1, Math.min(4, room)));
    checkLines.forEach((l, i) => ctx.fillText(l, X, checkTextY + i * 63));
    if (sources.length) {
      font(400, 33);
      ctx.fillStyle = t.muted;
      ctx.fillText(wrap(`Fontes: ${sources.join(' · ')} · checagem revisável`, R - X, 1)[0], X, checkTextY + checkLines.length * 63 + 12);
    }

    ctx.fillStyle = t.line;
    ctx.fillRect(X, lineY, R - X, 2);
    if (logo.complete && logo.naturalWidth) ctx.drawImage(logo, X, rowY, 66, 66);
    ctx.textBaseline = 'middle';
    font(400, 45, SERIF);
    ctx.fillStyle = t.ink;
    ctx.fillText('Verifique os Fatos', X + 90, rowY + 35);
    font(400, 36);
    ctx.textAlign = 'right';
    ctx.fillStyle = t.muted;
    ctx.fillText('verifiqueosfatos.com', R, rowY + 35);

    // Ready ahead of time so "Compartilhar imagem" keeps the click's user activation
    canvas.toBlob(b => blob = b, 'image/png');
  }

  const slug = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-');

  function fileName() {
    return `checagem-${slug(card.querySelector('h2').textContent)}-${slug(card.querySelector('.badge').textContent)}.png`;
  }

  // Image only, so it can be posted as a story; downloads it where files can't be shared
  function shareImage() {
    if (!blob) return;
    if (canShareImage) return navigator.share({ files: [new File([blob], fileName(), { type: 'image/png' })] }).catch(() => {});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = fileName();
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 10000);
  }

  // Shares the link to the card; without the Web Share API, copies it instead
  async function share() {
    const name = card.querySelector('h2').textContent;
    const title = `Veja se ${name} falou a verdade`;
    const text = `${name} disse que: "${card.querySelector('.said').textContent.trim()}"\n\nSerá que é verdade? Veja a checagem:`;
    const url = `${location.origin}/#${card.id}`;
    if (navigator.share) return navigator.share({ title, text, url }).catch(() => {});
    try {
      await navigator.clipboard.writeText(`${text}\n${url}`);
      const label = shareButton.querySelector('span');
      label.textContent = 'Copiado!';
      setTimeout(() => label.textContent = 'Compartilhar link', 2000);
    } catch {}
  }

  // Safari only keeps the click's user activation if the ClipboardItem gets a promise
  function copy() {
    const label = copyButton.querySelector('span');
    navigator.clipboard.write([new ClipboardItem({ 'image/png': new Promise(r => canvas.toBlob(r, 'image/png')) })])
      .then(() => {
        label.textContent = 'Imagem copiada!';
        setTimeout(() => label.textContent = 'Copiar imagem', 2000);
      }, () => {});
  }

  // Same-origin photo from the card itself, decoded before drawing
  function loadPhoto() {
    const current = card, img = new Image();
    photo = null;
    img.src = card.querySelector('img').currentSrc || card.querySelector('img').src;
    img.decode().then(() => {
      if (card !== current) return;
      photo = img;
      draw();
    }).catch(() => {});
  }

  function setLook(isDark) {
    dark = isDark;
    dialog.querySelectorAll('.sh-opt').forEach(b => b.setAttribute('aria-pressed', (b.dataset.dark === '1') === dark));
    draw();
  }

  // Called by the loader in index.html after share.css and share.js arrive
  self.openShare = button => {
    opener = button;
    card = button.closest('.card');
    loadPhoto();
    setLook(document.documentElement.dataset.theme === 'dark');
    dialog.showModal();
  };

  dialog.addEventListener('click', e => {
    // A click on the dialog itself (outside .sh-box) is a click on the backdrop
    if (e.target === dialog) return dialog.close();
    const b = e.target.closest('button');
    if (!b) return;
    if (b.classList.contains('sh-close')) dialog.close();
    else if (b.dataset.dark) setLook(b.dataset.dark === '1');
    else if (b.dataset.act === 'share-image') shareImage();
    else if (b.dataset.act === 'share') share();
    else if (b.dataset.act === 'copy') copy();
  });

  dialog.addEventListener('close', () => opener && opener.focus());
})();
