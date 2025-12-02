// ----------  config  ----------
const NOTES_KEY = 'coach-notes';
const GCAL_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'; // ← replace once
const GCAL_API_KEY   = 'YOUR_GOOGLE_API_KEY';   // ← replace once

let notes = JSON.parse(localStorage.getItem(NOTES_KEY) || '[]');

function $(id) { return document.getElementById(id); }

// ----------  load today CSV  ----------
async function loadToday() {
  const today = new Date().toISOString().slice(0,10);
  try {
    const csv = await (await fetch(`data/${today}_detected.csv`)).text();
    const rows = csv.split('\n').slice(1).filter(r => r);
    let html = '<table border=1 cellpadding=6><tr><th>activity</th><th>hour</th></tr>';
    rows.forEach(r => { const [a,h] = r.split(','); html += `<tr><td>${a}</td><td>${h}</td></tr>`; });
    html += '</table>';
    $('todayTable').innerHTML = html;
  } catch (e) {
    $('todayTable').innerHTML = '<p>No activity data yet</p>';
  }
}

// ----------  notes CRUD  ----------
function renderNotes() {
  let html = '';
  notes.forEach((n, idx) => {
    const checked = n.done ? 'checked' : '';
    const cls     = n.done ? 'done' : '';
    html += `<div class="note" style="background:${n.color}">
      <input type="checkbox" ${checked} onchange="toggleNote(${idx})">
      <label class="${cls}">${n.title}</label>
      <button onclick="delNote(${idx})">🗑</button>
    </div>`;
  });
  $('notes').innerHTML = html;
  localStorage.setItem(NOTES_KEY, JSON.stringify(notes));
}

function addNote() {
  const title = $('title').value.trim();
  if (!title) return;
  const alarm = $('alarm').value;
  notes.unshift({
    id: Date.now().toString(),
    title: title,
    body: $('body').value.trim(),
    color: '#fffacd',
    done: false,
    alarm: alarm || null
  });
  $('title').value = $('body').value = $('alarm').value = '';
  renderNotes();
  if (alarm) setBrowserAlarm(alarm, title);
}

function toggleNote(idx) {
  notes[idx].done = !notes[idx].done;
  renderNotes();
  suggestNextHour(notes[idx].title);
}

function delNote(idx) {
  if (confirm('Delete?')) { notes.splice(idx, 1); renderNotes(); }
}

// ----------  browser alarm + Windows beep  ----------
function setBrowserAlarm(iso, title) {
  const t = new Date(iso).getTime() - Date.now();
  if (t <= 0) return;
  setTimeout(() => {
    new Notification('Coach alarm', { body: title });
    // Windows native beep (if running on PC)
    if (window.Windows) Windows.UI.Notifications.ToastNotificationManager.show(new Windows.UI.Notifications.ToastNotification(
      new Windows.Data.Xml.Dom.XmlDocument.loadXml(`<toast><visual><binding template='ToastText01'><text id='1'>${title}</text></binding></visual></toast>`)
    ));
  }, t);
  if ('Notification' in window && Notification.permission !== 'granted') Notification.requestPermission();
}

// ----------  AI suggestion  ----------
function suggestNextHour(text) {
  const words = text.toLowerCase();
  let label = 'general';
  if (words.includes('study') || words.includes('read')) label = 'study';
  if (words.includes('buy') || words.includes('shop')) label = 'shopping';
  if (words.includes('clean') || words.includes('wash')) label = 'housekeeping';
  const next = (new Date().getHours() < 9) ? 9 : (new Date().getHours() < 12) ? new Date().getHours() + 1 : 18;
  alert(`AI label: "${label}"  –  best hour: ${next}`);
}

// ----------  Google Calendar export  ----------
async function exportGCal() {
  const note = notes[0];
  if (!note) return;
  if (!gapi.client) { $('calMsg').textContent = 'Google not loaded'; return; }
  const event = {
    summary: 'Coach: ' + note.title,
    start: { dateTime: new Date().toISOString(), timeZone: 'Asia/Kolkata' },
    end: { dateTime: new Date(Date.now() + 30 * 60000).toISOString(), timeZone: 'Asia/Kolkata' }
  };
  await gapi.client.calendar.events.insert({ calendarId: 'primary', resource: event });
  $('calMsg').textContent = 'Added to Google Calendar ✔';
}

// ----------  init  ----------
window.onload = () => {
  loadToday();
  renderNotes();
  // load Google API (optional)
  const script = document.createElement('script');
  script.src = 'https://apis.google.com/js/api.js';
  script.onload = () => gapi.load('client:auth2', () => gapi.client.init({
    apiKey: GCAL_API_KEY,
    clientId: GCAL_CLIENT_ID,
    discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'],
    scope: 'https://www.googleapis.com/auth/calendar'
  }));
  document.head.appendChild(script);
};