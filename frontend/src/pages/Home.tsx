import { Card, CardContent, Stack, Typography } from '@mui/material';

export function HomePage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4" component="h1">
        Добро пожаловать
      </Typography>
      <Card>
        <CardContent>
          <Typography color="text.secondary">
            Здесь появится ваш контент. Структура приложения уже настроена для React, Vite и
            Material UI.
          </Typography>
        </CardContent>
      </Card>
    </Stack>
  );
}
