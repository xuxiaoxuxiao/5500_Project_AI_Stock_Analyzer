function useTicker(ticker) {
    document.querySelector("input[name='ticker']").value = ticker;
}

document.querySelector("form").addEventListener("submit", () => {
    document.getElementById("loader").classList.remove("hidden");
});

// Clear recent searches
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("clear-history");
    if (btn) {
        btn.addEventListener("click", async () => {
            await fetch("/clear_history", { method: "POST" });
            window.location.reload();
        });
    }
});
