const axios = require('axios');

const url = 'http://127.0.0.1:5000/nerText';

async function containsName(checkFor, text) {
    const response = await axios.post(url, {
        checkFor,
        text
    });
    return response.data;
}

module.exports = {
    containsName
}
