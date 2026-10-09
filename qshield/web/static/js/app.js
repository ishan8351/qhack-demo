// Q-SHIELD Frontend Application Controller
document.addEventListener("DOMContentLoaded", () => {
    initAmbientHeader();
    initTheme();
    initNavigation();
    initWelcomeHero();
    initSimulator();
    initMoscaSliders();
    initPQCGateway();
    initCopilot();
    
    // Check if CBOM already exists
    fetchLatestCBOM();
});

let currentCBOM = null;

/* 1. Ambient Wave Header Canvas (Slow, continuous quantum probability wave) */
function initAmbientHeader() {
    const canvas = document.getElementById("waveCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = canvas.parentElement.offsetWidth);
    let height = (canvas.height = canvas.parentElement.offsetHeight);

    window.addEventListener("resize", () => {
        width = canvas.width = canvas.parentElement.offsetWidth;
        height = canvas.height = canvas.parentElement.offsetHeight;
    });

    let phase = 0;
    function renderWave() {
        ctx.clearRect(0, 0, width, height);

        const isCreme = document.documentElement.getAttribute("data-theme") === "creme";
        const waveColor = isCreme ? "rgba(2, 132, 199, 0.15)" : "rgba(56, 189, 248, 0.18)";
        const waveColor2 = isCreme ? "rgba(5, 150, 105, 0.08)" : "rgba(16, 185, 129, 0.12)";

        // First gentle sine wave
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        for (let x = 0; x < width; x += 4) {
            const y = Math.sin(x * 0.005 + phase) * 14 + Math.cos(x * 0.002 + phase * 0.5) * 8 + height / 2;
            ctx.lineTo(x, y);
        }
        ctx.strokeStyle = waveColor;
        ctx.lineWidth = 2;
        ctx.stroke();

        // Secondary subtle interference wave
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        for (let x = 0; x < width; x += 4) {
            const y = Math.sin(x * 0.008 - phase * 0.7) * 10 + Math.sin(x * 0.003 + phase) * 6 + height / 2;
            ctx.lineTo(x, y);
        }
        ctx.strokeStyle = waveColor2;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        phase += 0.008; // Very slow, ambient movement
        requestAnimationFrame(renderWave);
    }
    renderWave();
}

/* 2. Theme Management (Creme <-> Slate) */
function initTheme() {
    const themeBtn = document.getElementById("themeToggleBtn");
    const currentTheme = localStorage.getItem("qshield-theme") || "slate";
    document.documentElement.setAttribute("data-theme", currentTheme);
    updateThemeBtnText(currentTheme);

    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            const active = document.documentElement.getAttribute("data-theme") === "creme" ? "slate" : "creme";
            document.documentElement.setAttribute("data-theme", active);
            localStorage.setItem("qshield-theme", active);
            updateThemeBtnText(active);
        });
    }
}

function updateThemeBtnText(theme) {
    const label = document.getElementById("themeLabel");
    if (label) {
        label.textContent = theme === "creme" ? "Theme: Creme" : "Theme: Slate";
    }
}

/* 3. Navigation */
function initNavigation() {
    const pills = document.querySelectorAll(".nav-pill");
    pills.forEach(pill => {
        pill.addEventListener("click", () => {
            pills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");

            const tabName = pill.getAttribute("data-tab");
            document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
            const targetPane = document.getElementById(`tab-${tabName}`);
            if (targetPane) targetPane.classList.add("active");
        });
    });
}

/* 4. Welcome Hero & Benchmark Scanning */
function initWelcomeHero() {
    const scanBtn = document.getElementById("heroScanBtn");
    const uploadInput = document.getElementById("zipUploadInput");

    if (scanBtn) {
        scanBtn.addEventListener("click", () => runScanBenchmark());
    }

    if (uploadInput) {
        uploadInput.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                uploadAndScanZip(e.target.files[0]);
            }
        });
    }
}

