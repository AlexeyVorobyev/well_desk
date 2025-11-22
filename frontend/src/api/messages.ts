import { buildApiUrl } from './client';
import type { LLMMessageInput, Message, MessageUserInput } from './types';

async function fetchJson<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Request failed');
  }
  return response.json() as Promise<T>;
}

export async function getMessages(): Promise<Message[]> {
  const response = await fetch(buildApiUrl('/messages'));
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Не удалось загрузить сообщения');
  }
  return response.json();
}

export async function sendUserMessage(payload: MessageUserInput): Promise<Message> {
  return fetchJson<Message>(buildApiUrl('/messages'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}

export async function requestAssistantMessage(payload: LLMMessageInput): Promise<Message> {
  return fetchJson<Message>(buildApiUrl('/messages/llm'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
