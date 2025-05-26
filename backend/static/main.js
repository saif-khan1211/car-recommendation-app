document.getElementById("predictForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const data = {
    mileage: Number(form.mileage.value),
    rating: Number(form.rating.value),
    price: Number(form.price.value),
    certified: form.certified.value,
    "price drop": Number(form.price_drop.value)
  };

  try {
    const response = await fetch("http://localhost:5001/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    // Update the UI
    document.getElementById("result").textContent =
      `✅ ${result.value_tier} (${result.probability_score}%)`;

    document.getElementById("explanation").textContent = result.explanation;

  } catch (error) {
    document.getElementById("result").textContent = "❌ Something went wrong";
    document.getElementById("explanation").textContent = "";
    console.error(error);
  }
});
