/**
 * Created by PyCharm.
 * User: tigra
 * Date: 5/3/12
 * Time: 12:55 AM
 * To change this template use File | Settings | File Templates.
 */

define([],function(){
    var RedirectManager={
        overrides:{},
        addOverride:function(name,func){
            RedirectManager.overrides[name]=func;
        },
        removeOverride:function(name){
            delete RedirectManager.overrides[name];
        },
        redirect:function(location){
            var act=true;
            $.each(this.overrides,function(name,override){
                act=override(location);
                RedirectManager.removeOverride(name);
                return act;
            });
            if(act){
                document.location.href=location;
            }
        }
    };
    return RedirectManager;
});