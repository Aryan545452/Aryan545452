async function sendCommand(robot, left, right) {
  try {
    const res = await fetch(`/api/command/${robot}`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({left, right})
    });
    if (!res.ok) throw new Error("request failed");

    const card = document.querySelector(`[data-robot="${robot}"]`);
    card.querySelector(".left").textContent = left;
    card.querySelector(".right").textContent = right;
    document.querySelector("#status").textContent = "متصل";
  } catch (e) {
    document.querySelector("#status").textContent = "خطا در ارتباط با سرور";
  }
}

document.querySelectorAll(".robot").forEach(card => {
  const robot = card.dataset.robot;
  card.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("click", () => {
      sendCommand(robot, Number(btn.dataset.l), Number(btn.dataset.r));
    });
  });
});

document.querySelector("#stopAll").addEventListener("click", async () => {
  await fetch("/api/stop", {method: "POST"});
  document.querySelectorAll(".robot").forEach(card => {
    card.querySelector(".left").textContent = "0";
    card.querySelector(".right").textContent = "0";
  });
});
