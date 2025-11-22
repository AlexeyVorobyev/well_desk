import { LoadingButton } from '@mui/lab';
import {
  Alert,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { getProfile, upsertProfile } from '../api/profile';
import type { UserProfileInput } from '../api/types';

function toInput(profile?: UserProfileInput | null): UserProfileInput {
  return {
    age: profile?.age ?? undefined,
    role: profile?.role ?? '',
    work_style: profile?.work_style ?? '',
    work_hours_from: profile?.work_hours_from ?? '',
    work_hours_to: profile?.work_hours_to ?? '',
    break_interval_minutes: profile?.break_interval_minutes ?? undefined,
    screen_break_preference: profile?.screen_break_preference ?? '',
  };
}

export function ProfileForm() {
  const queryClient = useQueryClient();
  const { data, isFetching, error } = useQuery({ queryKey: ['profile'], queryFn: getProfile });
  const [form, setForm] = useState<UserProfileInput>(toInput());
  const isEmptyProfile = data === null && !isFetching;

  const mutation = useMutation({
    mutationFn: upsertProfile,
    onSuccess: (profile) => {
      queryClient.setQueryData(['profile'], profile);
    },
  });

  useEffect(() => {
    setForm(toInput(data ?? undefined));
  }, [data]);

  const handleChange = (field: keyof UserProfileInput) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setForm((prev) => ({
      ...prev,
      [field]: value === '' ? undefined : isNaN(Number(value)) ? value : Number(value),
    }));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    mutation.mutate(form);
  };

  return (
    <Card>
      <CardHeader
        title="Профиль"
        subheader="Заполните базовые данные, чтобы рекомендации стали персонализированными"
      />
      <CardContent>
        <Stack spacing={2} component="form" onSubmit={handleSubmit}>
          {error ? <Alert severity="error">Не удалось загрузить профиль</Alert> : null}
          {isEmptyProfile ? (
            <Alert severity="info">Профиль пока не заполнен. Добавьте данные, чтобы начать.</Alert>
          ) : null}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                label="Возраст"
                type="number"
                fullWidth
                value={form.age ?? ''}
                onChange={handleChange('age')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                label="Роль / род занятий"
                fullWidth
                value={form.role ?? ''}
                onChange={handleChange('role')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                label="Стиль работы"
                placeholder="например, офис / удалённо"
                fullWidth
                value={form.work_style ?? ''}
                onChange={handleChange('work_style')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                label="Начало рабочего дня"
                placeholder="09:00"
                fullWidth
                value={form.work_hours_from ?? ''}
                onChange={handleChange('work_hours_from')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                label="Конец рабочего дня"
                placeholder="18:00"
                fullWidth
                value={form.work_hours_to ?? ''}
                onChange={handleChange('work_hours_to')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                label="Перерыв каждые (мин)"
                type="number"
                fullWidth
                value={form.break_interval_minutes ?? ''}
                onChange={handleChange('break_interval_minutes')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
            <Grid item xs={12} md={8}>
              <TextField
                label="Предпочтения по перерывам"
                placeholder="короткая прогулка, разминка для плеч"
                fullWidth
                value={form.screen_break_preference ?? ''}
                onChange={handleChange('screen_break_preference')}
                disabled={isFetching || mutation.isPending}
              />
            </Grid>
          </Grid>
          <Stack direction="row" spacing={2} alignItems="center">
            <LoadingButton type="submit" variant="contained" loading={mutation.isPending}>
              Сохранить профиль
            </LoadingButton>
            {data?.updated_at ? (
              <Typography variant="body2" color="text.secondary">
                Обновлено: {new Date(data.updated_at).toLocaleString()}
              </Typography>
            ) : null}
            {mutation.isSuccess ? (
              <Typography variant="body2" color="success.main">
                Профиль сохранён
              </Typography>
            ) : null}
            {mutation.isError ? (
              <Typography variant="body2" color="error.main">
                {mutation.error instanceof Error ? mutation.error.message : 'Ошибка сохранения'}
              </Typography>
            ) : null}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
