const workbench = document.querySelector('#workbench');
const divider = document.querySelector('#workbenchDivider');
const editor = document.querySelector('#editor');
const lineNumbers = document.querySelector('#numbers');

let editorShare = 60;
let dragStart = null;

function isStacked() {
  return window.matchMedia('(max-width: 700px)').matches;
}

function setEditorShare(value) {
  editorShare = Math.max(25, Math.min(75, value));
  workbench.style.gridTemplateColumns = `minmax(0, ${editorShare}fr) 12px minmax(0, ${100 - editorShare}fr)`;
  divider.setAttribute('aria-valuenow', String(Math.round(editorShare)));
}

function setEditorHeight(value) {
  const height = Math.max(390, Math.min(900, value));
  editor.style.height = `${height}px`;
  lineNumbers.style.height = `${height}px`;
  divider.setAttribute('aria-valuenow', String(Math.round(height)));
}

function syncOrientation() {
  if (isStacked()) {
    workbench.style.gridTemplateColumns = '';
    divider.setAttribute('aria-orientation', 'horizontal');
    divider.setAttribute('aria-valuemin', '390');
    divider.setAttribute('aria-valuemax', '900');
    divider.setAttribute('aria-valuenow', String(Math.round(editor.getBoundingClientRect().height)));
  } else {
    divider.setAttribute('aria-orientation', 'vertical');
    divider.setAttribute('aria-valuemin', '25');
    divider.setAttribute('aria-valuemax', '75');
    divider.setAttribute('aria-valuenow', String(Math.round(editorShare)));
    setEditorShare(editorShare);
  }
}

divider.addEventListener('pointerdown', event => {
  event.preventDefault();
  divider.setPointerCapture(event.pointerId);
  dragStart = {
    coordinate: isStacked() ? event.clientY : event.clientX,
    share: editorShare,
    height: editor.getBoundingClientRect().height
  };
});

divider.addEventListener('pointermove', event => {
  if (!dragStart || !divider.hasPointerCapture(event.pointerId)) return;

  if (isStacked()) {
    setEditorHeight(dragStart.height + event.clientY - dragStart.coordinate);
  } else {
    const change = (event.clientX - dragStart.coordinate) / workbench.clientWidth * 100;
    setEditorShare(dragStart.share + change);
  }
});

function stopDragging(event) {
  if (divider.hasPointerCapture(event.pointerId)) divider.releasePointerCapture(event.pointerId);
  dragStart = null;
}

divider.addEventListener('pointerup', stopDragging);
divider.addEventListener('pointercancel', stopDragging);
divider.addEventListener('keydown', event => {
  if (isStacked() && ['ArrowUp', 'ArrowDown'].includes(event.key)) {
    event.preventDefault();
    const direction = event.key === 'ArrowDown' ? 1 : -1;
    setEditorHeight(editor.getBoundingClientRect().height + direction * 40);
  } else if (!isStacked() && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
    event.preventDefault();
    const direction = event.key === 'ArrowRight' ? 1 : -1;
    setEditorShare(editorShare + direction * 5);
  }
});

window.addEventListener('resize', syncOrientation);
syncOrientation();
