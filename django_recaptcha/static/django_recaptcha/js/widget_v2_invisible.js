function main() {
  for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

    const widgetUUID = captchaElement.getAttribute("data-widget-uuid");
    if (!widgetUUID) {
      continue;  // probably not a reCAPTCHA widget added by django-recaptcha
    }

    const callbackFunctionName = captchaElement.getAttribute("data-callback");
    if (!callbackFunctionName) {
      continue;
    }

    if (window[callbackFunctionName]) {
      continue; // callback function may already have been added by another script
    }

    const formElement = captchaElement.closest("form");
    if (!formElement) {
      console.warn(`reCAPTCHA widget with UUID '${widgetUUID}' is not part of a form`);
      continue;
    }

    formElement.addEventListener("submit", (event) => {
      event.preventDefault();
      grecaptcha.execute();
    });

    window[callbackFunctionName] = (token) => {
      formElement.submit();
    };

  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
