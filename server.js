import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { createVideoTask, getVideoTask } from './seedance.js';

const PORT = process.env.PORT || 3000;

function json(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(data));
}

async function readJson(req) {
  let raw = '';
  for await (const chunk of req) raw += chunk;
  return raw ? JSON.parse(raw) : {};
}

createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  try {
    if (req.method === 'POST' && url.pathname === '/api/video') {
      const { prompt, imageUrl, resolution, duration, ratio } = await readJson(req);
      if (!prompt) return json(res, 400, { error: 'Podaj prompt' });
      const id = await createVideoTask({ prompt, imageUrl, resolution, duration, ratio });
      return json(res, 202, { id });
    }
    const m = url.pathname.match(/^\/api\/video\/([\w-]+)$/);
    if (req.method === 'GET' && m) return json(res, 200, await getVideoTask(m[1]));
    if (req.method === 'GET' && url.pathname === '/') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(await readFile(new URL('./public/index.html', import.meta.url)));
    }
    json(res, 404, { error: 'Nie znaleziono' });
  } catch (err) {
    json(res, 502, { error: err.message });
  }
}).listen(PORT, () => console.log(`SKLEP działa na http://localhost:${PORT}`));
