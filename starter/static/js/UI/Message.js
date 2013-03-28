/**
 * Created by PyCharm.
 * User: tigra
 * Date: 11/30/11
 * Time: 7:33 PM
 * To change this template use File | Settings | File Templates.
 */

define([],function(){
    var Message={
        saved:function(){
            Message.good("Saved");
        },
        done:function(){
            Message.good("Done");
        },
        good:function(message){
            $('#message_bar .good').text(message).slideDown();
            setTimeout(function(){
                $('#message_bar .good').slideUp();
            },2500);
        },
        bad:function(message){
            $('#message_bar .bad').text(message).slideDown();
            setTimeout(function(){
                $('#message_bar .bad').slideUp();
            },2500);
        }
    };
    return Message;
});