/* Javascript for VideoIframeXBlock. */
function VideoIframeXBlock(runtime, element, data) {

    wrapper_width = $('.video_wrapper', element).width();
    $('.video_wrapper', element).height(wrapper_width*0.6);

    video_download_link = data['video_download_link'];
    captions_download_link = data['captions_download_link'];
    display_name = data['display_name']
    iframe_link = data['iframe_link']
    description = data['description']
    display_studio_instructions = data['display_studio_instructions']

    if(video_download_link){
        $('.downloads_wrapper', element).css('display', 'flex');
        $('.video_download_wrapper', element).show();
        $('#video_download_link', element).attr('href', video_download_link);
    }

    if(captions_download_link){
        $('.downloads_wrapper', element).css('display', 'flex');
        $('.captions_download_wrapper', element).show();
        $('#captions_download_link', element).attr('href', captions_download_link);
    }

    if(description){
        $('.description_wrapper', element).show();
        $('#description', element).text(description);
    }

    if(display_studio_instructions){
        $('#video_iframe', element).hide();
        $('.author_instruction_wrapper', element).css('display', 'flex');
    }
    $('#video_iframe', element).attr('src', iframe_link);
    $('#display_name', element).text(display_name);

    $(function ($) {
        /*
        Use `gettext` provided by django-statici18n for static translations

        var gettext = VideoIframeXBlocki18n.gettext;
        */

        /* Here's where you'd do things on page load. */

        // dummy_text is to have at least one string to translate in JS files. If you remove this line,
        // and you don't have any other string to translate in JS files; then you must remove the (--merge-po-files)
        // option from the "extract_translations" command in the Makefile
        const dummy_text = gettext("Hello World");
    });
}
