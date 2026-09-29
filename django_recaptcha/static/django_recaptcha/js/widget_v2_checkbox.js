function main() {
  for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

    const widgetUUID = captchaElement.getAttribute("data-widget-uuid");
    if (!widgetUUID) {
      continue;  // probably not a reCAPTCHA widget added by django-recaptcha
    }

    const recaptchaType = captchaElement.getAttribute("data-recaptcha-type");
    if (recaptchaType !== "classic-v2-checkbox") {
      continue;
    }

    const callbackFunctionName = captchaElement.getAttribute("data-callback");
    if (!callbackFunctionName) {
      continue;
    }

    if (window[callbackFunctionName]) {
      continue; // callback function may already have been added by another script
    }

    window[callbackFunctionName] = (token) => {
      // called when user clicks checkbox; use for debugging purposes
    };

  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
