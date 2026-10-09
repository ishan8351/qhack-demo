// Q-SHIELD Presentation Console Application Controller (High Energy & Animated)
document.addEventListener("DOMContentLoaded", () => {
    initAmbientHeader();
    initTheme();
    initStepper();
    initWelcomeHero();
    initMoscaSliders();
    initQuantumSuite();
    initPQCDiffenseSuite();
    initCopilot();
    
    // Check if initial CBOM exists
    fetchLatestCBOM();
});

let currentCBOM = null;
let currentStep = 1;

/* ========================================================================== */
/* 1. Ambient Wave Header with Floating Quantum Particles & Mouse Ripple      */
/* ========================================================================== */
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

    // Interactive mouse displacement
    let mouseX = -1000;
    let mouseY = -1000;
    canvas.parentElement.addEventListener("mousemove", (e) => {
        const rect = canvas.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;
    });
    canvas.parentElement.addEventListener("mouseleave", () => {
        mouseX = -1000;
        mouseY = -1000;
    });

    // Floating quantum probability particles
    const particles = [];
    for (let p = 0; p < 28; p++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.6,
            vy: (Math.random() - 0.5) * 0.4,
            radius: Math.random() * 2.2 + 1,
            color: p % 3 === 0 ? "rgba(0, 240, 255, 0.45)" : p % 3 === 1 ? "rgba(168, 85, 247, 0.45)" : "rgba(16, 185, 129, 0.4)",
            pulse: Math.random() * Math.PI
        });
    }

    let phase = 0;
    function renderWave() {
        ctx.clearRect(0, 0, width, height);

        const isCreme = document.documentElement.getAttribute("data-theme") === "creme";
        const cyanColor = isCreme ? "rgba(2, 132, 199, 0.22)" : "rgba(0, 240, 255, 0.28)";
        const purpleColor = isCreme ? "rgba(124, 58, 237, 0.16)" : "rgba(168, 85, 247, 0.22)";
        const greenColor = isCreme ? "rgba(5, 150, 105, 0.14)" : "rgba(16, 185, 129, 0.18)";

        // 1. Primary Quantum Wave (Cyan)
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        for (let x = 0; x < width; x += 4) {
            let dy = 0;
            const dist = Math.abs(x - mouseX);
            if (dist < 140) {
                dy = Math.sin((dist / 140) * Math.PI) * 16;
            }
            const y = Math.sin(x * 0.005 + phase) * 14 + Math.cos(x * 0.002 + phase * 0.5) * 8 + dy + height / 2;
            ctx.lineTo(x, y);
        }
        ctx.strokeStyle = cyanColor;
        ctx.lineWidth = 2.5;
        ctx.stroke();

        // 2. Secondary Harmonic Wave (Violet / Purple)
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        for (let x = 0; x < width; x += 4) {
            const y = Math.sin(x * 0.008 - phase * 0.7) * 11 + Math.sin(x * 0.003 + phase) * 7 + height / 2;
            ctx.lineTo(x, y);
        }
        ctx.strokeStyle = purpleColor;
        ctx.lineWidth = 2;
        ctx.stroke();

        // 3. Subtle Base Resonance Wave (Emerald)
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        for (let x = 0; x < width; x += 4) {
            const y = Math.cos(x * 0.004 + phase * 0.4) * 9 + height / 2;
            ctx.lineTo(x, y);
        }
        ctx.strokeStyle = greenColor;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // 4. Update and Render Floating Particles
        particles.forEach(pt => {
            pt.x += pt.vx;
            pt.y += pt.vy;
            pt.pulse += 0.03;

            if (pt.x < 0) pt.x = width;
            if (pt.x > width) pt.x = 0;
            if (pt.y < 0) pt.y = height;
            if (pt.y > height) pt.y = 0;

            const currentR = pt.radius + Math.sin(pt.pulse) * 0.6;
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, Math.max(currentR, 0.8), 0, Math.PI * 2);
            ctx.fillStyle = pt.color;
            ctx.fill();
        });

        phase += 0.01;
        requestAnimationFrame(renderWave);
    }
    renderWave();
}

/* ========================================================================== */
/* 2. Theme Management (Creme <-> Slate)                                      */
/* ========================================================================== */
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

/* ========================================================================== */
/* 3. Persistent Guided Stepper Navigation                                   */
/* ========================================================================== */
function initStepper() {
    const stepBtns = document.querySelectorAll(".step-btn");
    stepBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const stepNum = parseInt(btn.getAttribute("data-step"), 10);
            goToStep(stepNum);
        });
    });
}

