const util = require('util');

class OutgoingMessage {
    constructor(chat, options) {
        function getValueOrDefault(value, fallback) {
            if (typeof(options) == 'string') return fallback;
            else return options[value] || fallback
        }

        const payload = {
            history_external_id: chat.externalId,
            character_external_id: chat.characterId,
            text: getValueOrDefault("text", options),
            tgt: chat.aiId,
            ranking_method: getValueOrDefault("ranking_method", 'random'),
            faux_chat: getValueOrDefault("faux_chat", false),
            staging: getValueOrDefault("staging", false),
            model_server_address: getValueOrDefault("model_server_address", null),
            override_prefix: getValueOrDefault("override_prefix", null),
            override_rank: getValueOrDefault("override_rank", null),
            rank_candidates: getValueOrDefault("rank_candidates", null),
            filter_candidates: getValueOrDefault("filter_candidates", null),
            prefix_limit: getValueOrDefault("prefix_limit", null),
            prefix_token_limit: getValueOrDefault("prefix_token_limit", null),
            livetune_coeff: getValueOrDefault("livetune_coeff", null),
            parent_msg_id: getValueOrDefault("parent_msg_id", null),
            stream_params: getValueOrDefault("stream_params", null),
            enable_tti: getValueOrDefault("initial_timeout", true),
            initial_timeout: getValueOrDefault("initial_timeout", null),
            insert_beginning: getValueOrDefault("insert_beginning", null),
            translate_candidates: getValueOrDefault("translate_candidates", null),
            stream_every_n_steps: getValueOrDefault("stream_every_n_steps", 16),
            chunks_to_pad: getValueOrDefault("chunks_to_pad", 8),
            is_proactive: getValueOrDefault("is_proactive", true),
        }

        this.payload = payload;
        return this.payload;
    }
}

class Message {
    constructor(chat, options) {
        this.chat = chat;
        this.rawOptions = options;

        this.id = options.id
        this.text = options.text
        this.src = options.src
        this.tgt = options.tgt
        this.isAlternative = options.is_alternative
        this.imageRelativePath = options.image_rel_path
        this.imagePromptText = options.image_prompt_text
        this.deleted = null
        this.srcName = options.src__name
        this.srcInternalId = options.src__user__username
        this.srcIsHuman = options.src__is_human
        this.srcCharacterAvatarFileName = options.src__character__avatar_file_name
        this.srcCharacterDict = options.src_char
        this.responsibleUserName = options.responsible_user__username
    }

    async getPreviousMessage() {
        const chat = this.chat;

        const history = await chat.fetchHistory()
        const historyMessages = history.messages;

        let message = null;

        try {
            message = historyMessages[historyMessages.length - 2];
        } catch (error) {}

        return message;
    }

    async delete(deletePreviousToo = false) {
        if (typeof(deletePreviousToo) != 'boolean') throw Error('Invalid arguments');
        if (this.deleted) throw Error('Message is already deleted');

        const chat = this.chat;

        try {
            const messagesToDelete = [];
            messagesToDelete.push(this.id);

            if (deletePreviousToo) {
                const previousMessage = await this.getPreviousMessage();
                if (previousMessage != null && previousMessage.id != null && previousMessage.deleted != true)
                    messagesToDelete.push(previousMessage.id);
            }

            await chat.deleteMessages(messagesToDelete);
            this.deleted = true;
        } catch (error) {throw Error("Failed to delete message." + error);}
    }

    // getters
    getAvatarLink() {
        return `https://characterai.io/i/80/static/avatars/uploaded/${this.srcCharacterAvatarFileName}`;
    }

    returnMessage() {
        return this.text;
    }
}

class Reply {
    constructor(chat, options) {
        this.chat = chat;

        if (options.force_login == true) throw Error('Too many messages! (this might be because you use a guest account)');
        if (options.abort == true) throw Error('Could not get a reply because it was aborted. This might be because the output was filtered (NSFW).')

        const replyOptions = options.replies[0]; // todo fix if aborted
        this.text = replyOptions.text
        this.id = replyOptions.id

        const srcCharacterDict = options.src_char;
        this.srcCharacterName = srcCharacterDict.participant.name
        this.srcAvatarFileName = srcCharacterDict.avatar_file_name

        this.isFinalChunk = options.is_final_chunk
        this.lastUserMessageId = options.last_user_msg_id
    }

    async getMessage() {
        return await this.chat.getMessageById(this.id);
    }

    [util.inspect.custom](depth, opts) {
        return this.text;
    }
}

class MessageHistory {
    constructor(chat, messages, hasMore, nextPage) {
        this.chat = chat;
        this.messages = messages;
        this.hasMore = hasMore;
        this.nextPage = nextPage;
    }
}

module.exports = { OutgoingMessage, Reply, Message, MessageHistory }