document.getElementById("ask").addEventListener("click", async () => {
    const input = document.getElementById("input").value;
    const responseBox = document.getElementById("response");
    responseBox.textContent = "Thinking...";

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: input })
        });

        const data = await res.json();

        if (data.reply) {
            responseBox.textContent = data.reply;
        } else if (data.error) {
            responseBox.textContent = "Error del servidor: " + data.error;
        }
    } catch (e) {
        responseBox.textContent = "Error de conexión o JSON inválido: " + e.message;
    }
});