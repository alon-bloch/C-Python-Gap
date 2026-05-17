let currentData = [];
let sortSteps = [];
let currentStepIdx = 0;

const busContainer = document.getElementById('bus-container');
const btnLoadDefault = document.getElementById('btn-load-default');
const btnStartSort = document.getElementById('btn-start-sort');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const stepCounter = document.getElementById('step-counter');
const statusMsg = document.getElementById('status-msg');

const ptrI = document.getElementById('ptr-i');
const ptrJ = document.getElementById('ptr-j');
const ptrNext = document.getElementById('ptr-next');

// Initial Load
window.onload = () => loadDefaultData();

async function loadDefaultData() {
    const response = await fetch('/api/default_data');
    currentData = await response.json();
    renderBuses(currentData);
    resetControls();
}

// New Bus Form Elements
const inName = document.getElementById('in-name');
const inDistance = document.getElementById('in-distance');
const inDuration = document.getElementById('in-duration');
const inFrequency = document.getElementById('in-frequency');
const btnAddBus = document.getElementById('btn-add-bus');

const MAX_BUSES = 50;

btnAddBus.onclick = () => {
    if (currentData.length >= MAX_BUSES) {
        return alert(`Maximum limit reached (${MAX_BUSES} lines). Please sort or reset.`);
    }
    
    const name = inName.value.trim();
    const dist = parseInt(inDistance.value);
    const dur = parseInt(inDuration.value);
    const freq = parseInt(inFrequency.value);

    // Basic Validation (Matching project constraints)
    if (!name || name.length > 20) return alert("Name must be 1-20 chars");
    if (isNaN(dist) || dist < 0 || dist > 1000) return alert("Distance 0-1000");
    if (isNaN(dur) || dur < 10 || dur > 100) return alert("Duration 10-100");
    if (isNaN(freq) || freq < 1 || freq > 50) return alert("Frequency 1-50");

    currentData.push({ name, distance: dist, duration: dur, frequency: freq });
    renderBuses(currentData);
    resetControls();
    
    // Clear inputs
    [inName, inDistance, inDuration, inFrequency].forEach(i => i.value = '');
};

function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function renderBuses(data, activeIdxs = [], isSwap = false) {
    // If not swapping, we can just redraw
    if (!isSwap) {
        busContainer.innerHTML = '';
        data.forEach((bus, index) => {
            const card = document.createElement('div');
            card.className = 'bus-card';
            card.setAttribute('data-id', index);
            if (activeIdxs.includes(index)) card.classList.add('active');
            
            card.innerHTML = `
                <div class="bus-name">Line ${escapeHTML(bus.name)}</div>
                <div class="bus-stats">
                    <span>Dist: ${bus.distance}m</span>
                    <span>Dur: ${bus.duration}m</span>
                    <span>Freq: ${bus.frequency}x</span>
                </div>
            `;
            busContainer.appendChild(card);
        });
    }
}

async function performSwapAnimation(idxA, idxB, newState) {
    const cards = busContainer.querySelectorAll('.bus-card');
    const cardA = cards[idxA];
    const cardB = cards[idxB];
    
    cardA.classList.add('swapping');
    cardB.classList.add('swapping');
    
    const offset = cardB.offsetTop - cardA.offsetTop;
    
    cardA.style.transform = `translateY(${offset}px)`;
    cardB.style.transform = `translateY(${-offset}px)`;
    
    return new Promise(resolve => {
        setTimeout(() => {
            cardA.style.transform = '';
            cardB.style.transform = '';
            cardA.classList.remove('swapping');
            cardB.classList.remove('swapping');
            renderBuses(newState); // Finalize DOM order
            resolve();
        }, 400);
    });
}

const sortCriteria = document.getElementById('sort-criteria');
const currentCriteriaLabel = document.getElementById('current-criteria-label');
const algoTypeContainer = document.getElementById('algo-type-container');

// Metrics elements
const mComps = document.getElementById('metric-comps');
const mSwaps = document.getElementById('metric-swaps');
const mTime = document.getElementById('metric-time');

sortCriteria.onchange = () => {
    const criteria = sortCriteria.value;
    btnStartSort.innerText = criteria === 'name' ? "Start Bubble Sort" : "Start Quick Sort";
    algoTypeContainer.style.display = criteria === 'name' ? "flex" : "none";
    resetControls();
};

// Reset metrics when switching between Standard and Aborted
document.querySelectorAll('input[name="algo-type"]').forEach(radio => {
    radio.onchange = () => {
        resetControls();
    };
});

let currentAlgo = "";

btnStartSort.onclick = async () => {
    const criteria = sortCriteria.value;
    const algoType = document.querySelector('input[name="algo-type"]:checked').value;
    currentCriteriaLabel.innerText = criteria.charAt(0).toUpperCase() + criteria.slice(1);
    
    const response = await fetch('/api/sort_steps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            data: currentData,
            criteria: criteria,
            algo_type: algoType
        })
    });
    const result = await response.json();
    sortSteps = result.steps;
    currentAlgo = result.algo;
    
    // Update Metrics
    mComps.innerText = result.metrics.comparisons;
    mSwaps.innerText = result.metrics.swaps;
    mTime.innerText = result.metrics.time + "ms";
    
    currentStepIdx = 0;
    lastViewedIdx = -1;
    updateStepView();
    btnPrev.disabled = false;
    btnNext.disabled = false;
    btnStartSort.disabled = true;
};

