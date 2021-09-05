const axios = require('axios');

async function log(text) {
    await axios.post('http://localhost:3000/log', { text });
}

module.exports = {
    log
}
