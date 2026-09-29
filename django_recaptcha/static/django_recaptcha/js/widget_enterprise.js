/* Renders any reCAPTCHA widget with class "django-recaptcha-widget". */
(function() {

  /* Prepare grecaptcha.enterprise.ready() if necessary. */
  let cfg = window["___grecaptcha_cfg"] = window["___grecaptcha_cfg"] || {};
  let a = window["grecaptcha"] = window["grecaptcha"] || {};
  let gr = a["enterprise"] = a["enterprise"] || {};
  gr.ready = gr.ready || function(f) { (cfg["fns"] = cfg["fns"] || []).push(f);};

  /* Do actual work once reCAPTCHA has finished loading. */
  grecaptcha.enterprise.ready(() => {
    for (let widgetEl of document.querySelectorAll("django-recaptcha-widget-enterprise")) {

      let form = widgetEl.closest("form");
      if (!form) {
        continue;  // must be part of a form!
      }

      let sitekey = widgetEl.getAttribute("data-sitekey");
      if (!sitekey) {
        continue;  // must have a sitekey!
      }

      try {
        widgetID = grecaptcha.enterprise.render(widgetEl);
      } catch (error) {
        continue;  // already rendered!
      }

      if (!form.querySelector(".grecaptcha-badge")) {
        continue;  // is a checkbox widget; doesn't require event listener!
      }

      // Fetch token of non-interactive widgets right before submission.
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        grecaptcha.enterprise.execute(widgetID)
          .then(() => {
            form.submit();
          });
      });

    }
  });

})();
