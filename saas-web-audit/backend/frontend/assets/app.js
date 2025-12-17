
let token = '';

async function postJSON(url, data) {
  const res = await fetch(url, { method: 'POST', headers: {
    'Content-Type': 'application/json', ...(token ? {'Authorization': 'Bearer ' + token} : {})
  }, body: JSON.stringify(data) });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  try {
    const data = await postJSON('/auth/login', { email, password });
    token = data.access_token;
    alert('Logged in');
  } catch (err) { alert('Login failed: ' + err.message); }
});

document.getElementById('runBtn').addEventListener('click', async () => {
  const websiteId = document.getElementById('websiteId').value;
  const domain = document.getElementById('domain').value;
  try {
    const res = await postJSON('/audits/run?website_id=' + encodeURIComponent(websiteId) + '&max_pages=25&timeout=15', {});
    alert('Queued audit ' + res.audit_run_id);
  } catch (err) {
    alert('Audit failed: ' + err.message);
  }
});
