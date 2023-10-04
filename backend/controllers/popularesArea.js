const {exec}  = require('child_process');

function popularesArea(req, res) {
    const userId = req.params.userId;
    const command = `python3 ./backend/model/relevanteArea.py ${userId}`;

    exec(command, (err, stdout, stderr) => {
        if (err) {
            console.log(err);
            return res.status(500).json({message: 'Internal server error'});
        }
        console.log(stdout);
        console.log(stderr);
        return res.status(200).send(stdout);
    })
}

module.exports = popularesArea;