window.goToStep = function(stepNum) {
    currentStep = stepNum;

    // Update Step Buttons
    const stepBtns = document.querySelectorAll(".step-btn");
    stepBtns.forEach(btn => {
        const num = parseInt(btn.getAttribute("data-step"), 10);
        btn.classList.remove("active");
        if (num < stepNum) {
            btn.classList.add("completed");
        } else {
            btn.classList.remove("completed");
        }
        if (num === stepNum) {
            btn.classList.add("active");
        }
    });

    // Update Progress Fill Line
    const progressFill = document.getElementById("stepperProgressFill");
    if (progressFill) {
        const percent = ((stepNum - 1) / 4) * 100;
        progressFill.style.width = `${Math.max(percent, 8)}%`;
    }

    // Switch Visible Panes
    document.querySelectorAll(".step-pane").forEach(pane => pane.classList.remove("active"));
    const activePane = document.getElementById(`pane-step-${stepNum}`);
    if (activePane) {
        activePane.classList.add("active");
    }

    // Smooth Scroll to Top of Canvas
    window.scrollTo({ top: 70, behavior: "smooth" });
};

/* ========================================================================== */
/* 4. Welcome Hero & Benchmark Scanning                                      */
/* ========================================================================== */
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
        "Traversing Polyglot Source Trees (Python, Java, Go, JS)...",
        "Stripping comments and docstrings (Zero False Positive Filter)...",
        "Parsing X.509 certificates and Nginx/SSH TLS cipher directives...",
        "Evaluating Shor prime-factoring & Grover key space degradation...",
        "Synthesizing CycloneDX 1.6 Cryptographic Bill of Materials..."
    ];

    for (let i = 0; i < steps.length; i++) {
        if (statusText) statusText.textContent = steps[i];
        if (barFill) barFill.style.width = `${((i + 1) / steps.length) * 85}%`;
        await new Promise(r => setTimeout(r, 180));
    }

    try {
        const resp = await fetch("/api/scan/benchmark", { method: "POST" });
        const data = await resp.json();
        if (barFill) barFill.style.width = "100%";
        if (statusText) statusText.textContent = "Scan complete! Discovered 27 cryptographic assets.";
        await new Promise(r => setTimeout(r, 350));
        
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
    if (statusText) statusText.textContent = `Analyzing ${file.name}...`;

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
        console.log("No initial scan on startup");
    }
}

function applyCBOMData(data) {
    currentCBOM = data;

    // Header score chip
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

    // Populate CBOM Table & Roadmap
    renderCBOMTable(data.findings);
    loadRoadmap();
}

function renderCBOMTable(findings) {
    const tbody = document.getElementById("cbomTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    findings.forEach(f => {
        const tr = document.createElement("tr");

        let riskBadge = `<span class="badge-broken glow-red">Shor Broken</span>`;
        if (f.quantum_risk === "WEAKENED_BY_GROVER") {
            riskBadge = `<span class="badge-weakened">Grover Weakened</span>`;
        } else if (f.quantum_risk === "QUANTUM_RESILIENT") {
            riskBadge = `<span class="badge-safe glow-green">Quantum Resilient</span>`;
        }

        tr.innerHTML = `
            <td><code>${f.id}</code></td>
            <td><strong>${f.algorithm}</strong></td>
            <td>${f.asset_type}</td>
            <td><code>${f.file_path}:${f.line_number}</code></td>
            <td>${riskBadge}</td>
            <td><button class="btn-secondary" style="padding: 4px 10px; font-size: 0.76rem;" onclick="openDiffModal('${f.id}')">Inspect Diff</button></td>
        `;
        tbody.appendChild(tr);
    });

    // Table Filter and Search
    const searchInput = document.getElementById("cbomSearchInput");
    const riskFilter = document.getElementById("cbomRiskFilter");

    function applyFilter() {
        const query = searchInput ? searchInput.value.toLowerCase() : "";
        const risk = riskFilter ? riskFilter.value : "ALL";

        const rows = tbody.querySelectorAll("tr");
        rows.forEach(r => {
            const text = r.textContent.toLowerCase();
            const matchesQuery = text.includes(query);
            let matchesRisk = true;
            if (risk === "BROKEN") matchesRisk = text.includes("shor broken");
            if (risk === "WEAKENED") matchesRisk = text.includes("grover weakened");
            r.style.display = matchesQuery && matchesRisk ? "" : "none";
        });
    }

    if (searchInput) searchInput.oninput = applyFilter;
    if (riskFilter) riskFilter.onchange = applyFilter;
}

