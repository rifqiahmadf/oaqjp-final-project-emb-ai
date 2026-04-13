async function RunSentimentAnalysis() {
  const textToAnalyze = document.getElementById("textToAnalyze").value;
  const response = await fetch(
    `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`,
  );
  const responseText = await response.text();
  document.getElementById("system_response").innerHTML = responseText;
}

document
  .getElementById("analyzeButton")
  .addEventListener("click", RunSentimentAnalysis);

