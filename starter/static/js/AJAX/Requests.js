/**
 * Created by PyCharm.
 * User: tigra
 * Date: 11/30/11
 * Time: 7:32 PM
 * To change this template use File | Settings | File Templates.
 */

define(['UI/Message','ll','Managers/Redirect'],function(Message,ll,RM){
    var Requests={
        returnOrServercall:function(response,callback,callback_servercall){
            if(callback && typeof callback=='function') {
                return callback();
            }

            if(callback_servercall && typeof callback_servercall=='function'){
                if(response.call)
                    return callback_servercall();
            }

            return true;
        },
        checkResponse:function(response,callback,callback_servercall){
            //1==ok
            //0==error
            //2==good message
            //3==good message, but still stop
            //4==Request confirmation, message=confirmation request
            //5==redirect
            if(typeof callback_servercall=='undefined'){
                callback_servercall=null;
            }

            if(typeof callback=='undefined'){
                callback=null;
            }


            if(response.status==1){
                if(!$('#vdsModal').hasClass('in')){
                    require(['AJAX/RemoteModal'],function(RemoteModal){
                        $('#vdsModal').modal();
                        RemoteModal.recursiveModal('#vdsModal',response);
                    });
                    //return Requests.returnOrServercall(response,callback,callback_servercall);
                }
                return Requests.returnOrServercall(response,callback,callback_servercall);

            }
            else if(response.status==2){
                Message.good(response.message);
                return Requests.returnOrServercall(response,callback,callback_servercall);
            }else if(response.status==3){
                Message.good(response.message);
                return false;
            }
            else if(response.status==4){
                confirmed=confirm(response.message);
                if(confirmed){
                    $.post(response.confirmation_url,
                        {csrf:$('#csrf_embed').val()},
                        function(r){
                            Requests.checkResponse(r,callback,callback_servercall);
                        },
                        'json'
                    );
                }
                return confirmed;
            }
            else if(response.status==5){
                if(!response.in_modal){ //caught by RemoteModal
                    RM.redirect(response.redirect_to);
                }else{
                        if(!$('#vdsModal').hasClass('in')){
                        require(['AJAX/RemoteModal'],function(RemoteModal){
                            $('#vdsModal').modal();
                            RemoteModal.recursiveModal('#vdsModal',response);
                        });
                            return false;
                        }
                }
                return Requests.returnOrServercall(response,callback,callback_servercall);
            }
            else{
                Message.bad(response.message);
                return false;
            }
        },
        postJSON:function(url,callback){
            $.ajax({
                url:url,
                success:callback,
                type:'post',
                dataType:'json'
            });
        }

    };
    return Requests;
});