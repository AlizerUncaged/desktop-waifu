This project is suceeded by https://github.com/AlizerUncaged/waifu-desktop, check it out! 
<div>
  <img width="220" align="left" src="https://i.ibb.co/gvGbYB5/icon.png"/>
  <br>
  <h1>🌟 AI Waifu Assistant</h1>
  <p>
    💬 Your ultimate companion!
    <br>
  </p>
</div>

## 🤔 The Goal
By harnessing the power of the current technologies we have, we can turn the voices in our heads into reality.

## ✨ Features
- 💬 Easy to Use: AI Waifu Assistant is very user-friendly, even for those who are not tech-savvy.
- 🗣️ Casual Conversations: AI Waifu Assistant is perfect for roleplaying, asking questions, or just having a casual conversation with your own waifu. You can talk to her about anything and everything under the sun!
- 🎨 Customizable Characters: With the help of vtuber-studio, you can easily create your own character and give them a unique look that matches your personality. The perfect way to give voice to your inner demons, without actually summoning them in the physical world.
- 🧩 Modular and customizable! Want to use ElevenLabs for the voice instead of Voicevox? Want to change the output language to English? Do it your way!

## 🚀 Running
Running AI Waifu Assistant is easy and straightforward! Here's how you can get started:

📌 Requirements:

- Windows 7 x64 or above.
- [Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) for Visual Studio 2015, 2017 and 2019.
- [VTube Studio](https://denchisoft.com/), works on any OS both mobile and desktop.
- OpenAI API key, you can find it [here](https://platform.openai.com/account/api-keys).
### ⚙️ Optional
- Elevenlabs key, you can find it [here](https://beta.elevenlabs.io/subscription).

📥 Running:

- First, you need to download this repository. You can do this by [clicking here](https://github.com/AlizerUncaged/desktop-waifu/archive/refs/heads/master.zip).
- Once the download is complete, extract the contents of the ZIP file to a location on your computer where you can easily find it.
- Next, you'll need to make some changes to a file called ``example.env``. This file is located in the same folder where you extracted the ZIP file. You can open it with a text editor like Notepad.
- Look for the line that says ``OPENAI_KEY`` and replace the text after the equals sign with your own OpenAI key. You'll also need to change the ``ELEVENLABS_KEY`` to yours. If you're not using Elevenlabs, you can change the ``VOICE`` variable to ``voicevox``.
- Then open ``character_ai\runner.js`` and look for ``authenticateWithToken("")`` add your Character.AI ``char_token`` in the quotation marks. Which can be found by opening Developer Tools, and going to Application and finding Local Storage on the [beta.character.ai](https://beta.character.ai/) website. YOU MUST BE SIGNED IN TO SEE "char_token"!!!
- Next you wanna find and click on a character of your choice. Up top in the URL address bar you will see ``?char=`` copy the character ID after that, and ignore ``&source=recent-chats`` after that, you just want the ID.
- Open ``example.env`` and paste the Character.AI ID into the ``CHARACTERAI_CHARACTER=`` field.
- And don't forget to change python's path inside ``waifu\pyvenv.cfg`` to your installed location. A typical installed python path is located at ``C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310``.
- After that, you need to run a program called "VTube Studio" and enable API access. You can do this by going to the settings menu and selecting the option on the right side. Make sure the port number is set to "8001".

<div>
<center>
    <img align="center" src="https://i.ibb.co/b65QD9H/image.png"/>
</center>
<br/>
</div>

- Finally, double-click the "start.bat" file that's located in the same folder where you extracted the ZIP file. This will automatically download all dependencies and start the program.

### ⚙️ Optional
🔥 CUDA:

- Start by downloading and installing the [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) cuda_12.3.2_546.12_windows.exe
- Open a waifu environment and uninstall PyTorch ``pip uninstall pytorch``. Run the "start.bat" and press "control+c" and terminate the batch job.
- Then go to the [PyTorch website](https://pytorch.org/) and scroll down until you see the install PyTorch section. Select the newest version of CUDA available (currently CUDA 12.1 Version), despite the non matching NVIDIA CUDA Toolkit version.
- Copy and paste the command from the website. Just don't forget to remove the little 3 from ``pip3`` before running the command again in the waifu enviroment.
- Lastly change ``TORCH_DEVICE=cpu`` to ``TORCH_DEVICE=cuda`` inside the ``example.env`` file.
- Pray and run the "start.bat" file.

If you run into any problems, you can go to the following website to report issues: https://github.com/AlizerUncaged/desktop-waifu/issues/new.

## 💡 Goals
✔️ - Fully Implemented, 🚧 Partially Implemented, ❌ - Not Implemented yet

| Feature               | State |
|-----------------------|-------|
| Basic Functionality   | ✔️     |
| Fully Automatic Setup | 🚧     |
| GUI                   | ❌     |

## 🤝 Contributions
AI Waifu Assistant is an open-source project, and we welcome any contributions from the community to make it even better! Here are some ways you can contribute:

👉 Bug Reporting: If you encounter any bugs while using the app, please report them in the issues section of the repository. Make sure to provide a clear description of the issue and steps to reproduce it.

🔨 Pull Requests: If you have a fix or improvement that you would like to contribute, you can create a pull request. We encourage you to read the contribution guidelines before creating a pull request.

📈 Feature Requests: We also welcome feature requests from the community. If you have an idea for a new feature or improvement, you can submit it in the issues section of the repository.

We appreciate any contributions that can help make AI Waifu Assistant a better app for everyone to enjoy!

## 🎁 Credits
Massive thanks to these projects I've used/referenced.

[Node-CharacterAI](https://github.com/realcoloride/node_characterai) - Unofficial Character AI API library.
