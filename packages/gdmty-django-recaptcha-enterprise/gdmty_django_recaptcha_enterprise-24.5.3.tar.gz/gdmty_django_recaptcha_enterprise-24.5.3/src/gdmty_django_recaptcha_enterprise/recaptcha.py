from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
from django.conf import settings
from secrets import compare_digest
from logging import getLogger

DEBUG = settings.DEBUG or False
RECAPTCHA_ENTERPRISE_BYPASS_TOKEN = settings.RECAPTCHA_ENTERPRISE_BYPASS_TOKEN or False

log = getLogger('gdmty_django_recaptcha_enterprise.recaptcha')


class RecaptchaEnterprise:
    def __init__(self, project_id: str = None, site_key: str = None, credentials: str = None):
        """Create an assessment to analyze the risk of a UI action.
        Args:
            project_id: GCloud Project ID
            site_key: Site key obtained by registering a domain/app to use recaptcha services.
            credentials: The token obtained from the client on passing the recaptchaSiteKey.
        """
        self.project_id = project_id
        self.site_key = site_key
        self.service_account_credentials = credentials
        self.client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient(credentials=credentials)

    def create_assessment(self, token: str, recaptcha_action: str = None) -> Assessment | None:
        """Create an assessment to analyze the risk of a UI action.
        Args:
            token: The token obtained from the client on passing the recaptchaSiteKey.
            recaptcha_action: Action name corresponding to the token.
        """

        # Set the properties of the event to be tracked.
        event = recaptchaenterprise_v1.Event()
        event.site_key = self.site_key
        event.token = token

        assessment = recaptchaenterprise_v1.Assessment()
        assessment.event = event

        project_name = f"projects/{self.project_id}"

        # Build the assessment request.
        request = recaptchaenterprise_v1.CreateAssessmentRequest()
        request.assessment = assessment
        request.parent = project_name
        response = self.client.create_assessment(request)

        # Check if the token is valid.
        if not response.token_properties.valid:
            log.info(f"The CreateAssessment call failed because the token was invalid for for the following reasons: {str(response.token_properties.invalid_reason)}")
            return

        # Check if the expected action was executed.
        if response.token_properties.action != recaptcha_action:
            log.info("The action attribute in your reCAPTCHA tag does not match the action you are expecting to score")
            return
        else:
            # Get the risk score and the reason(s)
            # For more information on interpreting the assessment,
            # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
            for reason in response.risk_analysis.reasons:
                log.info(f"response.risk_analysis.reasons: {reason}")
            log.info(f"The reCAPTCHA score for this token is: {str(response.risk_analysis.score)}")
            # Get the assessment name (id). Use this to annotate the assessment.
            assessment_name = self.client.parse_assessment_path(response.name).get("assessment")
            log.info(f"Assessment name: {assessment_name}")
        return response

    def assess_token(self, token: str, action: str = None) -> bool:
        """Create an assessment of a token for a given action.
        Args:
            :param token: The token obtained from the client on passing the recaptchaSiteKey.
            :param action: The action name used to assess the token.
        """

        if DEBUG:
            if RECAPTCHA_ENTERPRISE_BYPASS_TOKEN is not False:
                if compare_digest(token, RECAPTCHA_ENTERPRISE_BYPASS_TOKEN):
                    return True

        if not DEBUG and RECAPTCHA_ENTERPRISE_BYPASS_TOKEN is not False:
            return False

        if not action and not settings.RECAPTCHA_ENTERPRISE_DEFAULT_ACTION:
            action = "VERIFY"

        response = self.create_assessment(token, action)
        log.info(f"Assessment response: {response}")

        if response:
            return response.token_properties.valid
        return False
