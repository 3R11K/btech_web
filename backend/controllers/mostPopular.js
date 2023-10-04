const fs = require('fs');

function mostPopular(req, res) {
    fs.readFile('./backend/model/most_popular.json', 'utf8', (err, data) => {
        if (err) {
          console.error(err);
          res.status(500).send('Internal server error');
        }
        const jsonObject = JSON.parse(data);
        res.status(200).send(jsonObject);
      });
}

module.exports = mostPopular;