import { CssBaseline, ThemeProvider } from '@mui/material';
import { Outlet } from 'react-router-dom';
import { AppLayout } from './components/AppLayout';
import { defaultTheme } from './themes/defaultTheme';

export function App() {
  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <AppLayout>
        <Outlet />
      </AppLayout>
    </ThemeProvider>
  );
}
