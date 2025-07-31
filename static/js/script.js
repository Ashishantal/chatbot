function triggerFileInput(event) {
  if (!document.getElementById("pdf-preview").style.display || document.getElementById("pdf-preview").style.display === "none") {
    document.getElementById("fileInput").click();
  }
}

function previewPDF(event) {
  const file = event.target.files[0];
  if (!file || file.type !== 'application/pdf') return;

  const reader = new FileReader();
  reader.onload = function () {
    document.getElementById("preview-frame").src = reader.result;
    document.getElementById("pdf-preview").style.display = "block";
    document.getElementById("upload-placeholder").style.display = "none";
  };
  reader.readAsDataURL(file);
}

function removePDF(event) {
  event.stopPropagation();
  document.getElementById("fileInput").value = '';
  document.getElementById("preview-frame").src = '';
  document.getElementById("pdf-preview").style.display = "none";
  document.getElementById("upload-placeholder").style.display = "flex";
}
