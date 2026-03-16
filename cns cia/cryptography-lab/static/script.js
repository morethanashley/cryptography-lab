// ── Cryptography Lab - Complete Script ────────────────────────────────────────
const API = '';
let explainMode = false;
let egPairs = [];

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', e => {
      e.preventDefault();
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      renderPage(item.dataset.algo);
    });
  });
  document.getElementById('themeToggle').addEventListener('change', e => {
    document.documentElement.setAttribute('data-theme', e.target.checked ? 'light' : 'dark');
  });
  document.getElementById('explainMode').addEventListener('change', e => {
    explainMode = e.target.checked;
    document.querySelectorAll('.steps-panel').forEach(p => p.classList.toggle('visible', explainMode));
  });
  renderPage('home');
});

async function apiPost(ep, body) {
  try {
    const r = await fetch(ep, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body) });
    return r.json();
  } catch(e) { return { status:'error', message: e.message }; }
}

function renderPage(algo) {
  const titles = { home:'Cryptography Learning Lab', caesar:'Caesar Cipher', vigenere:'Vigenere Cipher', hill:'Hill Cipher', playfair:'Playfair Cipher', railfence:'Rail Fence Cipher', rowcolumn:'Row-Column Transposition', des:'DES Algorithm', aes:'AES Algorithm', rsa:'RSA Algorithm', dh:'Diffie-Hellman Key Exchange', elgamal:'ElGamal Cryptography', ecc:'Elliptic Curve Cryptography' };
  document.getElementById('pageTitle').textContent = titles[algo] || algo;
  const area = document.getElementById('contentArea');
  area.innerHTML = '';
  const pages = { home:renderHome, caesar:renderCaesar, vigenere:renderVigenere, hill:renderHill, playfair:renderPlayfair, railfence:renderRailFence, rowcolumn:renderRowColumn, des:renderDES, aes:renderAES, rsa:renderRSA, dh:renderDH, elgamal:renderElGamal, ecc:renderECC };
  if (pages[algo]) pages[algo](area);
}