/* ========================================================================== */
/* 5. Code Diff & Developer Ticket Modal Dialog                              */
/* ========================================================================== */
window.openDiffModal = async function(findingId) {
    const modal = document.getElementById("diffModal");
    if (!modal) return;

    try {
        const res = await fetch(`/api/migration/diff/${findingId}`);
        const data = await res.json();

        const f = data.finding;
        document.getElementById("modalFindingTitle").textContent = `Remediation Diff: ${f.id} (${f.algorithm})`;
        document.getElementById("modalFindingMeta").textContent = `${f.file_path}:${f.line_number} • Target Phase ${f.phase}`;
        document.getElementById("modalRecommendationText").textContent = f.recommended_replacement;

        // Render syntax styled diff
        const preDiff = document.getElementById("modalDiffPre");
        if (preDiff) {
            const lines = data.diff.split("\n");
            preDiff.innerHTML = lines.map(line => {
                if (line.startsWith("+") && !line.startsWith("+++")) {
                    return `<span class="diff-add">${escapeHtml(line)}</span>`;
                } else if (line.startsWith("-") && !line.startsWith("---")) {
                    return `<span class="diff-del">${escapeHtml(line)}</span>`;
                }
                return `<span>${escapeHtml(line)}</span>`;
            }).join("");
        }

        // Render Ticket
        const preTicket = document.getElementById("modalTicketPre");
        if (preTicket) {
            preTicket.textContent = data.ticket;
        }

        modal.style.display = "flex";
    } catch (err) {
        alert("Failed to load diff: " + err.message);
    }
};

window.closeDiffModal = function() {
    const modal = document.getElementById("diffModal");
    if (modal) modal.style.display = "none";
};

window.copyTicketMarkdown = function() {
    const preTicket = document.getElementById("modalTicketPre");
    if (preTicket) {
        navigator.clipboard.writeText(preTicket.textContent).then(() => {
            const btn = document.getElementById("copyTicketBtn");
            if (btn) btn.textContent = "✓ Copied to Clipboard!";
            setTimeout(() => {
                if (btn) btn.textContent = "📋 Copy Ticket Markdown";
            }, 2000);
        });
    }
};

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* ========================================================================== */
/* 6. Step 02: Mosca Inequality Simulator & Grover Matrix                     */
/* ========================================================================== */
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

        if (vX) vX.textContent = `${X.toFixed(1)} yrs`;
        if (vY) vY.textContent = `${Y.toFixed(1)} yrs`;
        if (vZ) vZ.textContent = `${Z.toFixed(1)} yrs`;

        const resp = await fetch("/api/risk/mosca", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ shelf_life_years: X, migration_time_years: Y, q_day_years: Z })
        });
        const data = await resp.json();

        const badge = document.getElementById("moscaExposureBadge");
        const horizonText = document.getElementById("moscaHorizonText");
        const verdictText = document.getElementById("moscaVerdictText");
        const timelineRisk = document.getElementById("timelineRiskFill");
        const qdayMarker = document.getElementById("timelineQDayMarker");
        const riskLabel = document.getElementById("timelineRiskEndLabel");

        if (badge) {
            badge.textContent = data.exposure_level;
            badge.className = data.is_at_risk ? "badge-broken glow-red" : "badge-safe glow-green";
        }
        if (horizonText) {
            horizonText.textContent = `Horizon: X (${X.toFixed(1)}y) + Y (${Y.toFixed(1)}y) = ${data.total_risk_horizon}y vs Q-Day (${Z.toFixed(1)}y)`;
            horizonText.style.color = data.is_at_risk ? "var(--status-danger)" : "var(--status-safe)";
        }
        if (verdictText) verdictText.textContent = data.verdict;

        // Update Timeline Visualizer (Scale 0 to 25 years)
        if (timelineRisk) {
            const riskPct = Math.min((data.total_risk_horizon / 25) * 100, 100);
            timelineRisk.style.width = `${riskPct}%`;
        }
        if (qdayMarker) {
            const qPct = Math.min((Z / 25) * 100, 100);
            qdayMarker.style.left = `${qPct}%`;
        }
        if (riskLabel) {
            riskLabel.textContent = `Exposure Horizon: ${data.total_risk_horizon} yrs`;
        }
    }

    if (sX) sX.oninput = updateMosca;
    if (sY) sY.oninput = updateMosca;
    if (sZ) sZ.oninput = updateMosca;
    updateMosca();
}

/* ========================================================================== */
/* 7. Step 03: The Full Quantum Threat Suite (Visual Magnanimity)            */
/* ========================================================================== */
let circuitStage = 1;
let circuitPlayInterval = null;

function initQuantumSuite() {
    // 3A: Shor Simulator
    const runBtn = document.getElementById("runShorBtn");
    const selectN = document.getElementById("shorModulusSelect");

    if (runBtn) {
        runBtn.addEventListener("click", async () => {
            const N = parseInt(selectN.value, 10);
            runBtn.disabled = true;
            runBtn.textContent = "Simulating IQFT...";

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
                runBtn.textContent = "Run Period-Finding";
            }
        });
    }

    // Initialize Circuit Visualizer Stage 1
    renderCircuitStage(1);

    // Initialize Phase Wheel & Density Grid
    renderPhaseWheel(4);
    renderDensityGrid([0, 64, 128, 192]);

    // Initial Telemetry Load
    loadQubitTelemetry(2048);

    // Auto-run Shor for N=143
    setTimeout(() => {
        if (runBtn) runBtn.click();
    }, 400);
}

