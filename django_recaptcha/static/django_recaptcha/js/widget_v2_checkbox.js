function main() {
  for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

    const widgetUUID = captchaElement.getAttribute("data-widget-uuid");
    if (!widgetUUID) {
      console.warn("reCAPTCHA widget with missing UUID");
      break;
    }
    console.log(`found reCAPTCHA widget with UUID '${widgetUUID}'`);

    const callbackFunctionName = captchaElement.getAttribute("data-callback");
    if (!callbackFunctionName) {
      console.warn(`callback function missing from reCAPTCHA widget with UUID '${widgetUUID}'`);
      break;
    }
    if (window[callbackFunctionName]) {
      console.warn(`callback function '${callbackFunctionName}' has already been added`);
      break;
    }

    window[callbackFunctionName] = (token) => {
      console.log(`reCAPTCHA validated for reCAPTCHA widget with UUID '${widgetUUID}'`);
    };

  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
