
odoo.define('helpdesk_portal_richtext.helpdesk_portal_richtext', function(require) {
    'use strict';

    $(function(){
        $('.btn-primary').click(function () {
            var description_content = $('#editor-container').children().html();
            $('#hiddeninput').val(description_content);
        });
    });

});
