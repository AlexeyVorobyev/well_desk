import { LoadingButton } from '@mui/lab';
import {
  Alert,
  Avatar,
  Card,
  CardContent,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useMemo, useState } from 'react';
import { getMessages, requestAssistantMessage, sendUserMessage } from '../api/messages';
import type { Message } from '../api/types';

function sortMessages(messages?: Message[]) {
  return [...(messages ?? [])].sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
  );
}

export function MessagesPanel() {
  const queryClient = useQueryClient();
  const { data, error, isFetching } = useQuery({ queryKey: ['messages'], queryFn: getMessages });
  const [content, setContent] = useState('');

  const sendMutation = useMutation({
    mutationFn: sendUserMessage,
    onSuccess: async (message) => {
      queryClient.setQueryData<Message[]>(['messages'], (prev = []) => [...prev, message]);
      setContent('');
      try {
        const assistant = await requestAssistantMessage({ user_message_id: message.id });
        queryClient.setQueryData<Message[]>(['messages'], (prev = []) => [...prev, assistant]);
      } catch (assistantError) {
        console.error(assistantError);
      }
    },
  });

  const ordered = useMemo(() => sortMessages(data), [data]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!content.trim()) {
      return;
    }
    sendMutation.mutate({ content });
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardHeader
        title="Диалог с ассистентом"
        subheader="Ассистент анализирует сообщения и фиксирует ключевые признаки"
      />
      <CardContent sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {error ? <Alert severity="error">Не удалось загрузить сообщения</Alert> : null}
        <List sx={{ maxHeight: 320, overflow: 'auto' }}>
          {ordered.map((message) => (
            <ListItem key={message.id} alignItems="flex-start">
              <ListItemAvatar>
                <Avatar>{message.role === 'assistant' ? 'A' : 'U'}</Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Stack direction="row" spacing={1} alignItems="center">
                    <Typography fontWeight={600}>{message.role === 'assistant' ? 'Ассистент' : 'Вы'}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(message.created_at).toLocaleString()}
                    </Typography>
                  </Stack>
                }
                secondary={message.content}
              />
            </ListItem>
          ))}
          {ordered.length === 0 && !isFetching ? (
            <Typography variant="body2" color="text.secondary" px={2} py={1}>
              Сообщений пока нет. Расскажите, как вы себя чувствуете.
            </Typography>
          ) : null}
        </List>
        <Divider />
        <Stack component="form" onSubmit={handleSubmit} spacing={1}>
          <TextField
            label="Ваше сообщение"
            value={content}
            onChange={(event) => setContent(event.target.value)}
            multiline
            minRows={2}
            disabled={sendMutation.isPending}
            placeholder="Опишите усталость, настроение или запрос на рекомендации"
          />
          <LoadingButton type="submit" variant="contained" loading={sendMutation.isPending}>
            Отправить и получить совет
          </LoadingButton>
          {sendMutation.isError ? (
            <Typography variant="body2" color="error.main">
              {sendMutation.error instanceof Error
                ? sendMutation.error.message
                : 'Не удалось отправить сообщение'}
            </Typography>
          ) : null}
        </Stack>
      </CardContent>
    </Card>
  );
}
