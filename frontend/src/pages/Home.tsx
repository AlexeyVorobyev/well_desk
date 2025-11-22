import { Grid, Stack, Typography } from '@mui/material';
import { KnowledgeBase } from '../components/KnowledgeBase';
import { MessagesPanel } from '../components/MessagesPanel';
import { ProfileForm } from '../components/ProfileForm';
import { WellbeingForm } from '../components/WellbeingForm';

export function HomePage() {
  return (
    <Stack spacing={3}>
      <Stack spacing={1}>
        <Typography variant="h4" component="h1">
          WellDesk
        </Typography>
        <Typography color="text.secondary">
          Помощник фиксирует ваши сообщения, оценивает состояние и подсказывает короткие шаги для
          восстановления фокуса и снижения усталости.
        </Typography>
      </Stack>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <ProfileForm />
        </Grid>
        <Grid item xs={12} md={6}>
          <WellbeingForm />
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid item xs={12} md={5}>
          <MessagesPanel />
        </Grid>
        <Grid item xs={12} md={7}>
          <KnowledgeBase />
        </Grid>
      </Grid>
    </Stack>
  );
}
