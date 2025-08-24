/* Turn png to gif on hover */
document.querySelectorAll(".li_divider img[data-id]").forEach((img) => {
    console.log(img);
    img.addEventListener("mouseenter", () => {
        img.src = `/static/media/import_${img.dataset.id}.gif`;
    });

    img.addEventListener("mouseleave", () => {
        img.src = `/static/media/import_${img.dataset.id}_still.png`;
    });
});