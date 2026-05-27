// IP Address Tracker

let currentIPInfo = null;
let map = null;
let marker = null;

// Sahifani yuklash
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    initMap();
    loadHistory();
    
    // Default: O'z IP-ni olish
    const clientIP = document.getElementById('ipInput').value;
    if (clientIP) {
        searchIP(clientIP);
    }
});

// Event listeners
function setupEventListeners() {
    document.getElementById('ipInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchIP();
        }
    });
}

// Xaritani initsializatsiya qilish
function initMap() {
    map = L.map('map').setView([20, 0], 2);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

// IP addressni qidirish
function searchIP(ip = null) {
    const ipInput = document.getElementById('ipInput');
    const searchIP = ip || ipInput.value.trim();
    
    if (!searchIP) {
        showStatus('❌ IP address kiritishni unutmang!', 'error');
        return;
    }
    
    showStatus('⏳ Qidirilmoqda...', 'loading');
    
    fetch('/api/lookup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ip: searchIP
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayIPInfo(data.data);
            showStatus('✅ ' + data.message, 'success');
            loadHistory();
        } else {
            showStatus('❌ ' + data.error, 'error');
            hideResults();
        }
    })
    .catch(error => {
        showStatus('❌ Bog\'lanish xatosi!', 'error');
        console.error('Error:', error);
    });
}

// O'z IP-ni olish
function getMyIP() {
    showStatus('⏳ O\'z IP-m aniqlanmoqda...', 'loading');
    
    fetch('/api/my-ip')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('ipInput').value = data.data.ip;
                displayIPInfo(data.data);
                showStatus('✅ O\'z IP-m topildi!', 'success');
                loadHistory();
            } else {
                showStatus('❌ ' + data.error, 'error');
            }
        })
        .catch(error => {
            showStatus('❌ Xatolik!', 'error');
            console.error('Error:', error);
        });
}

// IP ma'lumotlarini ko'rsatish
function displayIPInfo(data) {
    currentIPInfo = data;
    
    // Info cards
    document.getElementById('infoIP').textContent = data.ip;
    document.getElementById('infoLocation').textContent = `${data.city}, ${data.region}`;
    document.getElementById('infoCountry').textContent = data.country;
    document.getElementById('infoTimezone').textContent = data.timezone;
    document.getElementById('infoISP').textContent = data.isp;
    document.getElementById('infoASN').textContent = data.asn;
    
    // Grid ko'rsatish
    document.getElementById('infoGrid').style.display = 'grid';
    
    // Detalliy ma'lumotlar
    displayDetailedInfo(data);
    
    // Xarita yangilash
    updateMap(data);
    
    // Map card ko'rsatish
    document.getElementById('mapCard').style.display = 'block';
}

// Detalliy ma'lumotlarni ko'rsatish
function displayDetailedInfo(data) {
    const detailsGrid = document.getElementById('detailsGrid');
    detailsGrid.innerHTML = '';
    
    const details = [
        { label: '🔐 IP Type', value: data.is_private ? 'Private' : 'Public' },
        { label: '🌍 Country Code', value: data.country_code },
        { label: '📮 Postal Code', value: data.postal_code || 'N/A' },
        { label: '📍 Latitude', value: data.latitude || 'N/A' },
        { label: '📍 Longitude', value: data.longitude || 'N/A' },
        { label: '🌐 Network', value: data.network || 'N/A' },
        { label: '💱 Currency', value: data.currency || 'N/A' },
        { label: '📞 Calling Code', value: data.calling_code || 'N/A' },
        { label: '🗣️ Languages', value: data.languages || 'N/A' },
        { label: '🛡️ VPN?', value: data.is_vpn ? '✓ Yes' : '✗ No' },
        { label: '🛡️ Proxy?', value: data.is_proxy ? '✓ Yes' : '✗ No' },
        { label: '🛡️ Datacenter?', value: data.is_datacenter ? '✓ Yes' : '✗ No' },
    ];
    
    details.forEach(detail => {
        const detailItem = document.createElement('div');
        detailItem.className = 'detail-item';
        detailItem.innerHTML = `
            <div class="detail-label">${detail.label}</div>
            <div class="detail-value">${escapeHtml(String(detail.value))}</div>
        `;
        detailsGrid.appendChild(detailItem);
    });
    
    document.getElementById('detailsCard').style.display = 'block';
}

// Xaritani yangilash
function updateMap(data) {
    if (!data.latitude || !data.longitude) {
        console.warn('Latitude/Longitude ma\'lumotlari yo\'q');
        return;
    }
    
    const lat = parseFloat(data.latitude);
    const lng = parseFloat(data.longitude);
    
    // Eski marker-ni o'chirish
    if (marker) {
        map.removeLayer(marker);
    }
    
    // Yangi marker qo'shish
    marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(`<strong>${data.city}, ${data.country}</strong><br>${data.ip}`)
        .openPopup();
    
    // Xaritani center qilish
    map.setView([lat, lng], 10);
}

// Status ko'rsatish
function showStatus(message, type) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = message;
    statusEl.className = 'status ' + type;
    
    if (type === 'success') {
        setTimeout(() => {
            statusEl.textContent = '';
            statusEl.className = 'status';
        }, 3000);
    }
}

// Natijalarni yashirish
function hideResults() {
    document.getElementById('infoGrid').style.display = 'none';
    document.getElementById('mapCard').style.display = 'none';
    document.getElementById('detailsCard').style.display = 'none';
}

// Tarixni yuklash
function loadHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.count > 0) {
                const historyCard = document.getElementById('historyCard');
                const historyList = document.getElementById('historyList');
                
                historyList.innerHTML = '';
                
                data.history.forEach(item => {
                    const historyItem = document.createElement('div');
                    historyItem.className = 'history-item';
                    historyItem.innerHTML = `
                        <div class="history-ip">${item.ip}</div>
                        <div class="history-location">📍 ${item.city}, ${item.country} | 🕐 ${item.timestamp}</div>
                    `;
                    historyItem.onclick = () => searchIP(item.ip);
                    historyList.appendChild(historyItem);
                });
                
                historyCard.style.display = 'block';
            }
        })
        .catch(error => console.error('Error:', error));
}

// HTML-ni escape qilish
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
