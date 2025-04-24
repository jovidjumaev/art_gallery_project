document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".nav-link");
  const main = document.getElementById("main-content");

  links.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const relativePath = link.getAttribute("data-url"); // e.g. "/report"

      const fullPath = BASE_PATH + relativePath; // cleanly prepended

      fetch(fullPath)
        .then(res => res.text())
        .then(html => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const newContent = doc.getElementById("main-content").innerHTML;
          main.innerHTML = newContent;
          history.pushState(null, "", fullPath);
        })
        .catch(err => {
          console.error("Error loading page:", err);
          main.innerHTML = "<p>Failed to load content.</p>";
        });
    });
  });

  window.addEventListener("popstate", () => location.reload());
});
