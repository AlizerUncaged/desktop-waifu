const { Reply, Message, MessageHistory, OutgoingMessage } = require("./message");
const Parser = require('./parser');

class Chat {
    constructor(client, characterId, continueBody) {
        this.characterId = characterId;
        this.externalId = continueBody.external_id;

        this.client = client;

        const ai = continueBody.participants.find(
            (participant) => participant.is_human === false
        );

        this.aiId = ai.user.username;
        this.requester = client.requester;
    }

    async fetchHistory(pageNumber) {
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');

        // page number is optional
        if (pageNumber) {
            if (typeof (pageNumber) != "number") throw Error("Invalid arguments");
        }

        const client = this.client;

        const pageString = pageNumber ? `&page_num=${pageNumber}` : ''

        const request = await this.requester.request(`https://beta.character.ai/chat/history/msgs/user/?history_external_id=${this.externalId}${pageString}`, {
            headers: client.getHeaders()
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)
            const historyMessages = response.messages;
            const messages = [];

            for (let i = 0; i < historyMessages.length; i++) {
                const message = historyMessages[i];

                messages.push(new Message(this, message));
            }

            const hasMore = response.has_more;
            const nextPage = response.next_page;
            return new MessageHistory(this, messages, hasMore, nextPage);
        } else Error('Could not fetch the chat history.')
    }
    async sendAndAwaitResponse(optionsOrMessage, singleReply) {
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');

        const payload = new OutgoingMessage(this, optionsOrMessage)
        const client = this.client;

        const request = await this.requester.request('https://beta.character.ai/chat/streaming/', {
            body: Parser.stringify(payload),
            method: 'POST',
            headers: client.getHeaders(),
            client: this.client
        }, true)

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request);
            console.log(`response: ${JSON.stringify(response)}`);
            const replies = response.replies;

            const messages = []

            for (let i = 0; i < replies.length; i++) {
                messages.push(new Reply(this, response));
            }

            if (!singleReply) return messages;
            else return messages.pop();
        } else throw Error('Failed sending message.')
    }

    // conversations
    async changeToConversationId(conversationExternalId, force = false) {
        if (typeof (conversationExternalId) != 'string' || typeof (force) != 'boolean') throw Error("Invalid arguments");
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');

        // force means that we dont check if the conversation exists, may lead to errors
        let passing = false;

        if (!force) {
            let conversations = await this.getSavedConversations();
            conversations = conversations.histories;

            for (let i = 0; i < conversations.length; i++) {
                const conversation = conversations[i];
                if (conversation.external_id == conversationExternalId) passing = true;
            }
        } else passing = true;

        if (passing) this.externalId = conversationExternalId;
        else Error("Could not switch to conversation, it either doesn't exist or is invalid.")
    }
    async getSavedConversations(amount = 50) {
        if (typeof (amount) != 'number') throw Error("Invalid arguments");
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');

        const client = this.client;
        const request = await this.requester.request(`https://beta.character.ai/chat/character/histories/`, {
            headers: client.getHeaders(),
            method: 'POST',
            body: Parser.stringify({
                "external_id": this.characterId,
                "number": amount
            })
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            this.externalId = response.external_id;
            return response;
        } else throw Error('Failed saving & creating new chat.')
    }

    // messages
    async getMessageById(messageId) {
        //if (typeof(messageId) != 'string') throw Error('Invalid arguments - (Message ids are now strings)');
        messageId = messageId.toString();
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');

        const history = await this.fetchHistory()
        const historyMessages = history.messages;

        for (let i = 0; i < historyMessages.length; i++) {
            const message = historyMessages[i];

            if (message.id == messageId) return message;
        }
        return null;
    }
    async deleteMessage(messageId) {
        if (typeof (messageId) != 'string') throw Error('Invalid arguments - (Message ids are now strings)');
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');
        if (this.client.isGuest()) throw Error('Guest accounts cannot delete messsages.');

        const client = this.client;
        const request = await this.requester.request(`https://beta.character.ai/chat/history/msgs/delete/`, {
            headers: client.getHeaders(),
            method: 'POST',
            body: Parser.stringify({
                "history_id": this.externalId,
                "ids_to_delete": [messageId],
                "regenerating": false
            })
        })

        let passing = false;

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request);

            if (response.status === 'OK') passing = true;
        }

        if (!passing) throw Error('Failed to delete the message.');
    }
    async deleteMessages(messageIds) {
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');
        if (this.client.isGuest()) throw Error('Guest accounts cannot delete messsages.');

        const messagesToDelete = [];

        try {
            for (let i = 0; i < messageIds.length; i++) {
                const messageId = messageIds[i];

                if (typeof (messageId) == "string") {
                    messagesToDelete.push(messageId);
                }
            }
        } catch (error) {
            throw Error("Failed to delete messages.")
        };

        const client = this.client;
        const request = await this.requester.request(`https://beta.character.ai/chat/history/msgs/delete/`, {
            headers: client.getHeaders(),
            method: 'POST',
            body: Parser.stringify({
                "history_id": this.externalId,
                "ids_to_delete": messagesToDelete,
                "regenerating": false
            })
        })

        let passing = false;

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request);

            if (response.status === 'OK') passing = true;
        }

        if (!passing) throw Error('Failed to delete messages.');
    }
    async deleteMessagesBulk(amount = 50, descending = false) {
        if (typeof (amount) != 'number') throw Error('Invalid arguments');
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');
        if (this.client.isGuest()) throw Error('Guest accounts cannot bulk delete messsages.');

        let idsToDelete = [];

        const history = await this.fetchHistory()
        const historyMessages = history.messages;

        for (let i = 0; i < amount; i++) {
            if (!descending) i = (amount - i);
            const message = historyMessages[i];

            if (message) idsToDelete.push(message.id);
        }

        if (idsToDelete.length == 0) return;

        const client = this.client;
        const request = await this.requester.request(`https://beta.character.ai/chat/history/msgs/delete/`, {
            headers: client.getHeaders(),
            method: 'POST',
            body: Parser.stringify({
                "history_id": this.externalId,
                "ids_to_delete": idsToDelete,
                "regenerating": false
            })
        })
        let passing = false;

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request);

            if (response.status === 'OK') passing = true;
        }

        if (!passing) throw Error('Failed to bulk delete messages.');
    }

    async saveAndStartNewChat() {
        if (!this.client.isAuthenticated()) throw Error('You must be authenticated to do this.');

        const client = this.client;
        const request = await this.requester.request(`https://beta.character.ai/chat/history/create/`, {
            headers: client.getHeaders(),
            method: 'POST',
            body: Parser.stringify({
                "character_external_id": this.characterId
            })
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            this.externalId = response.external_id;
            return response;
        } else throw Error('Failed saving & creating new chat.')
    }
}

module.exports = Chat
