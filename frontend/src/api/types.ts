export type UserProfileInput = {
  age?: number;
  role?: string;
  work_style?: string;
  work_hours_from?: string;
  work_hours_to?: string;
  break_interval_minutes?: number;
  screen_break_preference?: string;
};

export type UserProfile = UserProfileInput & {
  id: string;
  created_at: string;
  updated_at: string;
};

export type Message = {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  reply_to_id?: number | null;
  created_at: string;
};

export type MessageUserInput = {
  content: string;
};

export type LLMMessageInput = {
  user_message_id: number;
};

export type WellbeingInput = {
  energy: number;
  stress: number;
  focus: number;
  mood: string;
  note?: string;
};

export type Wellbeing = WellbeingInput & {
  updated_at: string;
};

export type MedicationReminderInput = {
  title: string;
  time: string;
  frequency: string;
};

export type MedicationReminder = MedicationReminderInput & {
  id: string;
  created_at: string;
};

export type MedicationLogInput = {
  taken: boolean;
};

export type MedicationLog = {
  id: string;
  reminder_id: string;
  taken: boolean;
  timestamp: string;
  reminder_title?: string | null;
  reminder_time?: string | null;
};
