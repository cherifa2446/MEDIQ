const patientName = document.getElementById("patientName");
const globalStatusBadge = document.getElementById("globalStatusBadge");

const metricId = document.getElementById("metricId");
const metricHeure = document.getElementById("metricHeure");
const metricFc = document.getElementById("metricFc");
const metricTa = document.getElementById("metricTa");
const metricFr = document.getElementById("metricFr");
const metricSat = document.getElementById("metricSat");
const metricTemp = document.getElementById("metricTemp");
const metricMed = document.getElementById("metricMed");
const metricAdmin = document.getElementById("metricAdmin");
const metricScore = document.getElementById("metricScore");

const alertTitle = document.getElementById("alertTitle");
const alertContent = document.getElementById("alertContent");
const timelineContainer = document.getElementById("timelineContainer");

let timelineData = [];
let currentIndex = 0;
let intervalId = null;
let currentSpeed = 2000;

async function loadTimelineData() {
  try {
    const response = await fetch("./timeline_results.json");

    if (!response.ok) {
      throw new Error("Impossible de charger timeline_results.json");
    }

    timelineData = await response.json();

    if (!Array.isArray(timelineData)) {
      timelineData = [];
    }

    console.log("Timeline chargée :", timelineData);

  } catch (error) {
    console.error(error);
    timelineData = [];
    timelineContainer.innerHTML = `
      <div class="empty-timeline">
        Erreur de chargement du fichier timeline_results.json
      </div>
    `;
  }
}

function normalizeStatus(status) {
  const s = (status || "").toLowerCase();

  if (s.includes("critique")) return "critique";
  if (s.includes("inhabituel")) return "inhabituel";
  return "normal";
}

function setBadgeStatus(status, label) {
  globalStatusBadge.className = `status-badge ${status}`;
  globalStatusBadge.textContent = label;
}

function setAlertBox(status, alerts) {
  alertContent.classList.remove("safe", "warning", "danger");

  if (!alerts || alerts.length === 0) {
    alertTitle.textContent = "Aucune alerte détectée";
    alertContent.classList.add("safe");
    alertContent.textContent = "Administration conforme. Aucun comportement suspect détecté.";
    return;
  }

  if (status === "critique") {
    alertTitle.textContent = "ALERTE CRITIQUE";
    alertContent.classList.add("danger");
  } else {
    alertTitle.textContent = "Alerte inhabituelle";
    alertContent.classList.add("warning");
  }

  alertContent.innerHTML = alerts.map(alert => `<div>• ${alert}</div>`).join("");
}

function formatValue(value, suffix = "") {
  if (value === null || value === undefined || value === "") {
    return "--";
  }
  return `${value}${suffix}`;
}

function formatTA(sys, dia) {
  const s = sys ?? "--";
  const d = dia ?? "--";
  return `${s} / ${d}`;
}

function updatePatientPanel(item) {
  const status = normalizeStatus(item.status);

  patientName.textContent = `Patient ${item.ID ?? "--"}`;
  metricId.textContent = formatValue(item.ID);
  metricHeure.textContent = formatValue(item.Heure);
  metricFc.textContent = formatValue(item.FC);
  metricTa.textContent = formatTA(item.TA_Sys, item.TA_Dia);
  metricFr.textContent = formatValue(item.FR);
  metricSat.textContent = formatValue(item.SAT);
  metricTemp.textContent = formatValue(item.Temp);
  metricMed.textContent = formatValue(item.Medicament);
  metricAdmin.textContent = formatValue(item.Administration);
  metricScore.textContent = formatValue(item.score, "");

  setBadgeStatus(status, item.status || "Normal");
  setAlertBox(status, item.alerts);
}

function createTimelineItem(item) {
  const status = normalizeStatus(item.status);
  const firstAlert =
    item.alerts && item.alerts.length > 0
      ? item.alerts[0]
      : "Aucune alerte";

  const div = document.createElement("div");
  div.className = `timeline-item ${status} new-entry`;

  div.innerHTML = `
    <div class="timeline-time">${formatValue(item.Heure, "")}</div>
    <div class="timeline-patient">Patient ${formatValue(item.ID, "")}</div>

    <div class="timeline-main">
      <div class="timeline-med">${formatValue(item.Medicament)}</div>
      <div class="timeline-admin">Administration : ${formatValue(item.Administration)}</div>

      <div class="timeline-vitals">
        <div>FC : ${formatValue(item.FC)}</div>
        <div>TA : ${formatTA(item.TA_Sys, item.TA_Dia)}</div>
        <div>FR : ${formatValue(item.FR)}</div>
        <div>SAT : ${formatValue(item.SAT)}</div>
        <div>Temp : ${formatValue(item.Temp)}</div>
      </div>

      <div class="timeline-alert">${firstAlert}</div>
    </div>

    <div class="timeline-score">Score ${formatValue(item.score, "")}</div>
  `;

  setTimeout(() => {
    div.classList.remove("new-entry");
  }, 700);

  return div;
}

function playNextStep() {
  if (currentIndex >= timelineData.length) {
    stopSimulation();
    return;
  }

  const item = timelineData[currentIndex];
  updatePatientPanel(item);

  const timelineItem = createTimelineItem(item);
  timelineContainer.prepend(timelineItem);

  currentIndex++;
}

function startSimulation() {
  if (timelineData.length === 0) return;
  if (intervalId !== null) return;

  playNextStep();
  intervalId = setInterval(playNextStep, currentSpeed);
}

function stopSimulation() {
  if (intervalId !== null) {
    clearInterval(intervalId);
    intervalId = null;
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  await loadTimelineData();

  if (timelineData.length > 0) {
    timelineContainer.innerHTML = "";
    startSimulation();
  } else {
    timelineContainer.innerHTML = `
      <div class="empty-timeline">Aucune donnée trouvée.</div>
    `;
  }
});
