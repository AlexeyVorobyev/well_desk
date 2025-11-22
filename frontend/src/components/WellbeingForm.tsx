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
import { getWellbeing, upsertWellbeing } from '../api/wellbeing';
import type { WellbeingInput } from '../api/types';

const defaultForm: WellbeingInput = {
  energy: 3,
  stress: 3,
  focus: 3,
  mood: '',
  note: '',
};

export function WellbeingForm() {
  const queryClient = useQueryClient();
  const { data, isFetching, error } = useQuery({ queryKey: ['wellbeing'], queryFn: getWellbeing });
  const [form, setForm] = useState<WellbeingInput>(defaultForm);

  const mutation = useMutation({
    mutationFn: upsertWellbeing,
    onSuccess: (value) => {
      queryClient.setQueryData(['wellbeing'], value);
    },
  });

  useEffect(() => {
    if (data) {
      setForm({ ...data });
    }
  }, [data]);

  const handleChange = (field: keyof WellbeingInput) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setForm((prev) => ({
      ...prev,
      [field]: field === 'mood' || field === 'note' ? value : Number(value),
    }));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    mutation.mutate(form);
  };

  return (
    <Card>
      <CardHeader
        title="Мини-опросник самочувствия"
        subheader="Оцените текущее состояние, чтобы получить точные рекомендации"
      />
      <CardContent>
        <Stack spacing={2} component="form" onSubmit={handleSubmit}>
          {error ? <Alert severity="error">Не удалось загрузить данные</Alert> : null}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <TextField
                label="Энергия (1-5)"
                type="number"
                inputProps={{ min: 1, max: 5 }}
                value={form.energy}
                onChange={handleChange('energy')}
                fullWidth
                disabled={isFetching || mutation.isPending}
                required
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                label="Стресс (1-5)"
                type="number"
                inputProps={{ min: 1, max: 5 }}
                value={form.stress}
                onChange={handleChange('stress')}
                fullWidth
                disabled={isFetching || mutation.isPending}
                required
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                label="Фокус (1-5)"
                type="number"
                inputProps={{ min: 1, max: 5 }}
                value={form.focus}
                onChange={handleChange('focus')}
                fullWidth
                disabled={isFetching || mutation.isPending}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Настроение"
                fullWidth
                required
                value={form.mood}
                onChange={handleChange('mood')}
                disabled={isFetching || mutation.isPending}
                placeholder="спокойное, взволнованное, уставшее"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Заметка"
                fullWidth
                multiline
                minRows={2}
                value={form.note ?? ''}
                onChange={handleChange('note')}
                disabled={isFetching || mutation.isPending}
                placeholder="что повлияло на ваше состояние?"
              />
            </Grid>
          </Grid>
          <Stack direction="row" spacing={2} alignItems="center">
            <LoadingButton type="submit" variant="contained" loading={mutation.isPending}>
              Сохранить состояние
            </LoadingButton>
            {data?.updated_at ? (
              <Typography variant="body2" color="text.secondary">
                Последнее обновление: {new Date(data.updated_at).toLocaleString()}
              </Typography>
            ) : null}
            {mutation.isSuccess ? (
              <Typography variant="body2" color="success.main">
                Данные сохранены
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
