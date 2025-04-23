
console.log("🔥 form-select.js loaded");

window.addEventListener("pageshow", (event) => {
    const navType = performance.getEntriesByType("navigation")[0].type;
    console.log("📦 pageshow event. Navigation type:", navType);
    setupFormSelection();
  });
  


function setupFormSelection() {
    const button = document.getElementById("select-form-btn");
    const select = document.getElementById("form-select");
  
    if (!button || !select) {
      console.warn("Button or select not found.");
      return;
    }
  
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);
  
    newButton.addEventListener("click", (e) => {
      e.preventDefault();
      const value = select.value;
      if (value) {
        window.location.href = `/form/${value}`;
      } else {
        alert("Please select a form.");
      }
    });
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    setupFormSelection();
  });
  
  window.addEventListener("pageshow", (event) => {
    setupFormSelection();
  });
  