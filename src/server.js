const port = 3000
const path = require('path')
const express = require('express')
const app = express()
const bodyParser = require('body-parser')

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

// Rotas backend e frontend
app.use('/api', require(path.join(__dirname, "..", 'backend', "controllers", "api"))); // Uso da API
app.use('/', require(path.join(__dirname, "..", "backend","routes", "pages"))); // Páginas

// Arquivos estáticos
app.use(express.static(path.join(__dirname,"..",'frontend')));

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`)
})
