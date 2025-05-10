function main() {
  grecaptcha.ready(function () {
    for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

      const widgetUUID = captchaElement.getAttribute("data-widget-uuid");
      if (!widgetUUID) {
        console.warn("reCAPTCHA widget with missing UUID");
        break;
      }
      console.log(`found reCAPTCHA widget with UUID '${widgetUUID}'`);

      const formElement = captchaElement.closest("form");
      if (!formElement) {
        console.warn(`reCAPTCHA widget with UUID '${widgetUUID}' is not part of a form`);
        break;
      }

      const publicKey = captchaElement.getAttribute("data-sitekey");
      if (publicKey === null) {
        console.warn(`public key missing missing from reCAPTCHA widget with UUID '${widgetUUID}'`);
        break;
      }

      const actionName = captchaElement.getAttribute("data-action");
      const config = {};
      if (actionName !== null) {
        config.action = actionName;
      }

      formElement.addEventListener("submit", function (event) {
        event.preventDefault();
        grecaptcha.execute(publicKey, config)
          .then(function (token) {
            console.log(`reCAPTCHA validated for reCAPTCHA widget with UUID '${widgetUUID}'`);
            captchaElement.value = token;
            console.log("submitting form...");
            formElement.submit();
          });
      });

    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
