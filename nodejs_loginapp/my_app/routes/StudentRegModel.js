/**
  Created by aditya.
*/
var mongoose  = require('mongoose');
var autoIncrement = require('mongoose-auto-increment');
var globals = require('./GlobalVariables');
var mongooseValidationErrorTransform = require('mongoose-validation-error-transform');
var uniqueValidator = require('mongoose-unique-validator');

mongoose.plugin(mongooseValidationErrorTransform, {
    capitalize: true,
    humanize: true,
    transform: function(messages) {
        return messages.join(', ');
    }
});

mongoose.Promise = global.Promise;
var connection = mongoose.createConnection(globals.DB_URL,{ useNewUrlParser: true, poolSize: 4 });
autoIncrement.initialize(connection);
var studentSchema = mongoose.Schema({
    firstname:{
        type:String,
        required: [true, "Please enter your FirstName."]
    },
    lastname:{
        type:String,
        required: [true,"Please enter your LastName."]
    },
    email:{
        type:String,
        required:[true,"Please enter Email address."],
        unique: [true, "Email already in use."],
        match: [/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid Email Address.']
    },
    password:{
        type:String,
        required:[true,"Please enter password."]
    },
    address:{
        type:String,
        required: false
    },
    aadhaar:{
        type:String,
        required:[true,"Please enter aadhaar number."],
        maxlength:[12,"Invalid aadhaar number."],
        minlength:[12,"Invalid aadhaar number."],
        unique:[true,"Aadhaar number already in use."]
    },
    profile:{
        type:String,
        required:false
    },
    dob:{
        type:String,
        required:[true,"Birth-date is required for registration."]
    }
},{strict:true});
studentSchema.plugin(autoIncrement.plugin, {
    model: 'student',
    field: 'uuid',
    startAt: 8900122,
    incrementBy: 3
});
studentSchema.plugin(uniqueValidator, { message: '{PATH} already in use.' });
var studentRegModel = connection.model("student",studentSchema);
module.exports = studentRegModel;