async function runScanBenchmark() {
    const progressEl = document.getElementById("scanProgress");
    const barFill = document.getElementById("progressBarFill");
    const statusText = document.getElementById("scanStatusText");
    
    if (progressEl) progressEl.style.display = "block";

    const steps = [
        "Ingesting Polyglot Source Trees (Python, Java, Go, JS)...",
        "Stripping comments and docstrings (Zero False Positive Filter)...",
        "Parsing X.509 certificates and SSH/TLS cipher configurations...",
        "Evaluating Shor & Grover algorithmic vulnerability metrics...",
        "Synthesizing CycloneDX 1.6 Cryptographic Bill of Materials..."
    ];

    for (let i = 0; i < steps.length; i++) {
        if (statusText) statusText.textContent = steps[i];
        if (barFill) barFill.style.width = `${((i + 1) / steps.length) * 85}%`;
        await new Promise(r => setTimeout(r, 200));
    }

    try {
        const resp = await fetch("/api/scan/benchmark", { method: "POST" });
        const data = await resp.json();
        if (barFill) barFill.style.width = "100%";
        if (statusText) statusText.textContent = "Scan complete! Discovered 27 cryptographic assets.";
        await new Promise(r => setTimeout(r, 400));
        
        applyCBOMData(data);
        hideHeroShowDashboard();
    } catch (err) {
        if (statusText) statusText.textContent = `Scan error: ${err.message}`;
    }
}

async function uploadAndScanZip(file) {
    const formData = new FormData();
    formData.append("file", file);

    const statusText = document.getElementById("scanStatusText");
    const progressEl = document.getElementById("scanProgress");
    if (progressEl) progressEl.style.display = "block";
    if (statusText) statusText.textContent = `Uploading & scanning ${file.name}...`;

    try {
        const resp = await fetch("/api/scan/upload", { method: "POST", body: formData });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || "Upload scan failed");
        }
        const data = await resp.json();
        applyCBOMData(data);
        hideHeroShowDashboard();
    } catch (err) {
        alert(`Scan failed: ${err.message}`);
    }
}

function hideHeroShowDashboard() {
    const hero = document.getElementById("welcomeHero");
    const dash = document.getElementById("dashboardContent");
    if (hero) hero.style.display = "none";
    if (dash) dash.style.display = "block";
}

async function fetchLatestCBOM() {
    try {
        const res = await fetch("/api/cbom/latest");
        const data = await res.json();
        if (data && data.total_assets) {
            applyCBOMData(data);
            hideHeroShowDashboard();
        }
    } catch (e) {
        console.log("No initial CBOM to load");
    }
}

function applyCBOMData(data) {
    currentCBOM = data;

    // Header chip
    const meterVal = document.getElementById("headerScoreVal");
    if (meterVal) meterVal.textContent = `${data.readiness_score}/100`;

    // Overview Stats
    const totalEl = document.getElementById("statTotalAssets");
    const vulnEl = document.getElementById("statVulnAssets");
    const scoreEl = document.getElementById("statReadinessScore");
    const targetEl = document.getElementById("statTargetName");

    if (totalEl) totalEl.textContent = data.total_assets;
    if (vulnEl) vulnEl.textContent = data.quantum_vulnerable_count;
    if (scoreEl) scoreEl.textContent = `${data.readiness_score}/100`;
    if (targetEl) targetEl.textContent = data.target_name;

    // Populate CBOM Table
    renderCBOMTable(data.findings);
    loadRoadmap();
}

function renderCBOMTable(findings) {
    const tbody = document.getElementById("cbomTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    findings.forEach(f => {
        const tr = document.createElement("tr");

        let riskBadge = `<span class="badge-broken">Shor Broken</span>`;
        if (f.quantum_risk === "WEAKENED_BY_GROVER") {
            riskBadge = `<span class="badge-weakened">Grover Weakened</span>`;
        } else if (f.quantum_risk === "QUANTUM_RESILIENT") {
            riskBadge = `<span class="badge-safe">Quantum Resilient</span>`;
        }

        tr.innerHTML = `
            <td><code>${f.id}</code></td>
            <td><strong>${f.algorithm}</strong></td>
            <td>${f.asset_type}</td>
            <td><code>${f.file_path}:${f.line_number}</code></td>
            <td>${riskBadge}</td>
            <td><button class="btn-secondary" style="padding: 4px 10px; font-size: 0.76rem;" onclick="viewDiff('${f.id}')">View Diff</button></td>
        `;
        tbody.appendChild(tr);
    });

    // Table Filter
    const searchInput = document.getElementById("cbomSearchInput");
    if (searchInput) {
        searchInput.oninput = (e) => {
            const query = e.target.value.toLowerCase();
            const rows = tbody.querySelectorAll("tr");
            rows.forEach(r => {
                r.style.display = r.textContent.toLowerCase().includes(query) ? "" : "none";
            });
        };
    }
}