window.switchQuantumSub = function(subId) {
    document.querySelectorAll(".quantum-subpane").forEach(p => p.style.display = "none");
    const target = document.getElementById(`qsub-${subId}`);
    if (target) target.style.display = "block";

    const pills = document.querySelectorAll("#pane-step-3 .subnav-pill");
    pills.forEach(p => p.classList.remove("active"));
    event.target.classList.add("active");
};

function renderShorResults(data) {
    const outBox = document.getElementById("shorOutputText");
    const svgWrap = document.getElementById("shorSvgWrap");

    const sim = data.simulation;
    const fact = data.factor_result;

    if (outBox) {
        outBox.innerHTML = `
<strong>Target Modulus N:</strong> ${sim.N} | <strong>Base a:</strong> ${sim.base_a}
<strong>Order r:</strong> ${sim.true_order_r} | <strong>Register Size Q:</strong> ${sim.register_size_Q} states (${sim.true_order_r}-fold constructive symmetry)
<strong>Interference Peak Spacing (Q/r):</strong> ${sim.peak_spacing}
<strong>Measured State Peaks:</strong> [${sim.peak_indices.join(", ")}]
<strong>Factored Result:</strong> ${fact.factor_1} × ${fact.factor_2} = ${sim.N} (${fact.method})
        `;
    }

    // Render SVG Probability Peaks with Vibrant Cyberpunk Gradients
    if (svgWrap && sim.sampled_peaks) {
        const svgW = 560;
        const svgH = 180;
        const maxState = sim.register_size_Q;

        let bars = sim.sampled_peaks.map((p, idx) => {
            const x = (p.state / maxState) * (svgW - 80) + 40;
            const barH = p.prob * 480;
            const y = svgH - 30 - barH;
            const color = idx % 2 === 0 ? "#00F0FF" : "#A855F7";
            return `
                <line x1="${x}" y1="${svgH - 30}" x2="${x}" y2="${y}" stroke="${color}" stroke-width="5" stroke-linecap="round" filter="drop-shadow(0 0 6px ${color})"/>
                <circle cx="${x}" cy="${y}" r="5" fill="${color}" filter="drop-shadow(0 0 8px ${color})"/>
                <text x="${x}" y="${svgH - 12}" font-size="11" fill="var(--text-secondary)" text-anchor="middle" font-family="monospace" font-weight="bold">${p.state}</text>
            `;
        }).join("");

        svgWrap.innerHTML = `
            <svg width="100%" height="${svgH}" viewBox="0 0 ${svgW} ${svgH}" style="background: var(--bg-base); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <line x1="30" y1="${svgH - 30}" x2="${svgW - 20}" y2="${svgH - 30}" stroke="var(--border-strong)" stroke-width="1.5"/>
                ${bars}
                <text x="15" y="${svgH / 2}" font-size="11" fill="var(--text-muted)" transform="rotate(-90 15,${svgH/2})" text-anchor="middle">|ψ|²</text>
            </svg>
        `;
    }
}

// 3B: Multi-Qubit Circuit Visualizer with Animated Photon Beads
window.stepCircuitStage = function(delta) {
    circuitStage = Math.max(1, Math.min(4, circuitStage + delta));
    renderCircuitStage(circuitStage);
};

window.toggleCircuitPlay = function() {
    if (circuitPlayInterval) {
        clearInterval(circuitPlayInterval);
        circuitPlayInterval = null;
    } else {
        circuitPlayInterval = setInterval(() => {
            circuitStage = (circuitStage % 4) + 1;
            renderCircuitStage(circuitStage);
        }, 1600);
    }
};

