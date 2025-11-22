import { LoadingButton } from '@mui/lab';
import {
  Alert,
  Box,
  Button,
  Chip,
  Divider,
  Grid,
  IconButton,
  Paper,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography,
} from '@mui/material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useMemo, useState } from 'react';
import {
  createMedicationReminder,
  deleteMedicationReminder,
  getMedicationLogs,
  getMedicationReminders,
  logMedication,
} from '../api/medications';
import type {
  MedicationLog,
  MedicationReminder,
  MedicationReminderInput,
} from '../api/types';
import DeleteIcon from '@mui/icons-material/Delete';

const frequencyOptions = [
  { value: 'daily', label: 'Ежедневно' },
  { value: 'weekly', label: 'Еженедельно' },
  { value: 'every_8_hours', label: 'Каждые 8 часов' },
];

function buildLatestLogMap(logs?: MedicationLog[]) {
  const map = new Map<string, MedicationLog>();
  if (!logs) return map;

  const ordered = [...logs].sort(
    (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime(),
  );

  for (const log of ordered) {
    if (!map.has(log.reminder_id)) {
      map.set(log.reminder_id, log);
    }
  }

  return map;
}

export function MedicationRemindersDock() {
  const queryClient = useQueryClient();
  const remindersQuery = useQuery({
    queryKey: ['medications'],
    queryFn: getMedicationReminders,
    refetchInterval: 12000,
  });
  const logsQuery = useQuery({
    queryKey: ['medicationLogs'],
    queryFn: () => getMedicationLogs(7),
    refetchInterval: 12000,
  });

  const [form, setForm] = useState<MedicationReminderInput>({
    title: '',
    time: '09:00',
    frequency: frequencyOptions[0].value,
  });

  const [historyTab, setHistoryTab] = useState<'done' | 'missed'>('done');

  const latestLogByReminder = useMemo(() => buildLatestLogMap(logsQuery.data), [
    logsQuery.data,
  ]);

  const filteredLogs = useMemo(() => {
    const source = logsQuery.data ?? [];
    return source.filter((log) => (historyTab === 'done' ? log.taken : !log.taken));
  }, [historyTab, logsQuery.data]);

  const createMutation = useMutation({
    mutationFn: createMedicationReminder,
    onSuccess: (reminder) => {
      queryClient.setQueryData<MedicationReminder[]>(['medications'], (prev = []) => [
        ...prev,
        reminder,
      ]);
      setForm({ title: '', time: '09:00', frequency: frequencyOptions[0].value });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteMedicationReminder,
    onSuccess: (_, reminderId) => {
      queryClient.setQueryData<MedicationReminder[]>(['medications'], (prev = []) =>
        (prev ?? []).filter((item) => item.id !== reminderId),
      );
      queryClient.setQueryData<MedicationLog[]>(['medicationLogs'], (prev = []) =>
        (prev ?? []).filter((log) => log.reminder_id !== reminderId),
      );
    },
  });

  const logMutation = useMutation({
    mutationFn: ({ reminderId, taken }: { reminderId: string; taken: boolean }) =>
      logMedication(reminderId, { taken }),
    onSuccess: (log) => {
      queryClient.setQueryData<MedicationLog[]>(['medicationLogs'], (prev = []) => [
        log,
        ...(prev ?? []),
      ]);
    },
  });

  const handleCreate = (event: React.FormEvent) => {
    event.preventDefault();
    if (!form.title.trim()) return;
    createMutation.mutate(form);
  };

  const handleDelete = (reminderId: string) => {
    deleteMutation.mutate(reminderId);
  };

  const handleLog = (reminderId: string, taken: boolean) => {
    logMutation.mutate({ reminderId, taken });
  };

  return (
    <Paper
      variant="outlined"
      sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, borderTopWidth: 2, zIndex: 10 }}
    >
      <Box px={{ xs: 2, md: 4 }} py={2}>
        <Stack spacing={2}>
          <Stack direction={{ xs: 'column', md: 'row' }} alignItems={{ md: 'center' }} justifyContent="space-between">
            <Stack spacing={0.5}>
              <Typography variant="h6">Напоминания</Typography>
              <Typography color="text.secondary">
                Создавайте напоминания о приёме лекарств и отмечайте статус выполнения.
              </Typography>
            </Stack>
            {remindersQuery.error || logsQuery.error ? (
              <Alert severity="error">Не удалось загрузить данные по напоминаниям</Alert>
            ) : null}
          </Stack>

          <Grid container spacing={2}>
            <Grid item xs={12} md={5}>
              <Stack component="form" onSubmit={handleCreate} spacing={1.5}>
                <TextField
                  label="Название лекарства"
                  value={form.title}
                  onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
                  required
                  disabled={createMutation.isPending}
                />
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1}>
                  <TextField
                    type="time"
                    label="Время"
                    value={form.time}
                    onChange={(event) => setForm((prev) => ({ ...prev, time: event.target.value }))}
                    InputLabelProps={{ shrink: true }}
                    sx={{ minWidth: 160 }}
                    disabled={createMutation.isPending}
                  />
                  <TextField
                    select
                    label="Частота"
                    value={form.frequency}
                    onChange={(event) => setForm((prev) => ({ ...prev, frequency: event.target.value }))}
                    SelectProps={{ native: true }}
                    sx={{ minWidth: 200 }}
                    disabled={createMutation.isPending}
                  >
                    {frequencyOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </TextField>
                </Stack>
                <LoadingButton type="submit" variant="contained" loading={createMutation.isPending}>
                  Создать напоминание
                </LoadingButton>
              </Stack>
            </Grid>

            <Grid item xs={12} md={7}>
              <Stack spacing={1}>
                <Typography fontWeight={600}>Текущие напоминания</Typography>
                <Stack spacing={1} maxHeight={200} sx={{ overflow: 'auto' }}>
                  {(remindersQuery.data ?? []).map((reminder) => {
                    const latestLog = latestLogByReminder.get(reminder.id);
                    const chipColor = latestLog
                      ? latestLog.taken
                        ? 'success'
                        : 'error'
                      : 'default';
                    const chipLabel = latestLog
                      ? latestLog.taken
                        ? 'Выполнено'
                        : 'Пропущено'
                      : 'Нет отметок';

                    return (
                      <Paper
                        key={reminder.id}
                        variant="outlined"
                        sx={{ p: 1, borderColor: 'divider' }}
                      >
                        <Stack direction="row" spacing={1.5} alignItems="center" justifyContent="space-between">
                          <Stack spacing={0.5}>
                            <Typography fontWeight={600}>{reminder.title}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              {reminder.time} · {reminder.frequency}
                            </Typography>
                            <Chip label={chipLabel} color={chipColor} size="small" />
                          </Stack>
                          <Stack direction="row" spacing={1} alignItems="center">
                            <Button
                              variant="contained"
                              color="success"
                              size="small"
                              onClick={() => handleLog(reminder.id, true)}
                              disabled={logMutation.isPending}
                            >
                              Выполнено
                            </Button>
                            <Button
                              variant="outlined"
                              color="error"
                              size="small"
                              onClick={() => handleLog(reminder.id, false)}
                              disabled={logMutation.isPending}
                            >
                              Пропущено
                            </Button>
                            <IconButton
                              aria-label="Удалить"
                              onClick={() => handleDelete(reminder.id)}
                              disabled={deleteMutation.isPending}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Stack>
                        </Stack>
                      </Paper>
                    );
                  })}

                  {(remindersQuery.data?.length ?? 0) === 0 ? (
                    <Typography variant="body2" color="text.secondary">
                      Напоминаний пока нет. Добавьте первое, чтобы начать отслеживание.
                    </Typography>
                  ) : null}
                </Stack>
              </Stack>
            </Grid>
          </Grid>

          <Divider />

          <Stack spacing={1}>
            <Stack direction="row" alignItems="center" spacing={1}>
              <Typography fontWeight={600}>История за 7 дней</Typography>
              <Tabs
                value={historyTab}
                onChange={(_, value) => setHistoryTab(value as 'done' | 'missed')}
                indicatorColor={historyTab === 'done' ? 'success' : 'error'}
                textColor="inherit"
                sx={{ minHeight: 36, '& .MuiTab-root': { minHeight: 36 } }}
              >
                <Tab value="done" label="🟢 Выполнено" />
                <Tab value="missed" label="🔴 Не выполнено" />
              </Tabs>
            </Stack>

            <Stack spacing={1} maxHeight={180} sx={{ overflow: 'auto' }}>
              {filteredLogs.map((log) => (
                <Paper
                  key={log.id}
                  sx={{
                    p: 1,
                    backgroundColor: log.taken ? 'success.light' : 'error.light',
                    color: log.taken ? 'success.contrastText' : 'error.contrastText',
                  }}
                >
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Stack spacing={0.25}>
                      <Typography fontWeight={600}>{log.reminder_title ?? 'Напоминание'}</Typography>
                      <Typography variant="body2">
                        {log.reminder_time ? `${log.reminder_time} — ` : ''}
                        {new Date(log.timestamp).toLocaleString()}
                      </Typography>
                    </Stack>
                    <Typography fontWeight={600}>{log.taken ? 'Выполнено' : 'Пропущено'}</Typography>
                  </Stack>
                </Paper>
              ))}

              {filteredLogs.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  История пока пустая.
                </Typography>
              ) : null}
            </Stack>
          </Stack>
        </Stack>
      </Box>
    </Paper>
  );
}
