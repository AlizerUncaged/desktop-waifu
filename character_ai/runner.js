const yandereGf = "_PjRfiokij64UvriwbB7QCZ_QJfSoKXh1U7WqMT1A98"
const port = 40001
const readlineSync = require('readline-sync')
const WebSocket = require('ws')
var CharacterAI = require('./client')
global.client = new CharacterAI()

const wss = new WebSocket.Server({ port: port });

wss.on('connection', (ws) => {
    console.log('A client connected');

    ws.on('message', async (message) => {

        let chatMessage = message.toString('utf8');

        console.log(`Received message: ${chatMessage}`);

        const response = await global.yandereRoom.sendAndAwaitResponse(chatMessage, true)

        console.log(`Character: ${response.text}`);

        ws.send(`${response.text}`);
    });

});

async function main() {
    await global.client.authenticateAsGuest();

    console.log(`Authenticated, fetching character AI info....`);

    var characterInfo = await global.client.fetchCharacterInfo(yandereGf);

    global.yandereRoom = await global.client.createOrContinueChat(yandereGf);

    console.log(`Character Name: ${characterInfo.name ?? "<Unkown>"}`);
    console.log(`Greeting: ${characterInfo.greeting ?? "<Unkown>"}`);
    console.log(`Character Id: ${global.yandereRoom.characterId ?? "<Unkown>"}`);
}

main();