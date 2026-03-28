const API_BASE = "http://127.0.0.1:5000/api";

// --- UI Logic ---
document.querySelectorAll('.nav-links li').forEach(link => {
    link.addEventListener('click', (e) => {
        // Update active class
        document.querySelector('.nav-links .active').classList.remove('active');
        e.target.classList.add('active');

        // Switch page
        document.querySelector('.page.active').classList.remove('active');
        const targetId = e.target.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');

        // Refresh Data
        refreshData();
    });
});

function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${isError ? 'error' : ''}`;
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

async function apiFetch(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' },
            ...(body && { body: JSON.stringify(body) })
        };
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        return await res.json();
    } catch (err) {
        showToast("API Connection Error", true);
        console.error(err);
    }
}

// --- Data Refreshing ---
async function refreshData() {
    loadDataCenters();
    loadWorkloads();
    loadWater();
    loadAnalytics();
}

async function loadDataCenters() {
    const res = await apiFetch('/datacenters');
    const tbody = document.querySelector('#table-dcs tbody');
    const selectWl = document.querySelector('#wl-dc-id');
    const selectWater = document.querySelector('#w-dc-id');
    
    tbody.innerHTML = '';
    selectWl.innerHTML = '<option value="">Select Data Center</option>';
    selectWater.innerHTML = '<option value="">Select Data Center</option>';

    if (res?.success) {
        document.getElementById('kpi-dcs').innerText = res.data.length;
        res.data.forEach(dc => {
            // Table
            tbody.innerHTML += `
                <tr>
                    <td>${dc.data_center_id}</td>
                    <td><b>${dc.name}</b></td>
                    <td>${dc.location}</td>
                    <td><button class="btn-danger" onclick="deleteDC(${dc.data_center_id})">Delete</button></td>
                </tr>
            `;
            // Selects
            const opt = `<option value="${dc.data_center_id}">${dc.name}</option>`;
            selectWl.innerHTML += opt;
            selectWater.innerHTML += opt;
        });
    }
}

async function loadWorkloads() {
    const res = await apiFetch('/workloads');
    const tbody = document.querySelector('#table-wls tbody');
    const selectWater = document.querySelector('#w-wl-id');
    
    tbody.innerHTML = '';
    selectWater.innerHTML = '<option value="">Select Workload</option>';

    if (res?.success) {
        document.getElementById('kpi-workloads').innerText = res.data.length;
        res.data.forEach(wl => {
            tbody.innerHTML += `
                <tr>
                    <td>${wl.workload_id}</td>
                    <td><b>${wl.name}</b></td>
                    <td><span style="color:var(--accent)">${wl.type}</span></td>
                    <td>${wl.datacenter || 'Unassigned'}</td>
                    <td><button class="btn-danger" onclick="deleteWorkload(${wl.workload_id})">Delete</button></td>
                </tr>
            `;
            selectWater.innerHTML += `<option value="${wl.workload_id}">${wl.name}</option>`;
        });
    }
}

async function loadWater() {
    const res = await apiFetch('/water');
    const tbody = document.querySelector('#table-water tbody');
    tbody.innerHTML = '';
    
    if (res?.success) {
        res.data.forEach(w => {
            tbody.innerHTML += `
                <tr>
                    <td>${w.water_id}</td>
                    <td><b>${w.water_used_liters} L</b></td>
                    <td>${w.date}</td>
                    <td>${w.datacenter}</td>
                    <td>${w.workload}</td>
                    <td><button class="btn-danger" onclick="deleteWater(${w.water_id})">Delete</button></td>
                </tr>
            `;
        });
    }
}

async function loadAnalytics() {
    // Water per DC
    const resDc = await apiFetch('/reports/water_per_dc');
    const listDc = document.getElementById('rep-water-dc');
    listDc.innerHTML = '';
    if(resDc?.success) {
        resDc.data.forEach(r => {
            listDc.innerHTML += `<li><span>${r.datacenter}</span> <b>${r.total_water || 0} L</b></li>`;
        });
    }

    // Water per WL
    const resWl = await apiFetch('/reports/water_per_wl');
    const listWl = document.getElementById('rep-water-wl');
    listWl.innerHTML = '';
    if(resWl?.success) {
        resWl.data.forEach(r => {
            listWl.innerHTML += `<li><span>${r.workload}</span> <b style="color:var(--accent)">${r.total_water || 0} L</b></li>`;
        });
    }

    // Cooling
    const resCool = await apiFetch('/reports/top_cooling');
    const listCool = document.getElementById('rep-cooling');
    listCool.innerHTML = '';
    if(resCool?.success) {
        resCool.data.forEach(r => {
            listCool.innerHTML += `<li><span>${r.cooling_system} (${r.datacenter})</span> <b>${r.efficiency}%</b></li>`;
        });
    }
}

// --- Form Submissions ---
document.getElementById('form-dc').addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await apiFetch('/datacenters', 'POST', {
        name: document.getElementById('dc-name').value,
        location: document.getElementById('dc-loc').value
    });
    if (res.success) { showToast("Data Center Added!"); e.target.reset(); refreshData(); }
    else showToast(res.error, true);
});

document.getElementById('form-wl').addEventListener('submit', async (e) => {
    e.preventDefault();
    const dc_id = document.getElementById('wl-dc-id').value;
    const res = await apiFetch('/workloads', 'POST', {
        name: document.getElementById('wl-name').value,
        type: document.getElementById('wl-type').value,
        data_center_id: dc_id ? parseInt(dc_id) : null
    });
    if (res.success) { showToast("Workload Added!"); e.target.reset(); refreshData(); }
    else showToast(res.error, true);
});

document.getElementById('form-water').addEventListener('submit', async (e) => {
    e.preventDefault();
    const dc_id = document.getElementById('w-dc-id').value;
    const wl_id = document.getElementById('w-wl-id').value;
    const res = await apiFetch('/water', 'POST', {
        water_used_liters: parseFloat(document.getElementById('w-liters').value),
        date: document.getElementById('w-date').value,
        data_center_id: dc_id ? parseInt(dc_id) : null,
        workload_id: wl_id ? parseInt(wl_id) : null
    });
    if (res.success) { showToast("Water consumption logged!"); e.target.reset(); refreshData(); }
    else showToast(res.error, true);
});

// --- Delete Actions ---
window.deleteDC = async (id) => {
    if(confirm("Delete Data Center?")) {
        const res = await apiFetch(`/datacenters/${id}`, 'DELETE');
        if(res.success) { showToast("Deleted"); refreshData(); }
        else showToast(res.error, true);
    }
};

window.deleteWorkload = async (id) => {
    if(confirm("Delete Workload?")) {
        const res = await apiFetch(`/workloads/${id}`, 'DELETE');
        if(res.success) { showToast("Deleted"); refreshData(); }
        else showToast(res.error, true);
    }
};

window.deleteWater = async (id) => {
    if(confirm("Delete Record?")) {
        const res = await apiFetch(`/water/${id}`, 'DELETE');
        if(res.success) { showToast("Deleted"); refreshData(); }
        else showToast(res.error, true);
    }
};

// Start
document.addEventListener('DOMContentLoaded', refreshData);
