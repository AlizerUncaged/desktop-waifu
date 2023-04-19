const Chat = require('./chat')
const { v4: uuidv4 } = require('uuid');
const Parser = require('./parser')
const Requester = require('./requester')

class Client {
    #token = undefined;
    #isGuest = false;
    #authenticated = false;
    #guestHeaders = {
        "content-type": "application/json",
        "user-agent": 'CharacterAI/1.0.0 (iPhone; iOS 14.4.2; Scale/3.00)'
    }
    requester = new Requester();

    constructor() {
        this.#token = undefined;
    }

    // api fetching
    async fetchCategories() {
        const request = await this.requester.request('https://beta.character.ai/chat/character/categories/')

        if (request.status() === 200) return await Parser.parseJSON(request);
        else throw Error('Failed to fetch categories');
    }
    async fetchUserConfig() {
        const request = await this.requester.request('https://beta.character.ai/chat/config/', {
            headers:this.#guestHeaders
        })
        
        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response;
        } else Error('Failed fetching user configuration.')
    }
    async fetchUser() {
        if (!this.isAuthenticated()) throw Error('You must be authenticated to do this.');
        
        const request = await this.requester.request('https://beta.character.ai/chat/user/', {
            headers:this.getHeaders()
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response;
        } else Error('Failed fetching user.')
    }
    async fetchFeaturedCharacters() {
        if (!this.isAuthenticated()) throw Error('You must be authenticated to do this.');
        
        const request = await this.requester.request('https://beta.character.ai/chat/characters/featured_v2/', {
            headers:this.getHeaders()
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response;
        } else Error('Failed fetching featured characters.')
    }
    async fetchCharactersByCategory(curated = false) {
        if (curated == undefined || typeof(curated) != 'boolean') throw Error('Invalid arguments.')

        const url = `https://beta.character.ai/chat/${
            curated ? 'curated_categories' : 'categories'
        }/characters/`;

        const request = await this.requester.request(url, {
            headers:this.#guestHeaders
        })

        const property = curated
        ? 'characters_by_curated_category'
        : 'characters_by_category';
      
        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response[property]
        } else Error('Failed fetching characters by category.')
    }
    async fetchCharacterInfo(characterId) {
        if (!this.isAuthenticated()) throw Error('You must be authenticated to do this.');
        if (characterId == undefined || typeof(characterId) != 'string') throw Error('Invalid arguments.')

        const request = await this.requester.request(`https://beta.character.ai/chat/character/info-cached/${characterId}/`, {
            headers:this.getHeaders(),
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response.character;
        } else Error('Could not fetch character information.')
    }
    async searchCharacters(characterName) {
        if (!this.isAuthenticated()) throw Error('You must be authenticated to do this.');
        if (this.#isGuest) throw Error('Guest accounts cannot use the search feature.');
        if (characterName == undefined || typeof(characterName) != 'string') throw Error('Invalid arguments.')

        const request = await this.requester.request(`https://beta.character.ai/chat/characters/search/?query=${characterName}`, {
            headers:this.getHeaders()
        })
        
        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response;
        } else Error('Could not search for characters.')
    }
    async getRecentConversations() {
        if (!this.isAuthenticated()) throw Error('You must be authenticated to do this.');
        const request = await this.requester.request(`https://beta.character.ai/chat/characters/recent/`, {
            headers:this.getHeaders()
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)

            return response;
        } else Error('Could not get recent conversations.')
    }

    // chat
    async createOrContinueChat(characterId, externalId = null) {
        if (!this.isAuthenticated()) throw Error('You must be authenticated to do this.');
        if (characterId == undefined || typeof(characterId) != 'string' || typeof(externalId != null ? externalId : '') != 'string') throw Error('Invalid arguments.')

        let request = await this.requester.request('https://beta.character.ai/chat/history/continue/',  {
            body:Parser.stringify({
                character_external_id: characterId,
                history_external_id: externalId,
            }),
            method:'POST',
            headers:this.getHeaders()
        })

        if (request.status() === 200 || request.status() === 404) {
            let response = await request.text()
            
            if (response === "No Such History" || response === "there is no history between user and character") { // Create a new chat
                request = await this.requester.request('https://beta.character.ai/chat/history/create/', {
                    body:Parser.stringify({
                        character_external_id: characterId,
                        history_external_id: null,
                    }),
                    method:'POST',
                    headers:this.getHeaders()
                })
                if (request.status() === 200) response = await Parser.parseJSON(request)
                else Error('Could not create a new chat.')
            } 

            // If a text gets returned, we try to parse it to JSON!
            try {
                response = JSON.parse(response);
            } catch (error) {}

            // Continue it 
            const continueBody = response;
            return new Chat(this, characterId, continueBody)
        } else Error('Could not create or resume a chat.')
    }

    // authentification
    async authenticateWithToken(token) {
        if (this.isAuthenticated()) throw Error('Already authenticated');
        if (!token || typeof(token) != 'string') throw Error('Specify a valid token');

        await this.requester.initialize();

        const request = await this.requester.request('https://beta.character.ai/dj-rest-auth/auth0/', {
            method:'POST',
            body:Parser.stringify({
                access_token: token
            }),
            headers:{
                'Content-Type': 'application/json',
            }
        })

        if (request.status() === 200 || request.status === 500) {
            const response = await Parser.parseJSON(request)

            this.#isGuest = false;
            this.#authenticated = true;
            this.#token = response.key;

            return response.token
        } else throw Error('Token is invalid')
    }
    async authenticateAsGuest() {
        if (this.isAuthenticated()) throw Error('Already authenticated');
        await this.requester.initialize();

        const uuid = uuidv4();
        
        const payload = JSON.stringify({
            lazy_uuid: uuid
        });

        let request = await this.requester.request('https://beta.character.ai/chat/auth/lazy/', {
            method:'POST',
            body:payload,
            headers: this.#guestHeaders
        })

        if (request.status() === 200) {
            const response = await Parser.parseJSON(request)
            
            if (response.success === true) {
                this.#isGuest = true;
                this.#authenticated = true;
                this.#token = response.token;
                this.uuid = uuid;

                return response.token;
            } else throw Error('Registering failed');
        } else throw Error('Failed to fetch a lazy token')
    }
    unauthenticate() {
        if (this.isAuthenticated()) {
            this.#authenticated = false;
            this.#isGuest = false;
            this.#token = undefined;
        }
    }

    // getters
    getToken() {
        return this.#token;
    }
    isGuest() {
        return this.#isGuest;
    }
    isAuthenticated() {
        return (this.#authenticated)
    }

    // headers
    getHeaders() {
        return {
            authorization: `Token ${this.#token}`,
            'Content-Type': 'application/json',
            //"user-agent": 'CharacterAI/1.0.0 (iPhone; iOS 14.4.2; Scale/3.00)'
            //'sec-ch-ua': `"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"`,
            //'sec-ch-ua-mobile': '?0'
            /*'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',*/
            //'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        };
    }
}

module.exports = Client