(function($){
    $(function(){
        $('.button-collapse').sideNav();
        $('.parallax').parallax();
        $('.tooltipped').tooltip({delay: 50});

        $('.modal-trigger').leanModal();
        }).hover( function() {
            $(this).toggleClass('hover');
        });
    });
})(jQuery); // end of jQuery name space