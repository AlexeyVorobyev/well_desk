import { Card, CardContent, CardHeader, Chip, Grid, List, ListItem, ListItemText } from '@mui/material';

const topics = [
  {
    title: 'Здоровый сон',
    tips: ['Ложитесь в одно и то же время', 'Уберите экраны за 60 минут до сна', 'Короткая растяжка перед сном снижает напряжение'],
  },
  {
    title: 'Разгрузка зрения',
    tips: ['Правило 20-20-20 каждые 20 минут', 'Увлажняйте глаза морганием', 'Отодвиньте монитор на расстояние вытянутой руки'],
  },
  {
    title: 'Освобождение шеи и спины',
    tips: ['Каждый час делайте круговые движения плечами', 'Поставьте ноги на опору, чтобы снять нагрузку со спины', 'Держите экран на уровне глаз'],
  },
  {
    title: 'Фокус и продуктивность',
    tips: ['Разбивайте задачи на 25-минутные спринты', 'Фиксируйте 1–3 ключевые цели на день', 'Делайте мини-паузы для дыхания перед переключением задач'],
  },
  {
    title: 'Снижение тревожности',
    tips: ['4–5 циклов глубокого дыхания', 'Короткая прогулка на свежем воздухе', 'Запишите волнующие мысли и вернитесь к ним позже'],
  },
];

export function KnowledgeBase() {
  return (
    <Card>
      <CardHeader title="База знаний" subheader="Краткие материалы для быстрой разгрузки" />
      <CardContent>
        <Grid container spacing={2}>
          {topics.map((topic) => (
            <Grid item xs={12} md={6} key={topic.title}>
              <Card variant="outlined">
                <CardHeader title={topic.title} action={<Chip label="1-2 мин" size="small" />} />
                <CardContent>
                  <List dense>
                    {topic.tips.map((tip) => (
                      <ListItem key={tip}>
                        <ListItemText primary={tip} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
}
