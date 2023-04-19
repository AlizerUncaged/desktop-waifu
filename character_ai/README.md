# Character AI Unofficial Node API

> Node.js client for the unofficial [Character AI API](https://character.ai/), an awesome website which brings characters to life with AI!

## Intro

This repository is inspired by [RichardDorian's unofficial node API](https://github.com/RichardDorian/node-character.ai/).
Though, I found it hard to use and it was not really stable and archived. So I remade it in javascript.

**This project is not affiliated with Character AI in any way! It is a community project.**
The purpose of this project is to bring and build projects powered by Character AI.

If you like this project, please check their [website](https://character.ai/).

## Features

* 👍 Fully written in Javascript and CommonJS (for max compatibility and ease of use)
* ⌚ Asynchronous requests
* 🗣️ Use conversations or use the API to fetch information
* 🧸 Easy to use
* 🔁 Active development
* 👤 Guest & token login support

## Installation

```bash
npm install node_characterai
```

## Usage

Basic guest login and conversation message:
```js
const CharacterAI = require('node_characterai');
const characterAI = new CharacterAI();

(async() => {
    await characterAI.authenticateAsGuest();

    const characterId = "8_1NyR8w1dOXmI1uWaieQcd147hecbdIK7CeEAIrdJw" // Discord moderator

    const chat = await characterAI.createOrContinueChat(characterId);
    const response = await chat.sendAndAwaitResponse('Hello discord mod!', true)

    console.log(response);
    // use response.text to use it in a string.
})();
```

## Using an Access Token

Some parts of the API, like managing a conversation requires for you to be logged in using an `accessToken`.
To get it, you can open your browser, go to the [character.ai website](https://character.ai) in `localStorage`.

To do so:
1. Open the Character AI website in your browser
2. Open the developer tools `F12` and go to the `Application` tab.
3. Go to the `Storage` section and click on `Local Storage`.
4. Look for the `@@auth0spajs@@::dyD3gE281MqgISG7FuIXYhL2WEknqZzv::https://auth0.character.ai/::openid profile email offline_access` key.
5. Open the body and copy the access token.

![Access_Token](https://i.imgur.com/09Q9mLe.png)

When using the package, you can:
* Login as guest using `authenticateAsGuest()` - *for mass usage or testing purposes*
* Login with your account or a token using `authenticateWithToken()`

## Finding the Character ID

You can find your character ID in the URL of a Character's chat page.
For example, if you go to the chat page of the character `Test Character` you will see the URL `https://character.ai/chat/chat?char=5f7f9b9b9b9b9b9b9b9b9b9b`.

The last part of the URL is the character ID:
![Character_ID](https://i.imgur.com/nd86fN4.png)

## Troubleshooting

|**Problem**|Answer|
|-------|------|
|❌ **Token was invalid**|Make sure your token is actually valid and you copied your entire token (its pretty long).|
|❓ **Fetch is not defined**|Upgrade to node 18 or higher (19 is better) or try installing `node-fetch`.|
|👥 **`authenticateAsGuest()` doesn't work**|See issue [#14](https://github.com/realcoloride/node_characterai/issues/14).|
|🦒 **Hit the max amount of messages?**|Sadly, guest accounts only have a limited amount of messages before they get limited and forced to login. See below for more info 👇|
|🪐 **How to use an account to mass use the library?**|You can use **conversations**, a feature introduced in `1.0.0`, to assign to users and channels. **To reproduce a conversation, use OOC (out of character) to make the AI think you're with multiple people.** __See an example here:__ ![chrome_RDbmXXtFNl](https://user-images.githubusercontent.com/108619637/224778145-284dd89e-7960-499c-b0f0-0deca419c578.png)![chrome_BgF8crPvqC](https://user-images.githubusercontent.com/108619637/224778153-c2a42a26-c5f7-4148-9644-34353482833e.png) (Disclaimer: on some characters, their personality will make them ignore any OOC request).|
|😮 **Why is a chrome window opening?**|This is because as of currently, the simple fetching is broken and I use puppeteer (a chromium browser control library) to go around cloudflare's restrictions.|
|📣 **Is this official?**|No, this project is made by a fan of the website and is unofficial. *To support the developers, please check out [their website](https://beta.character.ai)*.|
|😲 **Did something awesome with `node_characterai`?**|Please let me know!|
|✉️ **Want to contact me?**|See my profile|
|💡 **Have an idea?**|Open an issue in the [**Issues**](https://github.com/realcoloride/node_characterai/issues) tab|
|➕ **Other issue?**|Open an issue in the [**Issues**](https://github.com/realcoloride/node_characterai/issues) tab|

## Disclaimer
##### ❤️ This project is updated frequently, **always check for the latest version for new features or bug fixes**.

🚀 If you have an issue or idea, let me know in the [**Issues**](https://github.com/realcoloride/node_characterai/issues) tab.
📜 If you use this API, you also bound to the terms of usage of their website.

*(real)coloride - 2023, Licensed MIT.*