function renderCircuitStage(stage) {
    const svgWrap = document.getElementById("circuitSvgWrap");
    const expBox = document.getElementById("circuitStageExplanation");

    const explanations = [
        "Stage 1: Initialization & Superposition: Counting qubits pass through Hadamard gates H^⊗n to form an equal superposition across all 2^n states.",
        "Stage 2: Modular Exponentiation Oracle: Quantum oracle applies controlled unitary transformation U_a |x⟩|y⟩ = |x⟩|y ⊕ (a^x mod N)⟩.",
        "Stage 3: Inverse Quantum Fourier Transform (IQFT): Applies controlled-phase rotations R_k to translate periodic phase offsets into constructive interference peaks.",
        "Stage 4: Measurement & Factor Extraction: Wavefunction collapses into period multiple s = j · (Q/r). Continued fraction expansion extracts r."
    ];

    if (expBox) expBox.innerHTML = `<strong>${explanations[stage - 1]}</strong>`;

    if (svgWrap) {
        const svgW = 740;
        const svgH = 160;
        
        // Highlight active gate with high-voltage neon glow
        const hGlow = stage === 1 ? 'stroke="#00F0FF" stroke-width="3" fill="rgba(0, 240, 255, 0.2)" filter="drop-shadow(0 0 10px #00F0FF)"' : 'stroke="var(--border-strong)" fill="var(--bg-surface-elevated)"';
        const uGlow = stage === 2 ? 'stroke="#A855F7" stroke-width="3" fill="rgba(168, 85, 247, 0.2)" filter="drop-shadow(0 0 10px #A855F7)"' : 'stroke="var(--border-strong)" fill="var(--bg-surface-elevated)"';
        const iqftGlow = stage === 3 ? 'stroke="#38BDF8" stroke-width="3" fill="rgba(56, 189, 248, 0.2)" filter="drop-shadow(0 0 10px #38BDF8)"' : 'stroke="var(--border-strong)" fill="var(--bg-surface-elevated)"';
        const mGlow = stage === 4 ? 'stroke="#10B981" stroke-width="3" fill="rgba(16, 185, 129, 0.2)" filter="drop-shadow(0 0 10px #10B981)"' : 'stroke="var(--border-strong)" fill="var(--bg-surface-elevated)"';

        svgWrap.innerHTML = `
            <svg width="100%" height="${svgH}" viewBox="0 0 ${svgW} ${svgH}" style="background: var(--bg-base); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <!-- Qubit Wires with Neon Glow -->
                <line x1="50" y1="40" x2="690" y2="40" stroke="#33415C" stroke-width="2"/>
                <line x1="50" y1="75" x2="690" y2="75" stroke="#33415C" stroke-width="2"/>
                <line x1="50" y1="120" x2="690" y2="120" stroke="#33415C" stroke-width="2"/>

                <!-- Qubit Labels -->
                <text x="20" y="44" fill="#00F0FF" font-size="12" font-family="monospace" font-weight="bold">|q₀⟩</text>
                <text x="20" y="79" fill="#00F0FF" font-size="12" font-family="monospace" font-weight="bold">|q₁⟩</text>
                <text x="20" y="124" fill="#A855F7" font-size="12" font-family="monospace" font-weight="bold">|y⟩</text>

                <!-- Stage 1: Hadamard Gates -->
                <rect x="90" y="24" width="36" height="32" rx="5" ${hGlow}/>
                <text x="108" y="45" fill="#F8FAFC" font-size="13" font-weight="bold" text-anchor="middle">H</text>
                <rect x="90" y="59" width="36" height="32" rx="5" ${hGlow}/>
                <text x="108" y="80" fill="#F8FAFC" font-size="13" font-weight="bold" text-anchor="middle">H</text>

                <!-- Stage 2: Modular Exponentiation Oracle -->
                <rect x="200" y="18" width="135" height="118" rx="8" ${uGlow}/>
                <text x="267" y="75" fill="#F8FAFC" font-size="13" font-weight="bold" text-anchor="middle">U_a (mod N)</text>

                <!-- Stage 3: IQFT Box -->
                <rect x="390" y="20" width="125" height="75" rx="8" ${iqftGlow}/>
                <text x="452" y="62" fill="#F8FAFC" font-size="13" font-weight="bold" text-anchor="middle">IQFT †</text>

                <!-- Stage 4: Measurement Detectors -->
                <rect x="570" y="24" width="42" height="32" rx="5" ${mGlow}/>
                <text x="591" y="45" fill="#F8FAFC" font-size="14" text-anchor="middle">∡</text>
                <rect x="570" y="59" width="42" height="32" rx="5" ${mGlow}/>
                <text x="591" y="80" fill="#F8FAFC" font-size="14" text-anchor="middle">∡</text>

                <text x="640" y="62" fill="#10B981" font-size="13" font-family="monospace" font-weight="bold">➔ r</text>
            </svg>
        `;
    }
}

