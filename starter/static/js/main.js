require([],function(){
    //extending jquery
        $.fn.extend({
            clickToPost:function(callback){
                return this.each(function(){
                    var obj=$(this);
                    require(['AJAX/Requests'],function(Requests){
                        obj.click(function(){
                            var url=obj.attr('href');
                            Requests.postJSON(url,callback);
                            return false;
                        })
                    });
                });
            }
        });

        //scrollto implementation
        $.scrollTo=function(element,duration,options){
            var defaults={
                offset:{
                    top:-50
                },
                duration:300
            }

            if(typeof duration!='undefined'){
                options.duration=duration
            }

            var options= $.extend(defaults,options)

                $('body').animate({scrollTop:$(element).position().top+options.offset.top},options.duration)
        };

        //make ajax post works crossbrowser
        $.ajaxSetup({
            type: "POST",
            xhrFields: {
               withCredentials: true
            },
            crossDomain: true
        });
        jQuery.support.cors = true;

});

require(['ll','UI/SubmitButtons','AJAX/RemoteModal','AJAX/Requests','jqlibs/form'], function(ll,SubmitButtons,RemoteModal,Requests) {
    //common startup
    ll.debug=global_debug; //defined in main template
    $(function(){
        SubmitButtons();
    });
    RemoteModal.init();

    var makeAction=function(link){
        var form=$('#csrf_embed_form')
        if($(link).data('href')){
            form.attr('action',$(link).data('href'));
        }else{
            form.attr('action',$(link).attr('href'));
        }

        if($(link).hasClass('action-remote')){
            form.attr('action',RemoteModal.changeHref(form.attr('action')));
            form.ajaxSubmit({
                success:function(response){
                                if($(link).data('callback')){
                                    Requests.checkResponse(response,
                                            function(){
                                                $(link).data('callback')(response.data)
                                            }
                                    );
                                }else{
                                    Requests.checkResponse(response);
                                }
                            },
                dataType:'json'
            });
        }else{
            form.submit();
        }
        return false;
    }

    $('body').on('click','.action',function(){
        return makeAction(this);
    });

    $('a[rel="tooltip"]').tooltip();

    $('body').on('click','.btn.disabled',function(){
        return false;
    });

});