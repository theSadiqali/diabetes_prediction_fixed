 
/*
document.getElementById("prediction-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const data = {
        Pregnancies: parseFloat(form.Pregnancies.value),
        Glucose: parseFloat(form.Glucose.value),
        BloodPressure: parseFloat(form.BloodPressure.value),
        SkinThickness: parseFloat(form.SkinThickness.value),
        Insulin: parseFloat(form.Insulin.value),
        BMI: parseFloat(form.BMI.value),
        DiabetesPedigreeFunction: parseFloat(form.DiabetesPedigreeFunction.value),
        Age: parseFloat(form.Age.value),
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/predict/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        document.getElementById("result").textContent = 
            `Probability of diabetes: ${(result.probability * 100).toFixed(2)}%`;
    } catch (err) {
        document.getElementById("result").textContent = "Error: " + err;
    }
});
