var theme_path = 'ace/theme/';
var lang_path = 'ace/mode/';

function get_editor(jqobj){
    /* Find the editor related to a combobox (jqobj) */
    return jqobj.closest('.ace-editor-frame-options').parent().parent().find('.ace-editor-frame').first();
}

$( document ).ready(function(){
    /*Reset all <select> on page loading (some browser may cache this so we want to be sure it's the correct value)*/
    $('.select-ace-style select').each(function(){
        $(this).val($(this).find('option[selected]').val());
    });

    /* Init Ace editor(s) */
    $('.ace-editor-frame').each(function(index){
        var jqeditor = $(this);
        var editor = ace.edit(jqeditor.get(0));
        editor.renderer.setScrollMargin(10, 10);
        editor.setTheme(theme_path.concat(jqeditor.data('theme')));
        editor.getSession().setMode(lang_path.concat(jqeditor.data('lang')));
        jqeditor.get(0).style.fontSize = jqeditor.data('fontsize');
        editor.getSession().setTabSize(parseInt(jqeditor.data('tabsize')));
        editor.setReadOnly(jqeditor.data('ro') === 'yes');
        editor.getSession().setUseSoftTabs(jqeditor.data('softtabs') === 'yes');
        editor.setShowInvisibles(jqeditor.data('invisibles') === 'yes');
        editor.setHighlightActiveLine(jqeditor.data('highlight') === 'yes');
        editor.setShowPrintMargin(jqeditor.data('printmargin') === 'yes');
        jqeditor.closest('form').on('submit', function(){
            var code = editor.getValue();
            jqeditor.next('.hidden-code-value').val(code);
        });
    });
    /* Toggle configuration visibility */
    $('.ace-options-link').each(function(index){
        var clink = $(this);
        clink.on('click', function(){
            clink.toggleClass('ace-bottom-arrow');
            clink.toggleClass('ace-up-arrow');
            clink.closest('div').find('.ace-editor-frame-options').toggle(380);
        });
    });
    /* Change Lang */
    $('.ace-editor-lang-selector').each(function(index){
        $(this).on('change', function(){
            var new_lang = $(this).find('option:selected').first().val();
            var jqeditor = get_editor($(this));
            var editor = ace.edit(jqeditor.get(0));
            editor.getSession().setMode(lang_path.concat(new_lang));
        });
    });
    /* Change Theme */
    $('.ace-editor-theme-selector').each(function(index){
        $(this).on('change', function(){
            var new_theme = $(this).find('option:selected').first().val();
            var jqeditor = get_editor($(this));
            var editor = ace.edit(jqeditor.get(0));
            editor.setTheme(theme_path.concat(new_theme));
        });
    });
    /* Change Font Size */
    $('.ace-editor-fontsize-selector').each(function(index){
        $(this).on('change', function(){
            var new_fontsize = $(this).find('option:selected').first().val();
            var jqeditor = get_editor($(this));
            jqeditor.get(0).style.fontSize = new_fontsize;
        });
    });
});
