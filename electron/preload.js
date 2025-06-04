const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("api", {
  askBot: async (question) => {
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    return data.answer;
  },
});
