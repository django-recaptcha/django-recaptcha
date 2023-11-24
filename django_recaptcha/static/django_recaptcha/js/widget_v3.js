(function () {

  function main() {
    grecaptcha.ready(function () {
      for (const captchaElement of document.querySelectorAll(".g-recaptcha")) {

        const widgetUuid = captchaElement.getAttribute("data-widget-uuid");
        if (!widgetUuid) {
          console.warn("reCAPTCHA widget with missing UUID");
          break;
        }
        console.log(`found reCAPTCHA widget with UUID '${widgetUuid}'`);

        const formElement = captchaElement.closest("form");
        if (!formElement) {
          console.warn("reCAPTCHA widget with UUID '" + widgetUuid + "' is not part of a form");
          break;
        }

        const publicKey = captchaElement.getAttribute("data-sitekey");
        if (publicKey === null) {
          console.warn("public key missing missing from reCAPTCHA widget with UUID '" + widgetUuid + "'");
          break;
        }

        const action = {};
        Object.assign(action, {action: captchaElement.getAttribute("data-action")});

        formElement.addEventListener("submit", function (event) {
          event.preventDefault();
          grecaptcha.execute(publicKey, action)
            .then(function (token) {
              console.log("reCAPTCHA validated for reCAPTCHA widget with UUID '" + widgetUuid + "'");
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

})();
