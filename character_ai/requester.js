const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth')

class Requester {
    browser = undefined;
    page = undefined;

    #initialized = false;
    #hasDisplayed = false;
    #headless = true; // BERWARE: HEADLESS IS SLOW!

    constructor() {
        
    }
    isInitialized() {
        return this.#initialized;
    }

    async initialize() {
        if (!this.isInitialized());

        console.log("[node_characterai] Puppeteer - This is an experimental feature. Please report any issues on github.");

        puppeteer.use(StealthPlugin())
        const browser = await puppeteer.launch({
            headless: this.#headless,
            args: [
                '--fast-start',
                '--disable-extensions',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--no-gpu',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--override-plugin-power-saver-for-testing=never',
                '--disable-extensions-http-throttling',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3'
            ]
        });
        this.browser = browser;

        let page = await browser.pages();
        page = page[0];
        this.page = page;
        await page.setRequestInterception(false);

        page.setViewport({
            width: 1920 + Math.floor(Math.random() * 100),
            height: 3000 + Math.floor(Math.random() * 100),
            deviceScaleFactor: 1,
            hasTouch: false,
            isLandscape: false,
            isMobile: false,
        });
        await page.setJavaScriptEnabled(true);
        await page.setDefaultNavigationTimeout(0);
    
        const userAgent = 'CharacterAI/1.0.0 (iPhone; iOS 14.4.2; Scale/3.00)';
        await page.setUserAgent(userAgent);

        console.log("[node_characterai] Puppeteer - Done with setup");

    }

    async request(url, options) {
        const page = this.page;

        const method = options.method;
        /*(options.method == 'POST' || options.method == undefined || options.method == null
         ? 'POST' : 'GET');*/

        const body = (method == 'GET' ? {} : options.body);
        const headers = options.headers;
        
        let response

        try {
            const payload = {
                method: method,
                headers: headers,
                body: body
            }
            
            if (url.endsWith("/streaming/")) {
                await page.setRequestInterception(false);
                if (!this.#hasDisplayed) {
                    console.log("[node_characterai] Puppeteer - Eval-fetching is an experimental feature and may be slower. Please report any issues on github")
                    this.#hasDisplayed = true;
                }

                // Bless @roogue & @drizzle-mizzle for the code here!
                response = await page.evaluate(
                    async (payload, url) => {
                        const response = await fetch(url, payload);

                        const data = await response.text();
                        const matches = data.match(/\{.*\}/g);

                        const responseText = matches[matches.length - 1];

                        let result = {
                            code : 500,
                        }

                        if (!matches) result = null;
                        else {
                            result.code = 200;
                            result.response = responseText;
                        }

                        return result;
                    },
                    payload,
                    url
                );
                
                response.status = () => response.code // compatibilty reasons
                response.text = () => response.response // compatibilty reasons
            } else {
                await page.setRequestInterception(true);
                let initialRequest = true;
                
                page.once('request', request => {
                    var data = {
                        'method': method,
                        'postData': body,
                        'headers': headers
                    };
                    
                    if (request.isNavigationRequest() && !initialRequest) {
                        return request.abort();
                    }
                    
                    try {
                        initialRequest = false;
                        request.continue(data);
                    } catch (error) {
                        console.log("[node_characterai] Puppeteer - Non fatal error: " + error);
                    }
                });

                response = await page.goto(url, { waitUntil: 'networkidle2' });
                
            }
        } catch (error) {
            console.log("[node_characterai] Puppeteer - " + error)
        }
        
        return response;
    }
}

module.exports = Requester;