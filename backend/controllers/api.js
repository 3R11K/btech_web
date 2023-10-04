//rotas api usando router
const express = require('express')
const router = express.Router()
const path = require('path')

const forYouCourses = require('./forYouCourses')
const mostPopular = require('./mostPopular')
const popularesArea = require('./popularesArea')

//perfil
const profile = require('./profile')

router.get("/profile/:userId", profile)

router.get('/forYouCourses/:userId', forYouCourses)

router.get('/populares', mostPopular)

router.get('/popularesArea/:userId', popularesArea)

module.exports = router