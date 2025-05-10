function main() {
  grecaptcha.ready(function () {
    for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

      const widgetUUID = captchaElement.getAttribute("data-widget-uuid");
      if (!widgetUUID) {
        continue; // probably not a reCAPTCHA widget added by django-recaptcha
      }

      const formElement = captchaElement.closest("form");
      if (!formElement) {
        console.warn(`reCAPTCHA widget with UUID '${widgetUUID}' is not part of a form`);
        continue;
      }

      const publicKey = captchaElement.getAttribute("data-sitekey");
      if (publicKey === null) {
        console.warn(`public key missing missing from reCAPTCHA widget with UUID '${widgetUUID}'`);
        continue;
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
            captchaElement.value = token;
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
