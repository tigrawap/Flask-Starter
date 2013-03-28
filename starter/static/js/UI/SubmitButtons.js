define([],function(){
                return function(){
                    $('.submit_button').each(function(i,elem){
                        var form=$(elem).parents('form:eq(0)');
                        $(elem).click(function(){
                            $(form[0]).submit();
                        });

                        /*
                        form.find('input').keypress(function (e) {
                            if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
                                form.submit();
                            }
                        });
                        */
                    });
                }
        });