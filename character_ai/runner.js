let yandereGf = ""

let port = 40102

// the first argument is the port to run on
// the first argument is on index 2 for some reason
if (process.argv.length > 3) {
    port = process.argv[3]
    yandereGf = process.argv[2]
    console.log(`Running on port ${port} with character ${yandereGf}`);
}

const readlineSync = require('readline-sync')
const WebSocket = require('ws')
var CharacterAI = require('./client')
global.client = new CharacterAI()

const wss = new WebSocket.Server({ port: port });

/*
    WebSocket API, for debugging purposes.
*/
wss.on('connection', (ws) => {
    console.log('A client connected');

    ws.on('message', async (message) => {

        if (!global.yandereRoom)
        {
            console.log(`Unable to send message.`)
            console.log(`CharacterAI is still fetching character data!`);
            console.log(`If it's taking far too long please submit an issue.`);
            return
        }

        let chatMessage = message.toString('utf8');

        console.log(`Received message: ${chatMessage}`);

        const response = await global.yandereRoom.sendAndAwaitResponse(chatMessage, true)

        console.log(`Character: ${response.text}`);

        ws.send(`${response.text}`);
    });

});

async function main() {
    console.log(`Authenticating....`);
    await global.client.authenticateAsGuest();

    console.log(`Authenticated, fetching character AI info....`);

    var characterInfo = await global.client.fetchCharacterInfo(yandereGf);

    global.yandereRoom = await global.client.createOrContinueChat(yandereGf);

    console.log(`Character Name: ${characterInfo.name ?? "<Unkown>"}`);
    console.log(`Greeting: ${characterInfo.greeting ?? "<Unkown>"}`);
    console.log(`Character Id: ${global.yandereRoom.characterId ?? "<Unkown>"}`);

    /* while(true)
    {
        const message = readlineSync.question('You > ');
        const response = await global.yandereRoom.sendAndAwaitResponse(message, true)
        console.log('');
    } */
}

main();