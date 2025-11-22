import { AppBar, Box, Container, Toolbar, Typography } from '@mui/material';
import type { PropsWithChildren } from 'react';
import { MedicationRemindersDock } from './MedicationRemindersDock';

export function AppLayout({ children }: PropsWithChildren) {
  return (
    <Box display="flex" flexDirection="column" minHeight="100vh">
      <AppBar position="static" elevation={0} color="transparent">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Well Desk
          </Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flexGrow: 1, py: 4, pb: 16 }}>
        {children}
      </Container>
    </Box>
  );
}
