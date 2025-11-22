import { buildApiUrl } from './client';
import type { Wellbeing, WellbeingInput } from './types';

async function fetchJson<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Request failed');
  }
  return response.json() as Promise<T>;
}

export async function getWellbeing(): Promise<Wellbeing | null> {
  const response = await fetch(buildApiUrl('/wellbeing'));
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Не удалось загрузить данные благополучия');
  }
  return response.json();
}

export async function upsertWellbeing(payload: WellbeingInput): Promise<Wellbeing> {
  return fetchJson<Wellbeing>(buildApiUrl('/wellbeing'), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
