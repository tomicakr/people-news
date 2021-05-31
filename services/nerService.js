const axios = require('axios');

const url = 'http://127.0.0.1:5000/nerText';

async function containsName(checkFor, text, link) {
    const res = {
        paragraphResults: [],
        allNamedEntities: new Set(),
        containsCheckedSet: false
    };
    for (let i = 0; i < text.length; i++) {
        const paragraph = text[i];
        const response = await axios.post(url, {
            checkFor,
            text: paragraph,
            link
        });

        if (response.data.anyNameInside) {
            res.containsCheckedSet = true;
        }

        res.paragraphResults.push(response.data);
        response.data.foundNamedEntities.forEach(ne => {
            if (ne.trim()) res.allNamedEntities.add(ne);
        });
    }
    
    return res;
}

module.exports = {
    containsName
}