// 3C: Factorization Race
window.startFactorizationRace = function() {
    const keySelect = document.getElementById("raceKeySelect");
    const bits = parseInt(keySelect.value, 10);

    const cBar = document.getElementById("classicalRaceBar");
    const qBar = document.getElementById("quantumRaceBar");
    const cTime = document.getElementById("classicalTimeEst");
    const qTime = document.getElementById("quantumTimeEst");
    const cStatus = document.getElementById("classicalStatusText");
    const qStatus = document.getElementById("quantumStatusText");

    cBar.style.width = "0%";
    qBar.style.width = "0%";

    if (bits === 32) {
        cTime.textContent = "Estimated Time: 0.05 ms";
        qTime.textContent = "Estimated Time: 0.01 ms";
        animateRace(cBar, 100, 400);
        animateRace(qBar, 100, 200);
    } else if (bits === 64) {
        cTime.textContent = "Estimated Time: 12.4 seconds";
        qTime.textContent = "Estimated Time: 0.2 seconds";
        animateRace(cBar, 80, 800);
        animateRace(qBar, 100, 300);
    } else if (bits === 512) {
        cTime.textContent = "Estimated Time: 8.4 CPU-Months";
        qTime.textContent = "Estimated Time: 14 Minutes";
        animateRace(cBar, 25, 1000);
        animateRace(qBar, 100, 400);
    } else if (bits === 1024) {
        cTime.textContent = "Estimated Time: 5,000 CPU-Years";
        qTime.textContent = "Estimated Time: 1.2 Hours";
        animateRace(cBar, 8, 1200);
        animateRace(qBar, 100, 500);
    } else { // 2048
        cTime.textContent = "Estimated Time: 300,000,000 CPU-Years";
        qTime.textContent = "Estimated Time: 8.2 Hours";
        animateRace(cBar, 1.5, 1500);
        animateRace(qBar, 100, 600);
    }
};

function animateRace(bar, targetWidth, duration) {
    let start = null;
    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        bar.style.width = `${progress * targetWidth}%`;
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}

// 3D: Hardware Telemetry
window.loadQubitTelemetry = async function(bits) {
    try {
        const res = await fetch(`/api/quantum/resources/${bits}`);
        const data = await res.json();
        document.getElementById("telLogicalQubits").textContent = data.logical_qubits.toLocaleString();
        document.getElementById("telQubits2019").textContent = data.physical_noisy_qubits_gidney2019.toLocaleString();
        document.getElementById("telQubits2025").textContent = data.physical_noisy_qubits_gidney2025.toLocaleString();
        document.getElementById("telRuntime").textContent = data.estimated_runtime;
        document.getElementById("telToffoli").textContent = data.toffoli_gate_depth.toExponential(2);
        document.getElementById("telCodeDistance").textContent = `d = ${data.surface_code_distance}`;
    } catch (e) {
        console.error("Telemetry error", e);
    }
};

// 3E: Phase Wheel & Density Grid
function renderPhaseWheel(orderR) {
    const wrap = document.getElementById("phaseWheelSvgWrap");
    if (!wrap) return;
    const size = 180;
    const r = 65;
    const cx = size / 2;
    const cy = size / 2;

    let vectors = "";
    for (let k = 0; k < orderR; k++) {
        const theta = (2 * Math.PI * k) / orderR;
        const x = cx + r * Math.cos(theta);
        const y = cy + r * Math.sin(theta);
        vectors += `
            <line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#A855F7" stroke-width="2.5" filter="drop-shadow(0 0 6px #A855F7)"/>
            <circle cx="${x}" cy="${y}" r="4.5" fill="#00F0FF" filter="drop-shadow(0 0 6px #00F0FF)"/>
        `;
    }

    wrap.innerHTML = `
        <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
            <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="var(--border-subtle)" stroke-width="2" stroke-dasharray="4"/>
            <line x1="10" y1="${cy}" x2="${size-10}" y2="${cy}" stroke="var(--border-strong)" stroke-width="1"/>
            <line x1="${cx}" y1="10" x2="${cx}" y2="${size-10}" stroke="var(--border-strong)" stroke-width="1"/>
            ${vectors}
        </svg>
    `;
}

function renderDensityGrid(peaks) {
    const wrap = document.getElementById("densityGridWrap");
    if (!wrap) return;
    wrap.innerHTML = "";
    for (let i = 0; i < 256; i++) {
        const cell = document.createElement("div");
        cell.className = "density-cell";
        if (peaks.includes(i)) {
            cell.classList.add("peak");
        }
        wrap.appendChild(cell);
    }
}

/* ========================================================================== */
/* 8. Step 04: The Full PQC Active Defense Suite                             */
/* ========================================================================== */
let wireSegmentsData = [];

function initPQCDiffenseSuite() {
    loadHandshakeSegments();
    initAttackPlayground();
    startCryptoLogStream();
    startAmbientPacketDrift();
}

window.switchPqcSub = function(subId) {
    document.querySelectorAll(".pqc-subpane").forEach(p => p.style.display = "none");
    const target = document.getElementById(`pqcsub-${subId}`);
    if (target) target.style.display = "block";

    const pills = document.querySelectorAll("#pane-step-4 .subnav-pill");
    pills.forEach(p => p.classList.remove("active"));
    event.target.classList.add("active");
};

