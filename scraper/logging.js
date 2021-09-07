const axios = require('axios');

async function log(text, source='scraper') {
    await axios.post(`http://localhost:3000/log`, { source, text });
}

module.exports = {
    log
}
