#!/usr/bin/env python3
"""Gera metodologia.html a partir de METODOLOGIA.md, no layout do site.

Uso: python3 scripts/build_metodologia.py   (requer: pip install markdown)
Rode sempre que METODOLOGIA.md mudar e faça commit dos dois arquivos.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "METODOLOGIA.md"
TARGET = ROOT / "metodologia.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="/favicon.ico?v=2" sizes="48x48 32x32 16x16">
  <link rel="manifest" href="/manifest.json">
  <link rel="stylesheet" href="/normalize.css">
  <link rel="stylesheet" href="/style.css">
  <meta name="theme-color" content="#FAFAFA">
  <script>
    function setTheme(dark) {
      document.documentElement.dataset.theme = dark ? 'dark' : 'light';
      document.querySelector('meta[name=theme-color]').content = dark ? '#0A0A0A' : '#FAFAFA';
    }
    let savedTheme = null;
    try { savedTheme = localStorage.getItem('theme'); } catch {}
    setTheme(savedTheme ? savedTheme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches);
  </script>
  <title>Metodologia — Verifique os Fatos</title>
  <meta name="description" content="Como as falas são escolhidas, classificadas, revisadas e contestadas no Verifique os Fatos.">
  <style>
    /* Prosa do documento: só o necessário por cima do style.css */
    .prose { max-width: 720px; margin: 0 auto; color: var(--ink2); }
    .prose h1, .prose h2, .prose h3 { color: var(--ink); line-height: 1.25; }
    .prose h1 { font: 400 28px/1.2 var(--serif); margin: 0 0 16px; }
    .prose h2 { font-size: 20px; margin: 40px 0 12px; padding-top: 16px; border-top: 1px solid var(--line); }
    .prose h3 { font-size: 16px; margin: 24px 0 8px; }
    .prose p, .prose li { font-size: 16px; line-height: 1.6; }
    .prose blockquote { margin: 0 0 20px; padding: 10px 16px; background: var(--soft); border-left: 3px solid var(--line2); }
    .prose blockquote p { margin: 6px 0; font-size: 15px; }
    .prose table { width: 100%; border-collapse: collapse; margin: 12px 0 20px; font-size: 14px; }
    .prose th, .prose td { padding: 8px 10px; border: 1px solid var(--line); text-align: left; vertical-align: top; }
    .prose th { background: var(--soft); color: var(--ink); }
    .prose code { padding: 1px 5px; background: var(--soft); border-radius: 4px; font-size: .92em; }
    .prose pre { padding: 12px 14px; overflow: auto; background: var(--soft); border-radius: 8px; font-size: 13px; line-height: 1.5; }
    .prose pre code { padding: 0; background: none; }
    .prose a { color: var(--link); }
    .prose hr { border: 0; border-top: 1px solid var(--line); margin: 28px 0; }
    .prose hr + h2 { border-top: 0; padding-top: 0; margin-top: 0; }
    .prose ul.task { list-style: none; padding-left: 0; }
    .back { font-size: 14px; color: var(--link); }
    @media (max-width: 600px) { .prose table { display: block; overflow-x: auto; } }
  </style>
</head>
<body>
  <div class="layout">
    <header class="top">
      <span class="logo" aria-hidden="true"><img src="/icon.png" alt="" width="40" height="40"></span>
      <div>
        <h1>Verifique os Fatos</h1>
        <p class="sub">Metodologia</p>
      </div>
      <a class="github" href="https://github.com/felippe-regazio/verifiqueosfatos/blob/main/METODOLOGIA.md" target="_blank" rel="noopener noreferrer" aria-label="Fonte deste documento no GitHub">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2A10 10 0 0 0 2 12c0 4.4 2.9 8.2 6.8 9.5.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.3 1.1 2.9.8.1-.6.4-1.1.6-1.3-2.2-.3-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.7 1a9.4 9.4 0 0 1 5 0c1.9-1.3 2.7-1 2.7-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.4 4.7-4.6 5 .4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5A10 10 0 0 0 22 12 10 10 0 0 0 12 2z"/></svg>
      </a>
    </header>
    <p><a class="back" href="/">← Voltar às checagens</a></p>
    <main class="prose">
%%CONTENT%%
    </main>
    <footer class="foot">
      <p>Um projeto feito pela comunidade para a comunidade. Este documento é editado por pull request; qualquer pessoa pode propor mudanças.</p>
    </footer>
  </div>
</body>
</html>
"""


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"], output_format="html5")
    # Checkboxes do checklist (markdown puro não os converte)
    html = html.replace("<li>[ ] ", "<li>☐ ").replace("<li>[x] ", "<li>☑ ")
    TARGET.write_text(TEMPLATE.replace("%%CONTENT%%", html), encoding="utf-8")
    print(f"{TARGET.relative_to(ROOT)} gerado ({TARGET.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