async function loadHandshakeSegments() {
    try {
        const res = await fetch("/api/pqc/handshake");
        const data = await res.json();
        wireSegmentsData = data.wire_segments || [];
        if (wireSegmentsData.length > 0) {
            inspectWireSegment(0);
        }
    } catch (e) {
        console.error("Handshake segments error", e);
    }
}

window.inspectWireSegment = function(index) {
    if (!wireSegmentsData[index]) return;
    const seg = wireSegmentsData[index];
    document.getElementById("wireSegName").textContent = seg.name;
    document.getElementById("wireSegMeta").textContent = `${seg.standard} • ${seg.bytes} Bytes`;
    document.getElementById("wireSegDesc").textContent = seg.description;
    document.getElementById("wireSegHex").textContent = seg.hex_sample;
};

// Ambient Packet Gliding on Wire
function startAmbientPacketDrift() {
    const packet = document.getElementById("topoPacket");
    if (!packet) return;
    let forward = true;
    setInterval(() => {
        if (!packet.classList.contains("attacking")) {
            packet.style.left = forward ? "75%" : "25%";
            forward = !forward;
        }
    }, 2800);
}

// 4B: Attack Playground & MITM Harness with Laser and Shield Animations
function initAttackPlayground() {
    const tamperBtn = document.getElementById("pqcTamperBtn");
    const replayBtn = document.getElementById("pqcReplayBtn");
    const mitmBtn = document.getElementById("pqcMitmBtn");
    const packet = document.getElementById("topoPacket");
    const laser = document.getElementById("mitmLaser");
    const shield = document.getElementById("serverShieldRipple");

    if (tamperBtn) {
        tamperBtn.addEventListener("click", async () => {
            if (packet) {
                packet.classList.add("attacking");
                packet.style.left = "48%";
                packet.textContent = "💥";
            }
            if (laser) {
                laser.classList.add("firing");
                setTimeout(() => laser.classList.remove("firing"), 500);
            }

            const res = await fetch("/api/pqc/attack/tamper", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: "TAMPER PAYLOAD" })
            });
            const data = await res.json();

            setTimeout(() => {
                if (packet) packet.style.left = "78%";
                if (shield) {
                    shield.classList.add("active");
                    setTimeout(() => shield.classList.remove("active"), 800);
                }
            }, 350);

            setTimeout(() => {
                if (packet) {
                    packet.classList.remove("attacking");
                    packet.textContent = "📦";
                    packet.style.left = "20%";
                }
            }, 1200);

            showMitmBanner("danger", `🚨 [BIT-FLIP TAMPER INTERCEPTED] ${data.error}`, data.action);
        });
    }

    if (replayBtn) {
        replayBtn.addEventListener("click", async () => {
            if (packet) {
                packet.classList.add("attacking");
                packet.textContent = "🔄";
                packet.style.left = "78%";
            }

            const res = await fetch("/api/pqc/attack/replay", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: "REPLAY TRANSACTION" })
            });
            const data = await res.json();

            setTimeout(() => {
                if (packet) {
                    packet.classList.remove("attacking");
                    packet.textContent = "📦";
                    packet.style.left = "20%";
                }
            }, 1000);

            showMitmBanner("warn", `🛑 [REPLAY ATTACK DISCARDED] ${data.error}`, data.action);
        });
    }

    if (mitmBtn) {
        mitmBtn.addEventListener("click", async () => {
            if (packet) {
                packet.classList.add("attacking");
                packet.textContent = "🔓";
                packet.style.left = "48%";
            }

            const res = await fetch("/api/pqc/attack/mitm", { method: "POST" });
            const data = await res.json();

            setTimeout(() => {
                if (packet) {
                    packet.classList.remove("attacking");
                    packet.textContent = "📦";
                    packet.style.left = "20%";
                }
            }, 1000);

            showMitmBanner("danger", `🔒 [LATTICE SIGNATURE FORGERY BLOCKED] ${data.error}`, data.action);
        });
    }

    // 4G: Live Chat
    const sendBtn = document.getElementById("pqcSendBtn");
    const msgInput = document.getElementById("pqcMsgInput");
    if (sendBtn) {
        sendBtn.addEventListener("click", async () => {
            const msg = (msgInput ? msgInput.value.trim() : "") || "TRANSFER $50,000 TO ACCOUNT #49281";
            appendPqcChat("user", msg);
            if (msgInput) msgInput.value = "";

            const res = await fetch("/api/pqc/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            appendPqcChat("agent", `🛡️ [ML-KEM/AES-256-GCM Decrypted] Server: "${data.verified_decrypted}" (Ciphertext: ${data.ciphertext_hex})`);
        });
    }
}