/* 5. Quantum Threat Simulator */
function initSimulator() {
    const runBtn = document.getElementById("runShorBtn");
    const selectN = document.getElementById("shorModulusSelect");

    if (runBtn) {
        runBtn.addEventListener("click", async () => {
            const N = parseInt(selectN.value, 10);
            runBtn.disabled = true;
            runBtn.textContent = "Simulating Statevector IQFT...";

            try {
                const res = await fetch("/api/quantum/shor", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ N: N })
                });
                const data = await res.json();
                renderShorResults(data);
            } catch (err) {
                alert(`Simulation failed: ${err.message}`);
            } finally {
                runBtn.disabled = false;
                runBtn.textContent = "Run Shor Period-Finding";
            }
        });
    }

    // Auto-run on load for N=143
    setTimeout(() => {
        if (runBtn) runBtn.click();
    }, 500);
}

function renderShorResults(data) {
    const outBox = document.getElementById("shorOutputText");
    const svgWrap = document.getElementById("shorSvgWrap");

    const sim = data.simulation;
    const fact = data.factor_result;

    if (outBox) {
        outBox.innerHTML = `
<strong>Target Modulus N:</strong> ${sim.N} | <strong>Base a:</strong> ${sim.base_a}
<strong>Order r:</strong> ${sim.true_order_r} | <strong>Register Size Q:</strong> ${sim.register_size_Q} states (${sim.true_order_r}-fold symmetry)
<strong>Interference Peaks Spacing (Q/r):</strong> ${sim.peak_spacing}
<strong>Measured State Peaks:</strong> [${sim.peak_indices.join(", ")}]
<strong>Factored Result:</strong> ${fact.factor_1} × ${fact.factor_2} = ${sim.N} (${fact.method})
        `;
    }

    // Render SVG Probability Peaks
    if (svgWrap && sim.sampled_peaks) {
        const svgW = 560;
        const svgH = 180;
        const maxState = sim.register_size_Q;

        let bars = sim.sampled_peaks.map(p => {
            const x = (p.state / maxState) * (svgW - 80) + 40;
            const barH = p.prob * 500;
            const y = svgH - 30 - barH;
            return `
                <line x1="${x}" y1="${svgH - 30}" x2="${x}" y2="${y}" stroke="var(--accent-primary)" stroke-width="4" stroke-linecap="round"/>
                <circle cx="${x}" cy="${y}" r="4" fill="var(--accent-primary)"/>
                <text x="${x}" y="${svgH - 12}" font-size="10" fill="var(--text-secondary)" text-anchor="middle" font-family="monospace">${p.state}</text>
            `;
        }).join("");

        svgWrap.innerHTML = `
            <svg width="100%" height="${svgH}" viewBox="0 0 ${svgW} ${svgH}" style="background: var(--bg-base); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <line x1="30" y1="${svgH - 30}" x2="${svgW - 20}" y2="${svgH - 30}" stroke="var(--border-strong)" stroke-width="1"/>
                ${bars}
                <text x="15" y="${svgH / 2}" font-size="11" fill="var(--text-muted)" transform="rotate(-90 15,${svgH/2})" text-anchor="middle">|ψ|²</text>
            </svg>
        `;
    }
}

/* 6. Mosca's Inequality Sliders */
function initMoscaSliders() {
    const sX = document.getElementById("sliderX");
    const sY = document.getElementById("sliderY");
    const sZ = document.getElementById("sliderZ");

    const vX = document.getElementById("valX");
    const vY = document.getElementById("valY");
    const vZ = document.getElementById("valZ");

    async function updateMosca() {
        if (!sX || !sY || !sZ) return;
        const X = parseFloat(sX.value);
        const Y = parseFloat(sY.value);
        const Z = parseFloat(sZ.value);

        vX.textContent = `${X}y`;
        vY.textContent = `${Y}y`;
        vZ.textContent = `${Z}y`;

        const resp = await fetch("/api/risk/mosca", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ shelf_life_years: X, migration_time_years: Y, q_day_years: Z })
        });
        const data = await resp.json();

        const statusBadge = document.getElementById("moscaExposureBadge");
        const horizonEl = document.getElementById("moscaHorizonText");
        const verdictEl = document.getElementById("moscaVerdictText");

        if (statusBadge) {
            statusBadge.textContent = data.exposure_level;
            statusBadge.className = data.is_at_risk ? "badge-broken" : "badge-safe";
        }
        if (horizonEl) {
            horizonEl.textContent = `Horizon: X + Y = ${data.total_risk_horizon}y vs Q-Day (Z) = ${data.q_day_years_Z}y`;
        }
        if (verdictEl) verdictEl.textContent = data.verdict;
    }

    if (sX) sX.oninput = updateMosca;
    if (sY) sY.oninput = updateMosca;
    if (sZ) sZ.oninput = updateMosca;
    updateMosca();
}

