document.querySelectorAll(".checkbox [type=checkbox]").forEach(e => e.onchange = toggleServices);
function toggleServices(e) {
    let sums = [10, 0, 0];
    document.querySelectorAll(".checkbox [type=checkbox]:checked")
        .forEach(e => sums.forEach((e2, i, a) => a[i] += +e.dataset["cost" + (i + 1)]));
    sums.forEach((e, i) => { document.getElementById("aClassPrice-" + (i + 1)).textContent = e; });
}