var express = require('express');
var router=express.Router();

router.get('/',function(req,res,next){
    if(req.session.uuid==null){
        res.render('home', {status: false});
    }else{ 
        res.redirect('/student')
    }
});

module.exports = router;