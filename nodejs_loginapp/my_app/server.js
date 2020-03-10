var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var fs = require('fs');
var sessions = require('express-session');
var compression = require('compression');
var cookieParser = require('cookie-parser');
var fileType = require('file-type');
var helmet = require('helmet');

var home = require('./routes/home');
var register = require('./routes/register')
var api = require('./routes/api');

var port = 3000;
var app = express();	//initialize app

//view engine
app.set('views',path.join(__dirname,'views'));
app.set('view engine','ejs');
app.engine('html',require('ejs').renderFile);

//set Static folder
app.use(express.static(path.join(__dirname,'client'))); //for angular 2 related stuff

//body parser
//body parser
app.use(bodyParser.json({limit:'50mb'}));
app.use(bodyParser.urlencoded({extended:true, limit:'50mb'}));
app.use(cookieParser());
app.use(compression());
app.use(helmet());
app.use(sessions({
    cookieName : 'login_cookie',
    secret : 'portal_login-dev01-auth',
    resave: false,
    saveUninitialized: true,
    cookie: {
        maxAge : 30*60*1000,        // 1/2 hour
        ephemeral: true, // when true, cookie expires when the browser closes
        httpOnly: false, // when true, cookie is not accessible from javascript
        secure: false // when true, cookie will only be sent over SSL. use key 'secureProxy' instead if you handle SSL not in your node process
    }
}));

app.use('/',home);
app.use('/home',home)
app.use('/register',register)
app.use('/api',api)

app.listen(port,function(){
	console.log("Server Started on port "+port);
});
