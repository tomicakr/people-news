const axios = require('axios');

const url = 'http://127.0.0.1:5000/nerText';

async function containsName(checkFor, text) {
    const responses = [];
    for (let i = 0; i < text.length; i++) {
        const paragraph = text[i];
        const response = await axios.post(url, {
            checkFor,
            text: paragraph
        });

        responses.push(response.data);
    }
    
    return responses;
}

module.exports = {
    containsName
}
