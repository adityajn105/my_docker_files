var express = require('express');
var bcrypt=  require('bcryptjs');
var fileUpload = require('express-fileupload');
var path = require('path');
var globals = require('./GlobalVariables');
var StudentRegistrationModel = require('./StudentRegModel');
var router=express.Router();
router.use(fileUpload());

router.get('/',function(req,res,next){
    res.render('register', {status: false, type:1, msg:''});
});

router.post('/student',function(req,res,next){
    var student = new StudentRegistrationModel();
    student.firstname = req.body.firstname;
    student.lastname = req.body.lastname;
    student.email = req.body.email;
    student.aadhaar = req.body.aadhaar;
    student.dob = req.body.dob;
    student.address = req.body.address

    if((req.body.passwd != req.body.passwd2) || req.body.passwd.length < 5 ){
        res.render('register', {status: true, type:1, error: ["Passwords too small or do not match."], prev:req.body});
        return;
    }

    //get profile photo object
    var profilephoto = req.files.profile;

    //generate hash from password
    bcrypt.genSalt(10, function (err, salt) {
        bcrypt.hash(req.body.passwd, salt, function (err, hash) {
            student.password = hash;
            student.profile = "profilephotos/"+req.body.aadhaar;
            student.save(function (err, savedObject) {
                if (err) {
                    res.render('register', {status: true, type: 1, error: err.message.split(','), prev:req.body});
                }
                else {
                    if(profilephoto){
                      profilephoto.mv(__dirname +"/../profilephotos/"+req.body.aadhaar, function(err) {
                          if (err) console.log("Upload failed : "+err);
                      });
                    }
                    req.session.uuid = savedObject.uuid;
                    req.session.type = globals.sessionType[0];
                    res.render('register', {status: false, type: 1, msg: "You have Been Registered"});
                }
            });
        });
    });
});

router.post('/supplier',function(req,res,next){

});

module.exports = router;
