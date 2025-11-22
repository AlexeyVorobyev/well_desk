import { buildApiUrl } from './client';
import type { UserProfile, UserProfileInput } from './types';

async function fetchJson<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Request failed');
  }
  return response.json() as Promise<T>;
}

export async function getProfile(): Promise<UserProfile | null> {
  const response = await fetch(buildApiUrl('/profile'));
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Не удалось загрузить профиль');
  }
  return response.json();
}

export async function upsertProfile(payload: UserProfileInput): Promise<UserProfile> {
  return fetchJson<UserProfile>(buildApiUrl('/profile'), {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
