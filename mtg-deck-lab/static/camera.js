"use strict";

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const startBtn = document.getElementById("start");
const captureBtn = document.getElementById("capture");
const resultEl = document.getElementById("result");
const qInput = document.getElementById("q");
const searchBtn = document.getElementById("searchBtn");
let stream = null;

function showResult(html) {
  resultEl.hidden = false;
  resultEl.innerHTML = html;
}

function cardHtml(c, note) {
  const price = c.price_usd ? `<span class="price">$${c.price_usd}</span>` : "";
  const ocr = note ? `<p class="muted">Lido: “${note}”</p>` : "";
  return `
    <div class="found">
      ${c.image ? `<img src="${c.image}" alt="${c.name}">` : ""}
      <div>
        <h3>${c.name} ${price}</h3>
        <p class="muted">${c.type_line || ""} · ${c.set || ""}</p>
        ${ocr}
        ${c.scryfall_uri ? `<a href="${c.scryfall_uri}" target="_blank" rel="noopener">Ver no Scryfall</a>` : ""}
      </div>
    </div>`;
}

startBtn.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: "environment" } }, audio: false,
    });
    video.srcObject = stream;
    captureBtn.disabled = false;
    startBtn.textContent = "Câmera ligada";
  } catch (e) {
    showResult(`<p class="warn">Não consegui acessar a câmera: ${e.message}.
      No celular, é preciso HTTPS ou rede local. Use a busca por nome abaixo.</p>`);
  }
});

captureBtn.addEventListener("click", async () => {
  if (!stream) return;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
  showResult(`<p class="muted">Identificando…</p>`);
  const form = new FormData();
  form.append("image", dataUrl);
  try {
    const r = await fetch("/recognize", { method: "POST", body: form });
    const data = await r.json();
    if (r.ok) showResult(cardHtml(data, data.ocr));
    else showResult(`<p class="warn">${data.error || "Não reconheci."}</p>`);
  } catch (e) {
    showResult(`<p class="warn">Erro: ${e.message}</p>`);
  }
});

async function search() {
  const q = qInput.value.trim();
  if (!q) return;
  showResult(`<p class="muted">Buscando…</p>`);
  try {
    const r = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const data = await r.json();
    if (r.ok) showResult(cardHtml(data, null));
    else showResult(`<p class="warn">${data.error || "Não encontrada."}</p>`);
  } catch (e) {
    showResult(`<p class="warn">Erro: ${e.message}</p>`);
  }
}
searchBtn.addEventListener("click", search);
qInput.addEventListener("keydown", (e) => { if (e.key === "Enter") search(); });
