document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("select-report-btn");
    const select = document.getElementById("report-select");
  
    button.addEventListener("click", () => {
      const value = select.value;
      if (value) {
        const baseSegments = window.location.pathname.split("/");
        const basePath = baseSegments.length > 1 ? `/${baseSegments[1]}` : "";
        const redirectPath = `${basePath}/report/${value}`;
        window.location.href = redirectPath; // full reload
        console.log("hello");
      } else {
        alert("Please select a report.");
      }
    });
  });
  