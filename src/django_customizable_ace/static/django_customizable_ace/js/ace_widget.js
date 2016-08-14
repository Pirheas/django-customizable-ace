var theme_path = 'ace/theme/';
var lang_path = 'ace/mode/';

$( document ).ready(function(){
    $('.ace-editor-frame').each(function(index){
        var theme = $(this).data('theme');
        var lang = $(this).data('lang');
        var editor = ace.edit($(this).get(0));
        editor.setTheme(theme_path.concat(theme));
        editor.getSession().setMode(lang_path.concat(lang));
        editor.renderer.setScrollMargin(10, 10);
        console.log($(this).data('ro') === 'yes');
        if ($(this).data('ro') === 'yes'){
            console.log('Coucou');
            editor.setReadOnly(true);
        }
    });
});
