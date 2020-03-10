/**
 * Created by aditya on 8/8/18.
 */
var express = require('express');
var router=express.Router();
var globals = require('./GlobalVariables');
var mongojs = require('mongojs');
var fileUpload = require('express-fileupload');
var path = require('path');
var db=mongojs(globals.DB_URL,['student','teacher']);
var StudentRegistrationModel = require('./StudentRegModel');
router.use(fileUpload());

router.post('/',function(req,res,next){
    StudentRegistrationModel.findOne({email:req.body.email},function (err,foundData) {
        if(err){
            res.render('home',{status:true, error:"Email not registered yet!",prev:{}})
        }
        else{
            console.log(req.body.email,'found')
            if(foundData) {
                bcrypt.compare(req.body.passwd, foundData.password, function (err, result) {
                    if (!result) {
                        res.render('home',{status:true,error:"Password is not correct.",prev:req.body})
                    }
                    else {
                        req.session.uuid = foundData.uuid;
                        req.session.type = globals.sessionType[0];
                        res.render('studentportal',{status: true, type: 1, data: foundData } );
                    }
                });
            }
            else{
                res.render("home",{status:true,error:"Email or Password is not correct.",prev:req.body})
            }
        }
    });
});
module.exports = router;
