// Klient Seedance (ByteDance) przez API ModelArk: zadanie asynchroniczne, potem odpytywanie statusu.
const BASE_URL = (process.env.ARK_BASE_URL || 'https://ark.ap-southeast.bytepluses.com/api/v3').replace(/\/$/, '');
const MODEL = process.env.SEEDANCE_MODEL || 'dreamina-seedance-2-5-260628';

async function ark(path, init = {}) {
  const key = process.env.ARK_API_KEY;
  if (!key) throw new Error('Brak ARK_API_KEY w .env');
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', ...init.headers },
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body?.error?.message || `ModelArk HTTP ${res.status}`);
  return body;
}

// prompt: opis wideo; imageUrl: opcjonalne zdjęcie produktu (image-to-video)
export async function createVideoTask({ prompt, imageUrl, resolution = '720p', duration = 5, ratio = '16:9' }) {
  const content = [{ type: 'text', text: `${prompt} --resolution ${resolution} --duration ${duration} --ratio ${ratio}` }];
  if (imageUrl) content.push({ type: 'image_url', image_url: { url: imageUrl } });
  const { id } = await ark('/contents/generations/tasks', {
    method: 'POST',
    body: JSON.stringify({ model: MODEL, content }),
  });
  return id;
}

// Zwraca { status: queued|running|succeeded|failed|cancelled, videoUrl?, error? }
export async function getVideoTask(id) {
  const task = await ark(`/contents/generations/tasks/${encodeURIComponent(id)}`);
  return { status: task.status, videoUrl: task.content?.video_url, error: task.error?.message };
}
