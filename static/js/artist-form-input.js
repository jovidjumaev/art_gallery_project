document.addEventListener('DOMContentLoaded', function () {
  // Set today's date as the max value
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  const maxDate = `${year}-${month}-${day}`;
  document.getElementById('interviewDate').setAttribute('max', maxDate);

  // Function to handle showing/hiding "Other" text input
  function handleOtherOption(selectId, otherInputId) {
    const selectElement = document.getElementById(selectId);
    const otherInputElement = document.getElementById(otherInputId);

    selectElement.addEventListener('change', function () {
      if (selectElement.value === 'Other') {
        otherInputElement.classList.remove('hidden');
        otherInputElement.required = true;
      } else {
        otherInputElement.classList.add('hidden');
        otherInputElement.required = false;
        otherInputElement.value = ''; // Clear if not needed
      }
    });
  }

  // Attach event handlers to your selects
  handleOtherOption('typeSelect', 'otherType');
  handleOtherOption('mediumSelect', 'otherMedium');
  handleOtherOption('styleSelect', 'otherStyle');
});