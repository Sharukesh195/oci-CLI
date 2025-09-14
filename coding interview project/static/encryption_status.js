fetch('/api/db-systems/encryption-status')
    .then(r => r.json())
    .then(data => {
        const tbody = document.querySelector('#encryptionTable tbody');
        tbody.innerHTML = '';
        (Array.isArray(data) ? data : []).forEach((db, i) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i+1}</td>
                <td>${db.display_name||db.db_name||db.name||''}</td>
                <td>${db.connection_encryption_status||db.encryption_status||'Oracle-managed key'}</td>
                <td>${db.compartment_id||''}</td>
                <td>${db.id||''}</td>
            `;
            tbody.appendChild(row);
        });
        if (!data.length) tbody.innerHTML = '<tr><td colspan="5">No data</td></tr>';
    })
    .catch(() => {
        document.querySelector('#encryptionTable tbody').innerHTML = '<tr><td colspan="5">Error loading data</td></tr>';
    });