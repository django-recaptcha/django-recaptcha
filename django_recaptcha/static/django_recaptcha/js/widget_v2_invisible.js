(function () {

  function main() {
    for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

      const widgetUuid = captchaElement.getAttribute("data-widget-uuid");
      if (!widgetUuid) {
        console.warn("reCAPTCHA widget with missing UUID");
        break;
      }
      console.log(`found reCAPTCHA widget with UUID '${widgetUuid}'`);

      const callbackFunctionName = captchaElement.getAttribute("data-callback");
      if (!callbackFunctionName) {
        console.warn(`callback function missing from reCAPTCHA widget with UUID '${widgetUuid}'`);
        break;
      }
      if (window.hasOwnProperty(callbackFunctionName)) {
        console.warn(`callback function '${callbackFunctionName}' has already been added`);
        break;
      }

      const formElement = captchaElement.closest("form");
      if (!formElement) {
        console.warn(`reCAPTCHA widget with UUID '${widgetUuid}' is not part of a form`);
        break;
      }

      formElement.addEventListener("submit", (event) => {
        event.preventDefault();
        grecaptcha.execute();
      });

      window[callbackFunctionName] = (token) => {
        console.log(`reCAPTCHA validated for reCAPTCHA widget with UUID '${widgetUuid}'`);
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

})();
