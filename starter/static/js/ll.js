/**
 * Created by PyCharm.
 * User: tigra
 * Date: 11/27/11
 * Time: 11:13 AM
 * To change this template use File | Settings | File Templates.
 */

define({
    debug:false,
    log:function(message){
        if(this.debug){
            if(typeof console!='undefined')
                console.log(message);
            else
                alert(message);
        }
    }
});

