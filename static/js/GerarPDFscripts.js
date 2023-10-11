document.addEventListener("DOMContentLoaded", () => {
  const btnGenerate = document.querySelector("#generate-pdf");

  btnGenerate.addEventListener("click", () => {
  //conteudo do PDF
 const body = document.querySelector("body")

 // Configuração do arquivo final de PDF
 const options = {
 margin: [10, 10, 10, 10],
 filename: "Relatório de Férias.pdf",
 html2canvas: {scale: 1 },
 jsPDF: {unit: "mm", format: "a4", orientation: "portrait"}
 }

 // Gerar e baixar o PDF
 html2pdf().set(options).from(body).save();
  });
});