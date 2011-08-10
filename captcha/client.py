import urllib2, urllib

API_SSL_SERVER="https://www.google.com/recaptcha/api"
API_SERVER="http://www.google.com/recaptcha/api"
VERIFY_SERVER="www.google.com"

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (public_key,
                 attrs,
                 use_ssl = False,
                 error = None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    options_js = ''
    if attrs:
        options_js = '<script type="text/javascript">var RecaptchaOptions = {\n'
        for k, v in attrs.get('options').items():
            options_js += "\t%s : '%s',\n" % (k, v)
        options_js += '};\n</script>'

    return """
    %(options_js)s
    <script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>

<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>
""" % {
        'ApiServer' : server,
        'PublicKey' : public_key,
        'ErrorParam' : error_param,
        'options_js' : options_js
        }


def submit (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip,
            use_ssl=False):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len (recaptcha_response_field) and len (recaptcha_challenge_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')


    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode ({
            'privatekey': encode_if_necessary(private_key),
            'remoteip' :  encode_if_necessary(remoteip),
            'challenge':  encode_if_necessary(recaptcha_challenge_field),
            'response' :  encode_if_necessary(recaptcha_response_field),
            })

    if use_ssl:
        verify_url = 'https://%s/recaptcha/api/verify' % VERIFY_SERVER
    else:
        verify_url = 'http://%s/recaptcha/api/verify' % VERIFY_SERVER

    request = urllib2.Request (
        url = verify_url,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read ().splitlines ();
    httpresp.close();

    return_code = return_values [0]

    if (return_code == "true"):
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values [1])
