"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import translation
from django.utils.translation import gettext_noop as _
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String

try:
    from xblock.utils.studio_editable import StudioEditableXBlockMixin
except ModuleNotFoundError:  # For compatibility with Palm and earlier
    from xblockutils.studio_editable import StudioEditableXBlockMixin
try:
    from xblock.utils.resources import ResourceLoader
except ModuleNotFoundError:  # For compatibility with Palm and earlier
    from xblockutils.resources import ResourceLoader

from xblock.validation import Validation, ValidationMessage


class VideoIframeXBlock(StudioEditableXBlockMixin, XBlock):
    """
    This XBlock renders video in an iframe.

    Also renders a video download link and a captions download link.
    """

    icon_class = "video"
    has_author_view = True

    display_name = String(
        display_name=_("Video Title"),
        default="Video Iframe",
        scope=Scope.settings,
        help=_("This name appears at the top of the video.")
    )

    iframe_link = String(
        display_name=_("Video URL"),
        default="",
        scope=Scope.settings,
        help=_("Video link copied from Media Dashboard.")
    )

    description = String(
        display_name=_("Video Description"),
        default="",
        scope=Scope.settings,
        help=_("Optional description appears below the video.")
    )

    video_download_link = String(
        display_name=_("Video Download URL"),
        default="",
        scope=Scope.settings,
        help=_("Optional video download link copied from Media Dashboard.")
    )

    captions_download_link = String(
        display_name=_("Captions Download URL"),
        default="",
        scope=Scope.settings,
        help=_("Optional captions/transcript download link copied from Media Dashboard.")
    )

    editable_fields = ('display_name', 'iframe_link', 'description', 'video_download_link', 'captions_download_link')

    loader = ResourceLoader(__name__)

    def validate_field_data(self, validation, data):
        """
        Validate video link and video id.
        """
        validator = URLValidator(schemes=['https'])

        if not data.iframe_link:
            validation.add(ValidationMessage(ValidationMessage.ERROR, _("Video Link is mandatory")))
        else:
            try:
                validator(data.iframe_link)
            except ValidationError:
                validation.add(ValidationMessage(ValidationMessage.ERROR, _("Provided Video URL is invalid")))

        if data.video_download_link:
            try:
                validator(data.video_download_link)
            except ValidationError:
                validation.add(
                    ValidationMessage(ValidationMessage.ERROR, _("Provided Video Download URL is invalid"))
                )

        if data.captions_download_link:
            try:
                validator(data.captions_download_link)
            except ValidationError:
                validation.add(
                    ValidationMessage(ValidationMessage.ERROR, _("Provided Captions Download URL is invalid"))
                )

    def clean_studio_edits(self, data):
        """
        Strip all incoming URL strings.
        """
        for k in data:
            data[k] = data[k].strip()

    def validate(self):
        """
        Override validate method in StudioEditableXBlockMixin to prevent validation is Studio preview.
        """
        return Validation(self.scope_ids.usage_id)

    def student_view(self, context=None, display_studio_instructions=False):
        """
        Create primary view of the VideoIframeXBlock, shown to students when viewing courses.
        """
        frag = Fragment(self.loader.render_django_template("static/html/video_iframe.html", context=context))
        frag.add_css_url(self.runtime.local_resource_url(self, "public/css/video_iframe.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript_url(self.runtime.local_resource_url(self, "public/js/src/video_iframe.js"))
        frag.initialize_js(
            'VideoIframeXBlock', {
                'display_name': self.display_name,
                'description': self.description,
                'iframe_link': self.iframe_link,
                'video_download_link': self.video_download_link,
                'captions_download_link': self.captions_download_link,
                'display_studio_instructions': display_studio_instructions
            }
        )
        return frag

    def author_view(self, context=None):
        """
        Create preview to be show to course authors in Studio.
        """
        return self.student_view(context=context, display_studio_instructions=not self.iframe_link)

    @staticmethod
    def workbench_scenarios():
        """Create canned scenario for display in the workbench."""
        return [
            ("VideoIframeXBlock",
             """<video_iframe/>
             """),
            ("Multiple VideoIframeXBlock",
             """<vertical_demo>
                <video_iframe/>
                <video_iframe/>
                <video_iframe/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop('Dummy')
