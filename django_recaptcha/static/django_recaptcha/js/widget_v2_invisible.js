function main() {
  for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

    const widgetUUID = captchaElement.getAttribute("data-widget-uuid");
    if (!widgetUUID) {
      console.warn("reCAPTCHA widget with missing UUID");
      continue;
    }
    console.log(`found reCAPTCHA widget with UUID '${widgetUUID}'`);

    const callbackFunctionName = captchaElement.getAttribute("data-callback");
    if (!callbackFunctionName) {
      console.warn(`callback function missing from reCAPTCHA widget with UUID '${widgetUUID}'`);
      continue;
    }
    if (window[callbackFunctionName]) {
      console.warn(`callback function '${callbackFunctionName}' has already been added`);
      continue;
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
      console.log(`reCAPTCHA validated for reCAPTCHA widget with UUID '${widgetUUID}'`);
      console.log("submitting form...");
      formElement.submit();
    };

  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
