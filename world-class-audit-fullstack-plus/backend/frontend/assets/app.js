
async function postForm(url, data) {
  const res = await fetch(url, { method: 'POST', body: data });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

const form = document.getElementById('auditForm');
const results = document.getElementById('results');
const summary = document.getElementById('summary');
const pages = document.getElementById('pages');
const pdfForm = document.getElementById('pdfForm');
const pdfUrl = document.getElementById('pdf_url');
const pdfMax = document.getElementById('pdf_max_pages');
const pdfTimeout = document.getElementById('pdf_timeout');

function renderSummary(data) {
  const robots = data.summary.robots || {}; 
  const sitemap = data.sitemap || {}; 
  summary.innerHTML = `<h3>Summary</h3>
    <ul>
      <li>Total pages: ${data.summary.total_pages}</li>
      <li>OK responses: ${data.summary.ok_responses}</li>
      <li>Robots.txt: ${robots.present ? 'present' : 'missing'} (${robots.url || ''})</li>
      <li>Sitemap URLs found: ${(sitemap.urls || []).length}</li>
    </ul>`;
}

function renderPages(data) {
  pages.innerHTML = '<h3>Pages</h3>';
  Object.entries(data.pages).forEach(([url, page]) => {
    const sec = page.security;
    const https = page.https;
    const seo = page.seo;
    const acc = page.accessibility;
    const perf = page.performance;
    const broken = page.broken_links || [];
    const div = document.createElement('div');
    div.className = 'page-block';
    div.innerHTML = `
      <h4><a href="${url}" target="_blank">${url}</a> <small>(status: ${page.status})</small></h4>
      <details open><summary>HTTPS / Security</summary>
        <p><strong>HSTS:</strong> ${https.hsts}</p>
        <p><strong>Mixed content on HTTPS:</strong> ${https.mixed_content.length}</p>
        <p><strong>Missing headers:</strong> ${sec.missing.join(', ')}</p>
        <p><strong>Recommendations:</strong> ${sec.recommendations.join('; ')}</p>
      </details>
      <details><summary>SEO</summary>
        <ul>
          <li>Title (${seo.title_length} chars): ${seo.title}</li>
          <li>Meta description (${seo.meta_description_length} chars): ${seo.meta_description}</li>
          <li>Has H1: ${seo.has_h1}</li>
          <li>Canonical: ${seo.canonical}</li>
          <li>Robots: ${seo.robots}</li>
          <li>Structured data: ${seo.has_structured_data}</li>
          <li>OG title meta: ${seo.has_og_title}</li>
        </ul>
      </details>
      <details><summary>Accessibility</summary>
        <ul>
          <li>Images without alt: ${acc.images_without_alt_count}</li>
          <li>Has HTML lang attribute: ${acc.has_lang_attribute}</li>
          <li>Labeled inputs / total inputs: ${acc.label_to_input_ratio[0]} / ${acc.label_to_input_ratio[1]}</li>
        </ul>
      </details>
      <details><summary>Performance</summary>
        <ul>
          <li>TTFB (ms): ${Number(perf.ttfb_ms).toFixed(1)}</li>
          <li>Resources: scripts ${perf.resources.scripts}, stylesheets ${perf.resources.stylesheets}, images ${perf.resources.images}</li>
          <li>Estimated page weight (bytes): ${perf.page_weight_bytes_est}</li>
        </ul>
      </details>
      <details><summary>Broken Links</summary>
        ${broken.length === 0 ? '<p>None</p>' : '<ul>' + broken.map(b => `<li>${b[0]} — ${b[1]}</li>`).join('') + '</ul>'}
      </details>
    `;
    pages.appendChild(div);
  });
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const target = fd.get('url');
  results.hidden = true;
  summary.innerHTML = 'Running audit...';
  pages.innerHTML = '';
  try {
    const data = await postForm('/audit', fd);
    results.hidden = false;
    pdfUrl.value = target;
    pdfMax.value = fd.get('max_pages');
    pdfTimeout.value = fd.get('timeout');
    renderSummary(data);
    renderPages(data);
  } catch (err) {
    summary.innerHTML = 'Error: ' + err.message;
  }
});

pdfForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(pdfForm);
  try {
    const data = await postForm('/audit/pdf', fd);
    if (data.pdf) {
      const a = document.createElement('a');
      a.href = '/' + data.pdf; // path inside the container
      a.download = 'audit.pdf';
      a.textContent = 'Download audit.pdf';
      pdfForm.appendChild(a);
    }
  } catch (err) {
    alert('PDF generation failed: ' + err.message);
  }
});
