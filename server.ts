import { WebSocketServer, WebSocket } from 'ws';
import activeWindow from 'active-win'
import { activeWindowSchema } from './src/lib/schema'

const wss = new WebSocketServer({ port: 8080 });

const users: WebSocket[] = []

const interval = 5; //seconds
wss.on('connection', function connection(ws) {
  // TODO: negate if statement
  if (true) {
    users.push(ws)
    setInterval(async () => {
      const windowData = await activeWindow()
      try {
        const data = activeWindowSchema.parse({
          title: windowData?.title,
          app: windowData?.owner.name,
          time: interval,
        })
        ws.send(JSON.stringify(data))
      } catch(err) {
        console.error(err)
      }
    }, interval * 1000)
  }

  ws.on('close', (idk) => {
    console.log(idk)
  })
  ws.on('error', console.error);
  ws.on('message', function message(data) {
    console.log('received: %s', data);
  });
});
