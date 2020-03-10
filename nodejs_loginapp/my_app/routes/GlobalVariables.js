/**
 * Created by aditya.
 */
var datetime = require('node-datetime');
var GlobalVariables = {
    sessionType : ['student'],

    now: function(){
        var unixtimestamp = datetime.create();
        return unixtimestamp.format('d/m/Y I:M:S p')
    },

    DB_URL : "mongodb://mongo:27017/portal",
};
module.exports = GlobalVariables;
