/**
 * Created by PyCharm.
 * User: tigra
 * Date: 5/3/12
 * Time: 12:39 AM
 * To change this template use File | Settings | File Templates.
 */

define(['AJAX/Requests','Managers/Redirect'],function(Requests,RedirectManager){
    var RemoteModal={
        changeHref:function(href){
            var param = "method=modal";
            if (href.charAt(href.length - 1) === '?') //Very unlikely
                return href + param;
            else if (href.indexOf('?') > 0)
                return href + '&' + param;
            else
                return href + '?' + param;
        },
        recursiveModal:function(target,data){
            var successFunc=function(data){
                Requests.checkResponse(data,function(){
                        RemoteModal.recursiveModal(target,data);
                });
            };

            if(data.status==5 && (data.in_modal || data.remember_modal)){
                var href;
                if(data.remember_modal){
                    var go_to=$(target).data('modal-url');
                    RedirectManager.addOverride('modal',function(location){
                        $.getJSON(go_to,successFunc);
                        $(target).on('hidden',function(){
                            RedirectManager.redirect(location);
                        });
                        return false;
                    });
                }

                href=RemoteModal.changeHref(data.redirect_to);

                $(target).data('modal-url',href);

                //meanwhile redirect_on_close exists only in response_redirect, so this location for this check is OK
                if(typeof data.redirect_on_close != 'undefined'){
                    $(target).on('hidden',function(){
                        RedirectManager.redirect(data.redirect_on_close);
                    });
                }

                $.getJSON(href,successFunc);
            }else{
                $(target).html(data.data);
            }

            $(target).find('.modal-body a:not(.action,.popup_window,.direct_link)').addClass("modal_remote");

            $(target).find('a.action').click(function(){
                var originalHref=$(this).data('href') || $(this).attr('href');
                $('#csrf_embed_form').attr('action',RemoteModal.changeHref(originalHref)).ajaxSubmit({
                    success:successFunc,
                    dataType:'json'
                });
                return false;
            });



            $(target).find('form').ajaxForm({
                success:successFunc,
                dataType:'json'
            }).find('input').keyup(function(e,t){
                        if(e.keyCode==13){
                            $(this).parents('form:eq(0)').submit();
                        }
                    });
        },
        init:function(){
            $('body').on('click',"a.popup_window",function(){
                $(this).attr('target',"_blank");
            });

            $('body').on('click',"a.modal_remote",RemoteModal.initOnClick);
            //$('a.modal_remote').attr('data-target','#vdsModal').attr('data-toggle','modal');
        },
        initOnClick:function (e) {
          //$(this).attr('data-target','#vdsModal').attr('data-toggle','modal');
          $(this).attr('data-target','#vdsModal');
          var link=$(this);

          var lv_target = $(this).attr('data-target');

          var originalHref=$(this).data('href') || $(this).attr('href');
          var lv_url = RemoteModal.changeHref(originalHref);
          $(lv_target).data('modal-url',lv_url);
          $.getJSON(lv_url,function(data){
              Requests.checkResponse(data,function(){
                  if(link.data('callback')){
                      link.data('callback')(); //if has callback -> time to call
                  }
                  RemoteModal.recursiveModal(lv_target,data);
              });
          });
            if($(this).parents('.modal-body').length){
                //should return false when inside body to prevent default modal window behaviour
                return false
            }
            return false;
        }
    };
    return RemoteModal;
});