function showMitmBanner(type, title, desc) {
    const banner = document.getElementById("mitmStatusBanner");
    const bTitle = document.getElementById("mitmStatusTitle");
    const bDesc = document.getElementById("mitmStatusDesc");
    if (!banner) return;
    banner.style.display = "block";
    banner.className = `mitm-status-banner ${type}`;
    if (bTitle) bTitle.textContent = title;
    if (bDesc) bDesc.textContent = desc;
}

function appendPqcChat(role, text) {
    const stream = document.getElementById("pqcChatStream");
    if (!stream) return;
    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.textContent = text;
    stream.appendChild(div);
    stream.scrollTop = stream.scrollHeight;
}

// 4D: Cryptographic Monospace Terminal Stream
function startCryptoLogStream() {
    const term = document.getElementById("cryptoLogStream");
    if (!term) return;

    const logs = [
        "[INIT] Initializing OpenSSL 3.5.9 PQC engine with FIPS 203/204 support",
        "[KEM_KEYGEN] Generated 32-byte entropy seed from kernel CSPRNG",
        "[LATTICE_OP] Sampling polynomial matrix A in R_q^(3x3) over q=3329",
        "[ML-KEM-768] Public key vector synthesized (1,184 Bytes wire footprint)",
        "[TLS_HANDSHAKE] Emitting ClientHello with hybrid group x25519_mlkem768",
        "[SERVER_RECV] Received ClientHello: extracting ML-KEM encapsulation key",
        "[FO_TRANSFORM] Applying Fujisaki-Okamoto rejection sampling transform",
        "[ENCAPSULATE] Computed ciphertext vector (u, v): 1,088 Bytes",
        "[SIG_GEN] Generating ML-DSA-65 lattice signature (3,309 Bytes wire footprint)",
        "[KDF] Deriving 256-bit session key via HKDF-SHA256(SS_classical || SS_mlkem)",
        "[SECURE_TUNNEL] Established authenticated AES-256-GCM symmetric session",
        "[REPLAY_GUARD] Sliding-window anti-replay filter active (Window size: 1024 packets)"
    ];

    let i = 0;
    function addLog() {
        if (i < logs.length) {
            const p = document.createElement("div");
            const time = new Date().toISOString().substring(11, 19);
            p.innerHTML = `<span style="color: #64748B;">[${time}]</span> <span style="color: #00F0FF; font-weight: bold;">${logs[i]}</span>`;
            term.appendChild(p);
            term.scrollTop = term.scrollHeight;
            i++;
            setTimeout(addLog, 480);
        }
    }
    setTimeout(addLog, 700);
}

/* ========================================================================== */
/* 9. Step 05: Migration Roadmap & Grounded AI Copilot                       */
/* ========================================================================== */
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
            card.style.marginBottom = "14px";
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <h4 style="font-size: 0.96rem; font-weight: 700;">Phase ${p.phase}: ${p.title}</h4>
                    <span class="badge-safe glow-green">Target: ${p.target_readiness}/100</span>
                </div>
                <p style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 8px;">${p.description}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 0.74rem; font-family: var(--font-mono); color: #EAB308;">
                        Impacted: ${p.findings.map(f => f.id).join(", ") || "None"}
                    </div>
                    ${p.findings.length > 0 ? `<button class="btn-secondary" style="font-size: 0.72rem; padding: 3px 8px;" onclick="openDiffModal('${p.findings[0].id}')">View First Diff</button>` : ""}
                </div>
            `;
            listEl.appendChild(card);
        });
    } catch (e) {
        console.error("Roadmap error", e);
    }
}

function initCopilot() {
    const sendBtn = document.getElementById("copilotSendBtn");
    const input = document.getElementById("copilotInput");

    async function sendPrompt(query) {
        if (!query.trim()) return;
        appendCopilot("user", query);
        input.value = "";

        // Temporary thinking typing bubble
        const stream = document.getElementById("copilotStream");
        const thinkingBubble = document.createElement("div");
        thinkingBubble.className = "chat-msg agent";
        thinkingBubble.id = "copilotThinkingMsg";
        thinkingBubble.innerHTML = `<em>⚡ Verifying finding IDs in active CBOM database...</em>`;
        if (stream) stream.appendChild(thinkingBubble);

        try {
            const res = await fetch("/api/copilot/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            });
            const data = await res.json();
            const tb = document.getElementById("copilotThinkingMsg");
            if (tb) tb.remove();
            appendCopilot("agent", data.answer);
        } catch (e) {
            const tb = document.getElementById("copilotThinkingMsg");
            if (tb) tb.remove();
            appendCopilot("agent", `Copilot error: ${e.message}`);
        }
    }

    if (sendBtn) sendBtn.addEventListener("click", () => sendPrompt(input.value));
    if (input) {
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") sendPrompt(input.value);
        });
    }

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
