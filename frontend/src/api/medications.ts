import { buildApiUrl } from './client';
import type {
  MedicationLog,
  MedicationLogInput,
  MedicationReminder,
  MedicationReminderInput,
} from './types';

async function fetchJson<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Request failed');
  }
  return response.json() as Promise<T>;
}

export async function getMedicationReminders(): Promise<MedicationReminder[]> {
  return fetchJson<MedicationReminder[]>(buildApiUrl('/medications'));
}

export async function createMedicationReminder(
  payload: MedicationReminderInput,
): Promise<MedicationReminder> {
  return fetchJson<MedicationReminder>(buildApiUrl('/medications'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}

export async function deleteMedicationReminder(reminderId: string): Promise<void> {
  const response = await fetch(buildApiUrl(`/medications/${reminderId}`), {
    method: 'DELETE',
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Не удалось удалить напоминание');
  }
}

export async function logMedication(
  reminderId: string,
  payload: MedicationLogInput,
): Promise<MedicationLog> {
  return fetchJson<MedicationLog>(buildApiUrl(`/medications/${reminderId}/log`), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}

export async function getMedicationLogs(days = 7): Promise<MedicationLog[]> {
  const search = new URLSearchParams({ days: String(days) });
  return fetchJson<MedicationLog[]>(buildApiUrl(`/medications/logs?${search.toString()}`));
}