function navigateTo(algo) {
  document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.algo === algo));
  renderPage(algo);
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function esc(s) { return String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function showToast(msg, type) {
  const t = document.createElement('div');
  t.textContent = msg;
  const bg = type === 'error' ? 'var(--red)' : type === 'success' ? 'var(--green)' : 'var(--accent)';
  Object.assign(t.style, { position:'fixed', bottom:'24px', right:'24px', background:bg, color:'white', padding:'10px 20px', borderRadius:'8px', fontSize:'13px', zIndex:'9999', boxShadow:'0 4px 20px rgba(0,0,0,0.3)' });
  document.body.appendChild(t); setTimeout(() => t.remove(), 2500);
}

function copyText(text) { navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard!', 'success')); }

function fillExample(prefix, vals) {
  Object.entries(vals).forEach(([k,v]) => { const el = document.getElementById(prefix+'-'+k); if(el) el.value = v; });
}

function resetForm(id) {
  document.querySelectorAll('[id^="'+id+'-"]').forEach(el => { if(el.tagName==='INPUT'||el.tagName==='TEXTAREA') el.value=''; });
  const out = document.getElementById(id+'-output');
  if(out) out.innerHTML = '<span style="color:var(--text2)">Result will appear here...</span>';
  const steps = document.getElementById(id+'-explain');
  if(steps) steps.innerHTML = '';
}

function exBtn(id, vals) {
  return '<button class="btn btn-outline btn-sm" onclick=\'fillExample("'+id+'",'+JSON.stringify(vals)+')\'>📋 Load Example</button>';
}

function kvRow(k, v) {
  return '<div class="kv-row"><span class="kv-key">'+esc(k)+'</span><span class="kv-val">'+esc(String(v))+'</span></div>';
}

// ── Rich Output Renderer ──────────────────────────────────────────────────────
function showResult(id, result, steps, charSteps) {
  const out = document.getElementById(id+'-output');
  if (out) {
    out.className = 'result-box pulse';
    out.innerHTML =
      '<div class="result-label">✅ Result</div>' +
      '<div class="result-value">'+esc(result)+'</div>' +
      '<div class="result-actions">' +
      '<button class="btn btn-outline btn-sm" onclick=\'copyText("'+esc(result)+'")\'>📋 Copy</button>' +
      '</div>';
  }
  const explainEl = document.getElementById(id+'-explain');
  if (!explainEl) return;
  if (!steps || !steps.length) { explainEl.innerHTML = ''; return; }

  let html = '<div class="explain-panel">' +
    '<div class="explain-panel-header">📚 Step-by-Step Explanation</div>' +
    '<div class="step-timeline">';

  steps.forEach((s, i) => {
    html += '<div class="step-block"><div class="step-dot"></div><div class="step-card">' +
      '<div class="step-num">Step ' + (i+1) + '</div>' +
      '<div class="step-heading">'+esc(s.step || s.description || 'Process')+'</div>';
    if (s.description && s.step) html += '<div class="step-body">'+esc(s.description)+'</div>';
    if (s.formula) html += '<div class="step-formula-box">'+esc(s.formula)+'</div>';
    if (s.note) html += '<div class="step-note">💡 '+esc(s.note)+'</div>';
    html += '</div></div>';
  });

  html += '</div>';

  if (charSteps && charSteps.length) {
    html += '<div style="margin-top:16px"><div class="step-num" style="margin-bottom:8px">Character-by-Character Breakdown</div>' +
      '<table class="char-table"><thead><tr><th>Original</th><th>Process</th><th>Result</th></tr></thead><tbody>';
    charSteps.forEach(cs => {
      if (cs.unchanged) {
        html += '<tr><td>'+esc(cs.original||cs.plain||cs.cipher||'')+'</td><td style="color:var(--text2)">unchanged</td><td class="enc-col">'+esc(cs.encrypted||cs.decrypted||'')+'</td></tr>';
      } else {
        const orig = cs.original||cs.plain||cs.cipher||'';
        const enc = cs.encrypted||cs.decrypted||'';
        const proc = cs.formula || (cs.key_char ? 'key='+cs.key_char+', shift='+cs.key_shift : cs.original_pos !== undefined ? 'pos '+cs.original_pos+' → '+cs.new_pos : '');
        html += '<tr><td>'+esc(orig)+'</td><td style="color:var(--cyan);font-family:var(--mono)">'+esc(proc)+'</td><td class="enc-col">'+esc(enc)+'</td></tr>';
      }
    });
    html += '</tbody></table></div>';
  }

  html += '</div>';
  explainEl.innerHTML = html;
  if (explainMode) explainEl.style.display = 'block';
}

function showError(id, msg) {
  const out = document.getElementById(id+'-output');
  if (out) out.innerHTML = '<div style="color:var(--red);font-size:13px">❌ Error: '+esc(msg)+'</div>';
  showToast(msg, 'error');
}

function outputArea(id) {
  return '<div id="'+id+'-output" style="min-height:60px;padding:14px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;font-family:var(--mono);font-size:13px;color:var(--text2)">Result will appear here...</div>' +
    '<div id="'+id+'-explain" style="display:none;margin-top:16px"></div>';
}

// ── Info Card with Tabs ───────────────────────────────────────────────────────
function infoCard(icon, title, what, why, howSteps, uses) {
  const id = 'info-'+Math.random().toString(36).slice(2,7);
  return '<div class="card">' +
    '<div class="card-title">'+icon+' '+esc(title)+'</div>' +
    '<div class="tab-bar">' +
    '<button class="tab-btn active" onclick=\'switchTab("'+id+'","what")\'>What is it?</button>' +
    '<button class="tab-btn" onclick=\'switchTab("'+id+'","how")\'>How it works</button>' +
    '<button class="tab-btn" onclick=\'switchTab("'+id+'","uses")\'>Applications</button>' +
    '</div>' +
    '<div id="'+id+'-what" class="tab-panel active"><p style="font-size:13.5px;color:var(--text2);line-height:1.8">'+esc(what)+'</p></div>' +
    '<div id="'+id+'-how" class="tab-panel"><div class="how-steps">'+howSteps.map((s,i)=>'<div class="how-step"><div class="how-step-num">'+(i+1)+'</div><span>'+esc(s)+'</span></div>').join('')+'</div></div>' +
    '<div id="'+id+'-uses" class="tab-panel"><div class="tag-row">'+uses.map(u=>'<span class="tag">'+esc(u)+'</span>').join('')+'</div></div>' +
    '</div>';
}

function switchTab(id, tab) {
  ['what','how','uses'].forEach(t => {
    const panel = document.getElementById(id+'-'+t);
    if(panel) panel.classList.toggle('active', t===tab);
  });
  const bar = document.querySelector('[onclick*="'+id+'"]')?.closest('.card')?.querySelector('.tab-bar');
  if(bar) bar.querySelectorAll('.tab-btn').forEach((btn,i) => {
    btn.classList.toggle('active', ['what','how','uses'][i]===tab);
  });
}

// ── HOME ──────────────────────────────────────────────────────────────────────
function renderHome(area) {
  const algos = [
    {id:'caesar',icon:'🔤',name:'Caesar Cipher',type:'classical',desc:'Shift letters by a fixed number'},
    {id:'vigenere',icon:'📝',name:'Vigenere Cipher',type:'classical',desc:'Keyword-based polyalphabetic shifts'},
    {id:'hill',icon:'🔢',name:'Hill Cipher',type:'classical',desc:'Matrix multiplication encryption'},
    {id:'playfair',icon:'🎯',name:'Playfair Cipher',type:'classical',desc:'5x5 matrix digraph substitution'},
    {id:'railfence',icon:'🚂',name:'Rail Fence Cipher',type:'classical',desc:'Zigzag transposition cipher'},
    {id:'rowcolumn',icon:'📊',name:'Row-Column Transposition',type:'classical',desc:'Columnar rearrangement by key'},
    {id:'des',icon:'🔒',name:'DES Algorithm',type:'modern',desc:'16-round Feistel block cipher'},
    {id:'aes',icon:'🛡️',name:'AES Algorithm',type:'modern',desc:'Current global encryption standard'},
    {id:'rsa',icon:'🔑',name:'RSA Algorithm',type:'asymmetric',desc:'Public/private key pair encryption'},
    {id:'dh',icon:'🤝',name:'Diffie-Hellman',type:'asymmetric',desc:'Shared secret over public channel'},
    {id:'elgamal',icon:'⚡',name:'ElGamal Cryptography',type:'asymmetric',desc:'Probabilistic DH-based encryption'},
    {id:'ecc',icon:'📈',name:'Elliptic Curve (ECC)',type:'asymmetric',desc:'Strongest security per bit size'},
  ];
  area.innerHTML =
    '<div class="home-hero">' +
    '<h1>🔐 <span>Cryptography</span> Interactive Learning Lab</h1>' +
    '<p>Explore 12 classical and modern cryptography algorithms. Encrypt, decrypt, and get step-by-step explanations of every transformation — designed for students.</p>' +
    '<div style="display:flex;gap:12px;justify-content:center;margin-top:20px;flex-wrap:wrap">' +
    '<span style="background:rgba(16,185,129,0.15);color:var(--green);padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600">6 Classical Ciphers</span>' +
    '<span style="background:rgba(99,102,241,0.15);color:var(--accent2);padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600">2 Modern Symmetric</span>' +
    '<span style="background:rgba(245,158,11,0.15);color:var(--yellow);padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600">4 Asymmetric / Key Exchange</span>' +
    '</div></div>' +
    '<div class="algo-grid">' +
    algos.map(a =>
      '<div class="algo-card" onclick="navigateTo(\''+a.id+'\')">'+
      '<div class="algo-icon">'+a.icon+'</div>'+
      '<div class="algo-name">'+a.name+'</div>'+
      '<div style="font-size:11px;color:var(--text2);margin:4px 0 8px">'+a.desc+'</div>'+
      '<span class="algo-type type-'+a.type+'">'+a.type.charAt(0).toUpperCase()+a.type.slice(1)+'</span>'+
      '</div>'
    ).join('') + '</div>';
}

// ── CAESAR ────────────────────────────────────────────────────────────────────
function renderCaesar(area) {
  area.innerHTML =
    '<div class="module-grid">' +
    infoCard('🔤','Caesar Cipher',
      'The Caesar cipher is one of the oldest known encryption techniques, used by Julius Caesar to protect military messages. It works by shifting every letter in the plaintext by a fixed number of positions in the alphabet.',
      ['Take each letter of your message','Find its position in the alphabet (A=0, B=1, ... Z=25)','Add the shift value to the position','If it goes past Z, wrap around to the beginning','The resulting letter is your encrypted character'],
      ['Historical military communications','ROT13 (a Caesar cipher with shift 13)','Teaching the basics of substitution ciphers','Simple text obfuscation']
    ) +
    '<div class="card"><div class="card-title">🔧 Try It Yourself</div>' +
    '<div class="form-group"><label>Message</label><input type="text" id="caesar-text" placeholder="Type your message here..."/></div>' +
    '<div class="form-group"><label>Shift Value (0–25)</label><input type="number" id="caesar-shift" min="0" max="25" value="3"/></div>' +
    '<div class="btn-row">' +
    '<button class="btn btn-primary" onclick="doCaesar(\'encrypt\')">🔒 Encrypt</button>' +
    '<button class="btn btn-success" onclick="doCaesar(\'decrypt\')">🔓 Decrypt</button>' +
    '<button class="btn btn-outline" onclick="resetForm(\'caesar\')">↺ Reset</button>' +
    exBtn('caesar',{text:'Hello World',shift:'3'}) +
    '</div>' +
    '<div style="margin-top:16px">'+outputArea('caesar')+'</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:20px"><div class="card-title">�� Live Alphabet Shift Visualizer</div>' +
    '<p style="font-size:12px;color:var(--text2);margin-bottom:12px">Change the shift value above to see the mapping update in real time.</p>' +
    '<div id="caesar-viz"></div></div>';
  document.getElementById('caesar-shift').addEventListener('input', updateCaesarViz);
  updateCaesarViz();
}

function updateCaesarViz() {
  const shift = parseInt(document.getElementById('caesar-shift')?.value) || 3;
  const alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const viz = document.getElementById('caesar-viz'); if (!viz) return;
  viz.innerHTML =
    '<div style="margin-bottom:6px;font-size:11px;font-weight:600;color:var(--text2);letter-spacing:1px;text-transform:uppercase">Plain Alphabet</div>' +
    '<div class="alphabet-strip">'+alpha.map(c=>'<div class="alpha-char">'+c+'</div>').join('')+'</div>' +
    '<div style="margin:10px 0;font-size:11px;font-weight:600;color:var(--accent2);letter-spacing:1px;text-transform:uppercase">Cipher Alphabet (shift '+shift+')</div>' +
    '<div class="alphabet-strip">'+alpha.map((_,i)=>'<div class="alpha-char shifted">'+alpha[(i+shift)%26]+'</div>').join('')+'</div>' +
    '<div style="margin-top:12px;font-size:12px;color:var(--text2)">Each plain letter maps to the cipher letter directly below it.</div>';
}

async function doCaesar(op) {
  const text = document.getElementById('caesar-text').value;
  const shift = document.getElementById('caesar-shift').value;
  if (!text) return showToast('Please enter a message first');
  const res = await apiPost('/'+op+'/caesar', { text, shift });
  if (res.status === 'success') {
    showResult('caesar', res.data.result, [
      {step:'Input', description:'Your original message: "'+text+'" with shift value of '+shift},
      {step:'Shift Applied', description:'Each letter is shifted '+shift+' position(s) forward in the alphabet (wrapping around after Z)'},
      {step:'Non-letters', description:'Spaces, numbers, and punctuation are kept unchanged'},
      {step:'Output', description:'Encrypted result: "'+res.data.result+'"'}
    ], res.data.steps);
  } else showError('caesar', res.message);
}

// ── VIGENERE ──────────────────────────────────────────────────────────────────
function renderVigenere(area) {
  area.innerHTML =
    '<div class="module-grid">' +
    infoCard('📝','Vigenere Cipher',
      'The Vigenere cipher uses a keyword to apply multiple different Caesar ciphers to the plaintext. Each letter of the keyword determines the shift for the corresponding plaintext letter. The keyword repeats as needed. It was called "le chiffre indéchiffrable" (the unbreakable cipher) for 300 years.',
      ['Write out your plaintext','Repeat the keyword below it until lengths match','For each letter pair, find the row (key letter) and column (plain letter) in the Vigenere square','The cell where they intersect is the ciphertext letter'],
      ['Historical diplomatic communications','Teaching polyalphabetic substitution','Basis for the one-time pad concept','Cryptanalysis practice (Kasiski test)']
    ) +
    '<div class="card"><div class="card-title">🔧 Try It Yourself</div>' +
    '<div class="form-group"><label>Message</label><input type="text" id="vigenere-text" placeholder="e.g. ATTACKATDAWN"/></div>' +
    '<div class="form-group"><label>Keyword</label><input type="text" id="vigenere-key" placeholder="e.g. LEMON"/></div>' +
    '<div class="btn-row">' +
    '<button class="btn btn-primary" onclick="doVigenere(\'encrypt\')">🔒 Encrypt</button>' +
    '<button class="btn btn-success" onclick="doVigenere(\'decrypt\')">🔓 Decrypt</button>' +
    '<button class="btn btn-outline" onclick="resetForm(\'vigenere\')">↺ Reset</button>' +
    exBtn('vigenere',{text:'ATTACKATDAWN',key:'LEMON'}) +
    '</div>' +
    '<div style="margin-top:16px">'+outputArea('vigenere')+'</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:20px"><div class="card-title">📊 Vigenere Square (Tabula Recta)</div>' +
    '<p style="font-size:12px;color:var(--text2);margin-bottom:10px">Row = key letter, Column = plain letter. Their intersection = cipher letter.</p>' +
    '<div class="vigenere-table-wrap" id="vigenere-table"></div></div>';
  buildVigenereTable();
}

function buildVigenereTable() {
  const alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let html = '<table class="vigenere-table"><tr><th></th>';
  for (const c of alpha) html += '<th>'+c+'</th>';
  html += '</tr>';
  for (let r = 0; r < 26; r++) {
    html += '<tr><th>'+alpha[r]+'</th>';
    for (let c = 0; c < 26; c++) html += '<td>'+alpha[(r+c)%26]+'</td>';
    html += '</tr>';
  }
  const el = document.getElementById('vigenere-table');
  if(el) el.innerHTML = html + '</table>';
}

async function doVigenere(op) {
  const text = document.getElementById('vigenere-text').value;
  const key = document.getElementById('vigenere-key').value;
  if (!text || !key) return showToast('Please enter both message and keyword');
  const res = await apiPost('/'+op+'/vigenere', { text, key });
  if (res.status === 'success') {
    const keyUsed = res.data.key_used || key.toUpperCase();
    showResult('vigenere', res.data.result, [
      {step:'Setup', description:'Message: "'+text+'" | Keyword: "'+keyUsed+'"'},
      {step:'Keyword Repetition', description:'Keyword "'+keyUsed+'" is repeated to match message length: '+keyUsed.repeat(Math.ceil(text.length/keyUsed.length)).slice(0,text.replace(/[^a-zA-Z]/g,'').length)},
      {step:'Lookup in Vigenere Square', description:'For each letter pair (plain, key), find row=key letter, col=plain letter in the table above'},
      {step:'Result', description:op==='encrypt'?'Encrypted: "'+res.data.result+'"':'Decrypted: "'+res.data.result+'"'}
    ], res.data.steps);
  } else showError('vigenere', res.message);
}

// ── HILL ──────────────────────────────────────────────────────────────────────
function renderHill(area) {
  area.innerHTML =
    '<div class="module-grid">' +
    infoCard('🔢','Hill Cipher',
      'The Hill cipher uses matrix multiplication in modular arithmetic (mod 26) to encrypt blocks of letters. The key is an n×n invertible matrix. For a 2×2 key, it encrypts 2 letters at a time. This was the first polygraphic cipher that could operate on more than 3 symbols simultaneously.',
      ['Convert each letter to a number (A=0, B=1, ..., Z=25)','Group the message into blocks matching the matrix size','Multiply the key matrix by each block vector (mod 26)','Convert the resulting numbers back to letters'],
      ['Teaching linear algebra in cryptography','Block cipher design concepts','Academic cryptography courses','Historical cipher analysis']
    ) +
    '<div class="card"><div class="card-title">🔧 Try It Yourself</div>' +
    '<div class="form-group"><label>Message (letters only)</label><input type="text" id="hill-text" placeholder="e.g. HELP"/></div>' +
    '<div class="form-group"><label>Key Matrix — comma-separated (2×2: 4 values, 3×3: 9 values)</label><input type="text" id="hill-key" placeholder="e.g. 6,24,1,13"/></div>' +
    '<div class="btn-row">' +
    '<button class="btn btn-primary" onclick="doHill(\'encrypt\')">🔒 Encrypt</button>' +
    '<button class="btn btn-success" onclick="doHill(\'decrypt\')">�� Decrypt</button>' +
    '<button class="btn btn-outline" onclick="resetForm(\'hill\')">↺ Reset</button>' +
    exBtn('hill',{text:'HELP',key:'6,24,1,13'}) +
    '</div>' +
    '<div style="margin-top:16px">'+outputArea('hill')+'</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:20px"><div class="card-title">🔢 Key Matrix Visualization</div>' +
    '<div id="hill-matrix-viz"><p style="color:var(--text2);font-size:13px">Enter a key matrix above to see it visualized.</p></div></div>';
  document.getElementById('hill-key').addEventListener('input', function() {
    const vals = this.value.split(',').map(v=>parseInt(v.trim())).filter(v=>!isNaN(v));
    const size = Math.round(Math.sqrt(vals.length));
    const viz = document.getElementById('hill-matrix-viz');
    if (size*size===vals.length && size>0 && viz) {
      viz.innerHTML = '<p style="font-size:12px;color:var(--text2);margin-bottom:8px">'+size+'×'+size+' Key Matrix:</p>' +
        '<div class="matrix-grid" style="grid-template-columns:repeat('+size+',44px)">' +
        vals.map(v=>'<div class="matrix-cell">'+v+'</div>').join('') + '</div>';
    }
  });
}

async function doHill(op) {
  const text = document.getElementById('hill-text').value;
  const key = document.getElementById('hill-key').value;
  if (!text || !key) return showToast('Please enter message and key matrix');
  const res = await apiPost('/'+op+'/hill', { text, key });
  if (res.status === 'success') {
    const size = res.data.size || 2;
    const mat = res.data.key_matrix || res.data.inv_matrix;
    if (mat) {
      document.getElementById('hill-matrix-viz').innerHTML =
        '<p style="font-size:12px;color:var(--text2);margin-bottom:8px">'+size+'×'+size+' '+(op==='decrypt'?'Inverse ':'')+'Key Matrix:</p>' +
        '<div class="matrix-grid" style="grid-template-columns:repeat('+size+',44px)">' +
        mat.flat().map(v=>'<div class="matrix-cell highlight">'+v+'</div>').join('') + '</div>';
    }
    showResult('hill', res.data.result, [
      {step:'Prepare Text', description:'Text "'+text+'" padded to multiple of '+size+' with X if needed'},
      {step:'Convert to Numbers', description:'Each letter → number: A=0, B=1, ..., Z=25'},
      {step:'Matrix Multiplication', description:'Each '+size+'-letter block is multiplied by the '+size+'×'+size+' key matrix'},
      {step:'Modulo 26', description:'All results taken mod 26 to stay in alphabet range'},
      {step:'Convert Back', description:'Numbers converted back to letters → "'+res.data.result+'"'}
    ], res.data.steps);
  } else showError('hill', res.message);
}

// ── PLAYFAIR ──────────────────────────────────────────────────────────────────
function renderPlayfair(area) {
  area.innerHTML =
    '<div class="module-grid">' +
    infoCard('🎯','Playfair Cipher',
      'The Playfair cipher encrypts pairs of letters (digraphs) using a 5×5 key matrix. I and J share the same cell. It was the first practical digraph substitution cipher, used by the British in WWI and WWII.',
      ['Build a 5×5 matrix from the keyword (no duplicate letters, I=J)','Split plaintext into pairs; insert X between repeated letters in a pair','For each pair: if same row → shift right; if same column → shift down; otherwise → swap columns (rectangle rule)'],
      ['WWI/WWII British military communications','Teaching digraph substitution','Historical cryptanalysis study','Introduction to block-based ciphers']
    ) +
    '<div class="card"><div class="card-title">🔧 Try It Yourself</div>' +
    '<div class="form-group"><label>Message</label><input type="text" id="playfair-text" placeholder="e.g. HELLO"/></div>' +
    '<div class="form-group"><label>Keyword</label><input type="text" id="playfair-key" placeholder="e.g. MONARCHY"/></div>' +
    '<div class="btn-row">' +
    '<button class="btn btn-primary" onclick="doPlayfair(\'encrypt\')">🔒 Encrypt</button>' +
    '<button class="btn btn-success" onclick="doPlayfair(\'decrypt\')">🔓 Decrypt</button>' +
    '<button class="btn btn-outline" onclick="resetForm(\'playfair\')">↺ Reset</button>' +
    exBtn('playfair',{text:'HELLO',key:'MONARCHY'}) +
    '</div>' +
    '<div style="margin-top:16px">'+outputArea('playfair')+'</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:20px"><div class="card-title">🔲 5×5 Key Matrix</div>' +
    '<p style="font-size:12px;color:var(--text2);margin-bottom:10px">Type a keyword above to see the matrix update live.</p>' +
    '<div id="playfair-matrix"></div></div>';
  document.getElementById('playfair-key').addEventListener('input', updatePlayfairMatrix);
  updatePlayfairMatrix();
}

function buildPFMatrix(key) {
  const k = (key||'MONARCHY').toUpperCase().replace(/J/g,'I');
  const seen = [];
  for (const c of k) if (/[A-Z]/.test(c) && !seen.includes(c)) seen.push(c);
  for (const c of 'ABCDEFGHIKLMNOPQRSTUVWXYZ') if (!seen.includes(c)) seen.push(c);
  return seen;
}

function updatePlayfairMatrix() {
  const key = document.getElementById('playfair-key')?.value || 'MONARCHY';
  const cells = buildPFMatrix(key);
  const viz = document.getElementById('playfair-matrix'); if (!viz) return;
  viz.innerHTML = '<div class="playfair-matrix">'+cells.map(c=>'<div class="pf-cell">'+c+'</div>').join('')+'</div>';
}

async function doPlayfair(op) {
  const text = document.getElementById('playfair-text').value;
  const key = document.getElementById('playfair-key').value;
  if (!text || !key) return showToast('Please enter message and keyword');
  const res = await apiPost('/'+op+'/playfair', { text, key });
  if (res.status === 'success') {
    if (res.data.matrix) {
      document.getElementById('playfair-matrix').innerHTML =
        '<div class="playfair-matrix">'+res.data.matrix.flat().map(c=>'<div class="pf-cell highlight">'+c+'</div>').join('')+'</div>';
    }
    const pairSteps = (res.data.steps||[]).map(s => ({
      step: 'Pair: '+s.pair,
      description: 'Rule: '+s.rule,
      formula: s.pair + ' → ' + (s.encrypted||s.decrypted)
    }));
    showResult('playfair', res.data.result, [
      {step:'Build Matrix', description:'5×5 matrix built from keyword "'+key+'" (I=J, no duplicates)'},
      {step:'Prepare Pairs', description:'Message split into digraphs; X inserted between repeated letters; X appended if odd length'},
      {step:'Apply Rules', description:'Same row → shift right | Same column → shift down | Rectangle → swap columns'},
      ...pairSteps
    ], null);
  } else showError('playfair', res.message);
}

// ── RAIL FENCE ────────────────────────────────────────────────────────────────
function renderRailFence(area) {
  area.innerHTML =
    '<div class="module-grid">' +
    infoCard('🚂','Rail Fence Cipher',
      'The Rail Fence cipher writes the plaintext in a zigzag pattern across a number of "rails" (rows), then reads off each row from top to bottom to produce the ciphertext. It is a transposition cipher — letters are rearranged, not substituted.',
      ['Write the message diagonally down and up across N rails','When you reach the bottom rail, go back up; when you reach the top, go back down','Read each rail from left to right, top rail first','Concatenate all rails to get the ciphertext'],
      ['Teaching transposition ciphers','Simple message obfuscation','Cryptography fundamentals','Basis for more complex route ciphers']
    ) +
    '<div class="card"><div class="card-title">🔧 Try It Yourself</div>' +
    '<div class="form-group"><label>Message</label><input type="text" id="railfence-text" placeholder="e.g. WEAREDISCOVERED"/></div>' +
    '<div class="form-group"><label>Number of Rails</label><input type="number" id="railfence-rails" min="2" max="10" value="3"/></div>' +
    '<div class="btn-row">' +
    '<button class="btn btn-primary" onclick="doRailFence(\'encrypt\')">🔒 Encrypt</button>' +
    '<button class="btn btn-success" onclick="doRailFence(\'decrypt\')">🔓 Decrypt</button>' +
    '<button class="btn btn-outline" onclick="resetForm(\'railfence\')">↺ Reset</button>' +
    exBtn('railfence',{text:'WEAREDISCOVERED',rails:'3'}) +
    '</div>' +
    '<div style="margin-top:16px">'+outputArea('railfence')+'</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:20px"><div class="card-title">🚂 Zigzag Pattern Visualization</div>' +
    '<p style="font-size:12px;color:var(--text2);margin-bottom:10px">Each row is a "rail". Letters are placed in zigzag order, then read row by row.</p>' +
    '<div id="railfence-viz" class="rail-viz"><p style="color:var(--text2)">Encrypt a message to see the zigzag pattern.</p></div></div>';
}

async function doRailFence(op) {
  const text = document.getElementById('railfence-text').value;
  const rails = document.getElementById('railfence-rails').value;
  if (!text) return showToast('Please enter a message');
  const res = await apiPost('/'+op+'/railfence', { text, rails });
  if (res.status === 'success') {
    if (res.data.positions) renderRailViz(res.data.positions, parseInt(rails), text.length);
    showResult('railfence', res.data.result, [
      {step:'Setup', description:'Message "'+text+'" written across '+rails+' rails in zigzag pattern'},
      {step:'Zigzag Writing', description:'Characters placed diagonally: down to rail '+rails+', then back up to rail 1, repeating'},
      {step:'Read by Rail', description:'Read each rail left-to-right: Rail 1 first, then Rail 2, etc.'},
      {step:'Result', description:op==='encrypt'?'Ciphertext: "'+res.data.result+'"':'Plaintext: "'+res.data.result+'"'}
    ], null);
  } else showError('railfence', res.message);
}

function renderRailViz(positions, rails, len) {
  const viz = document.getElementById('railfence-viz'); if (!viz) return;
  const grid = Array.from({length:rails}, () => Array(len).fill(null));
  positions.forEach(p => { grid[p[0]][p[1]] = p[2]; });
  viz.innerHTML = grid.map((row, ri) =>
    '<div class="rail-row"><span class="rail-label">Rail '+(ri+1)+'</span>' +
    row.map(c => c ? '<div class="rail-char filled">'+c+'</div>' : '<div class="rail-char empty">·</div>').join('') +
    '</div>'
  ).join('');
}

// ── ROW-COLUMN ────────────────────────────────────────────────────────────────
function renderRowColumn(area) {
  area.innerHTML =
    '<div class="module-grid">' +
    infoCard('📊','Row-Column Transposition',
      'The Row-Column Transposition cipher writes the plaintext into a grid row by row, then reads the columns in an order determined by alphabetically sorting the keyword. It is a stronger transposition cipher than Rail Fence.',
      ['Write the message into a grid with as many columns as the key length','Number the columns by alphabetical order of the key letters','Read the columns in that numbered order (left to right by number)','Concatenate to get the ciphertext'],
      ['Historical military ciphers (WWII)','Teaching columnar transposition','Combined with substitution for double encryption','Basis for more complex transposition systems']
    ) +
    '<div class="card"><div class="card-title">🔧 Try It Yourself</div>' +
    '<div class="form-group"><label>Message</label><input type="text" id="rowcolumn-text" placeholder="e.g. ATTACKATDAWN"/></div>' +
    '<div class="form-group"><label>Key (determines column reading order)</label><input type="text" id="rowcolumn-key" placeholder="e.g. ZEBRA"/></div>' +
    '<div class="btn-row">' +
    '<button class="btn btn-primary" onclick="doRowColumn(\'encrypt\')">🔒 Encrypt</button>' +
    '<button class="btn btn-success" onclick="doRowColumn(\'decrypt\')">🔓 Decrypt</button>' +
    '<button class="btn btn-outline" onclick="resetForm(\'rowcolumn\')">↺ Reset</button>' +
    exBtn('rowcolumn',{text:'ATTACKATDAWN',key:'ZEBRA'}) +
    '</div>' +
    '<div style="margin-top:16px">'+outputArea('rowcolumn')+'</div>' +
    '</div></div>' +
    '<div class="card" style="margin-top:20px"><div class="card-title">📊 Grid Visualization</div>' +
    '<p style="font-size:12px;color:var(--text2);margin-bottom:10px">Yellow header = key letters with their reading order number. Grid shows message layout.</p>' +
    '<div id="rowcolumn-viz"><p style="color:var(--text2)">Encrypt a message to see the grid.</p></div></div>';
}

async function doRowColumn(op) {
  const text = document.getElementById('rowcolumn-text').value;
  const key = document.getElementById('rowcolumn-key').value;
  if (!text || !key) return showToast('Please enter message and key');
  const res = await apiPost('/'+op+'/rowcolumn', { text, key });
  if (res.status === 'success') {
    if (res.data.grid) {
      const cols = key.length, order = res.data.column_order;
      document.getElementById('rowcolumn-viz').innerHTML =
        '<div class="matrix-grid" style="grid-template-columns:repeat('+cols+',44px);margin-bottom:8px">' +
        key.toUpperCase().split('').map((c,i)=>'<div class="matrix-cell" style="background:rgba(245,158,11,0.15);color:var(--yellow)">'+c+'<br><small style="font-size:9px;color:var(--text2)">#'+(order.indexOf(i)+1)+'</small></div>').join('') + '</div>' +
        '<div class="matrix-grid" style="grid-template-columns:repeat('+cols+',44px)">' +
        res.data.grid.flat().map(c=>'<div class="matrix-cell">'+c+'</div>').join('') + '</div>';
    }
    showResult('rowcolumn', res.data.result, [
      {step:'Write Grid', description:'Message written row by row into a '+key.length+'-column grid'},
      {step:'Number Columns', description:'Columns numbered by alphabetical order of key "'+key.toUpperCase()+'"'},
      {step:'Read Columns', description:op==='encrypt'?'Columns read in numbered order to produce ciphertext':'Columns filled in numbered order, then read row by row'},
      {step:'Result', description:'"'+res.data.result+'"'}
    ], null);
  } else showError('rowcolumn', res.message);
}
