function useTicker(ticker) {
    document.querySelector("input[name='ticker']").value = ticker;
}

document.querySelector("form").addEventListener("submit", () => {
    document.getElementById("loader").classList.remove("hidden");
});
