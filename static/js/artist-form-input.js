document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
  
    form.addEventListener("submit", async (event) => {
      event.preventDefault(); // Prevent page reload
  
      const formData = {
        interview_date: form.interview_date.value,
        interviewer_name: form.interviewer_name.value,
        artist_last_name: form.artist_last_name.value,
        artist_first_name: form.artist_first_name.value,
        street: form.street.value,
        city: form.city.value,
        state: form.state.value,
        zip: form.zip.value,
        area_code: form.area_code.value,
        phone_number: form.phone_number.value,
        ssn: form.ssn.value,
        usual_type: form.usual_type.value,
        usual_medium: form.usual_medium.value,
        usual_style: form.usual_style.value,
      };
  
      try {
        const response = await fetch("/form/artist-form", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });
  
        if (response.ok) {
          alert("Form submitted successfully!");
          form.reset();
        } else {
          alert("Failed to submit form.");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
      }
    });
  });
  