async function updateStepView() {
    const step = sortSteps[currentStepIdx];
    if (!step) return;

    const prevStep = currentStepIdx > 0 ? sortSteps[currentStepIdx - 1] : null;
    
    // If the action is a swap, and we are moving forward, animate it
    if (step.swap && (!prevStep || currentStepIdx > lastViewedIdx)) {
        let idxA, idxB;
        if (currentAlgo === "Bubble Sort") {
            idxA = step.cur; idxB = step.next;
        } else {
            idxA = step.small; idxB = step.current;
        }
        await performSwapAnimation(idxA, idxB, step.array);
    } else {
        let activeIdxs = [];
        if (currentAlgo === "Bubble Sort") {
            activeIdxs = [step.cur, step.next];
        } else {
            activeIdxs = [step.small, step.current, step.pivot];
        }
        renderBuses(step.array, activeIdxs, step.swap);
    }
    
    lastViewedIdx = currentStepIdx;

    const baseAddr = 0x1000;
    const structSize = 0x40;
    
    const labels = document.querySelectorAll('.label');
    // Labels 0, 1, 2 are for Metrics. Labels 3, 4, 5 are for Pointers.
    
    if (currentAlgo.includes("Bubble Sort")) {
        ptrI.innerText = `0x${(baseAddr + (step.current_pass * structSize)).toString(16).toUpperCase()}`;
        ptrJ.innerText = `0x${(baseAddr + (step.cur * structSize)).toString(16).toUpperCase()}`;
        ptrNext.innerText = `0x${(baseAddr + (step.next * structSize)).toString(16).toUpperCase()}`;
        labels[3].innerText = "current (i):";
        labels[4].innerText = "cur (j):";
        labels[5].innerText = "cur + 1:";
    } else {
        ptrI.innerText = `0x${(baseAddr + (step.pivot * structSize)).toString(16).toUpperCase()}`;
        ptrJ.innerText = `0x${(baseAddr + (step.small * structSize)).toString(16).toUpperCase()}`;
        ptrNext.innerText = `0x${(baseAddr + (step.current * structSize)).toString(16).toUpperCase()}`;
        labels[3].innerText = "pivot:";
        labels[4].innerText = "small:";
        labels[5].innerText = "current:";
    }
    
    stepCounter.innerText = `${currentAlgo} | Step: ${currentStepIdx + 1} / ${sortSteps.length}`;
    statusMsg.innerText = step.swap ? "Swapping elements!" : "Comparing elements...";
    if (step.action === "pivot_placed") statusMsg.innerText = "Pivot placed in final position!";
}

let lastViewedIdx = -1;

const btnPlay = document.getElementById('btn-play');
let isPlaying = false;
let playInterval = null;

btnPlay.onclick = () => {
    if (isPlaying) {
        stopAutoPlay();
    } else {
        startAutoPlay();
    }
};

function startAutoPlay() {
    if (currentStepIdx >= sortSteps.length - 1) return;
    isPlaying = true;
    btnPlay.innerText = "Stop";
    btnPlay.classList.add('active');
    
    playInterval = setInterval(async () => {
        if (currentStepIdx < sortSteps.length - 1) {
            currentStepIdx++;
            await updateStepView();
        } else {
            stopAutoPlay();
            statusMsg.innerText = "Sorting Complete!";
        }
    }, 600); // 600ms per step (allows 400ms for swap animation + 200ms pause)
}

function stopAutoPlay() {
    isPlaying = false;
    btnPlay.innerText = "Auto Play";
    btnPlay.classList.remove('active');
    clearInterval(playInterval);
}

btnNext.onclick = async () => {
    if (currentStepIdx < sortSteps.length - 1) {
        currentStepIdx++;
        await updateStepView();
    } else {
        statusMsg.innerText = "Sorting Complete!";
        btnNext.disabled = true;
    }
};

btnPrev.onclick = () => {
    if (currentStepIdx > 0) {
        currentStepIdx--;
        updateStepView();
        btnNext.disabled = false;
    }
};

function resetControls() {
    stopAutoPlay();
    sortSteps = [];
    currentStepIdx = 0;
    lastViewedIdx = -1;
    btnPrev.disabled = true;
    btnNext.disabled = true;
    btnStartSort.disabled = false;
    stepCounter.innerText = 'Step: 0 / 0';
    statusMsg.innerText = 'Ready to sort...';
    ptrI.innerText = '0x----';
    ptrJ.innerText = '0x----';
    ptrNext.innerText = '0x----';
    
    // Clear Metrics
    mComps.innerText = '-';
    mSwaps.innerText = '-';
    mTime.innerText = '-';
}

const btnClearAll = document.getElementById('btn-clear-all');

btnClearAll.onclick = () => {
    currentData = [];
    renderBuses(currentData);
    resetControls();
};

btnLoadDefault.onclick = loadDefaultData;
