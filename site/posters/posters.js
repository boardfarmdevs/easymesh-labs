// Connector lines from each card of a poster board to its central device, in the card's
// colour (not from a full-width card below the ring). Drawn only in the wide three-column layout; redrawn on resize.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  function draw(board) {
    let svg = board.querySelector(':scope > svg.wires');
    if (!svg) {
      svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('class', 'wires');
      svg.setAttribute('aria-hidden', 'true');
      board.prepend(svg);
    }
    svg.replaceChildren();
    const device = board.querySelector('.device .laptop, .device');
    if (!device || window.innerWidth < 1100) return;
    const b = board.getBoundingClientRect();
    const d = device.getBoundingClientRect();
    const D = { l: d.left - b.left, r: d.right - b.left, t: d.top - b.top, bot: d.bottom - b.top };
    for (const card of board.querySelectorAll(':scope > .card:not(.wide)')) {
      const c = card.getBoundingClientRect();
      const C = { l: c.left - b.left, r: c.right - b.left, t: c.top - b.top, bot: c.bottom - b.top };
      const cx = (C.l + C.r) / 2, cy = (C.t + C.bot) / 2;
      const clampY = (y) => Math.min(Math.max(y, D.t + 24), D.bot - 24);
      const clampX = (x) => Math.min(Math.max(x, D.l + 40), D.r - 40);
      let d1, x1, y1, x2, y2;
      if (C.r < D.l) {
        x1 = C.r; y1 = cy; x2 = D.l; y2 = clampY(cy);
        const mx = (x1 + x2) / 2;
        d1 = `M${x1},${y1} H${mx} V${y2} H${x2}`;
      } else if (C.l > D.r) {
        x1 = C.l; y1 = cy; x2 = D.r; y2 = clampY(cy);
        const mx = (x1 + x2) / 2;
        d1 = `M${x1},${y1} H${mx} V${y2} H${x2}`;
      } else if (C.bot < D.t) {
        x1 = cx; y1 = C.bot + 14; x2 = clampX(cx); y2 = D.t;
        d1 = `M${x1},${y1} V${(y1 + y2) / 2} H${x2} V${y2}`;
      } else {
        x1 = cx; y1 = C.t; x2 = clampX(cx); y2 = D.bot;
        d1 = `M${x1},${y1} V${(y1 + y2) / 2} H${x2} V${y2}`;
      }
      const colour = getComputedStyle(card).getPropertyValue('--c').trim();
      const path = document.createElementNS(NS, 'path');
      path.setAttribute('d', d1);
      path.setAttribute('stroke', colour);
      svg.append(path);
      for (const [x, y] of [[x1, y1], [x2, y2]]) {
        const dot = document.createElementNS(NS, 'circle');
        dot.setAttribute('cx', x); dot.setAttribute('cy', y); dot.setAttribute('r', 4);
        dot.setAttribute('fill', colour);
        svg.append(dot);
      }
    }
  }
  function all() { document.querySelectorAll('.board').forEach(draw); }
  window.addEventListener('resize', all);
  window.addEventListener('load', all);
  document.fonts?.ready.then(all);
})();