/* 7. PQC Gateway & Attack Playground */
function initPQCGateway() {
    const sendBtn = document.getElementById("pqcSendBtn");
    const tamperBtn = document.getElementById("pqcTamperBtn");
    const replayBtn = document.getElementById("pqcReplayBtn");
    const inputMsg = document.getElementById("pqcMsgInput");
    const chatStream = document.getElementById("pqcChatStream");

    if (sendBtn) {
        sendBtn.addEventListener("click", async () => {
            const msg = inputMsg.value.trim() || "AUTHORIZE WIRE TRANSFER #9872";
            appendChat("user", msg);
            inputMsg.value = "";

            const res = await fetch("/api/pqc/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            appendChat("agent", `🛡️ [ML-KEM-768/AES-256-GCM Verified] Server Received: "${data.verified_decrypted}" (Ciphertext: ${data.ciphertext_hex})`);
        });
    }

    if (tamperBtn) {
        tamperBtn.addEventListener("click", async () => {
            appendChat("user", "⚠️ INJECTING ADVERSARIAL BIT-FLIP TAMPER IN TRANSMISSION...");
            const res = await fetch("/api/pqc/attack/tamper", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: "TAMPER TEST PAYLOAD" })
            });
            const data = await res.json();
            appendChat("agent", `🚨 [ATTACK MITIGATED] ${data.error} — ${data.action}`);
        });
    }

    if (replayBtn) {
        replayBtn.addEventListener("click", async () => {
            appendChat("user", "🔄 SIMULATING REPLAY ATTACK (DUPLICATING TRANSMITTED PACKET)...");
            const res = await fetch("/api/pqc/attack/replay", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: "REPLAY TRANSACTION" })
            });
            const data = await res.json();
            appendChat("agent", `🛑 [ATTACK MITIGATED] ${data.error} — ${data.action}`);
        });
    }
}

function appendChat(role, text) {
    const stream = document.getElementById("pqcChatStream");
    if (!stream) return;
    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.textContent = text;
    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
}

/* 8. Migration Roadmap */
async function loadRoadmap() {
    const listEl = document.getElementById("roadmapPhaseList");
    if (!listEl) return;
    try {
        const res = await fetch("/api/migration/roadmap");
        const phases = await res.json();
        listEl.innerHTML = "";

        phases.forEach(p => {
            const card = document.createElement("div");
            card.className = "stat-card";
            card.style.marginBottom = "16px";
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="font-size: 1rem; font-weight: 700;">${p.title}</h3>
                    <span class="badge-safe">Target Readiness: ${p.target_readiness}/100</span>
                </div>
                <p style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 10px;">${p.description}</p>
                <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--accent-primary);">
                    Impacted Assets (${p.count}): ${p.findings.map(f => f.id).join(", ") || "None"}
                </div>
            `;
            listEl.appendChild(card);
        });
    } catch (e) {
        console.error("Roadmap error", e);
    }
}

/* View Diff Modal / Display */
window.viewDiff = async function(findingId) {
    try {
        const res = await fetch(`/api/migration/diff/${findingId}`);
        const data = await res.json();
        alert(`Finding: ${findingId}\n\nRecommended Replacement:\n${data.finding.recommended_replacement}\n\nProposed Code Diff:\n${data.diff}`);
    } catch (e) {
        alert("Diff not found");
    }
};

/* 9. AI Copilot */
function initCopilot() {
    const sendBtn = document.getElementById("copilotSendBtn");
    const input = document.getElementById("copilotInput");
    const stream = document.getElementById("copilotStream");

    async function sendPrompt(query) {
        if (!query.trim()) return;
        appendCopilot("user", query);
        input.value = "";

        try {
            const res = await fetch("/api/copilot/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            });
            const data = await res.json();
            appendCopilot("agent", data.answer);
        } catch (e) {
            appendCopilot("agent", `Copilot error: ${e.message}`);
        }
    }

    if (sendBtn) {
        sendBtn.addEventListener("click", () => sendPrompt(input.value));
    }
    if (input) {
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") sendPrompt(input.value);
        });
    }

    // Chip prompt click
    window.askChip = function(text) {
        sendPrompt(text);
    };
}

function appendCopilot(role, text) {
    const stream = document.getElementById("copilotStream");
    if (!stream) return;
    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.innerHTML = text.replace(/\n/g, "<br/>");
    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
}
