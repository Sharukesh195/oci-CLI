fetch('/api/db-systems')
    .then(r => r.json())
    .then(data => {
        const tbody = document.querySelector('#dbTable tbody');
        tbody.innerHTML = '';
        (Array.isArray(data) ? data : []).forEach((db, i) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i+1}</td>
                <td>${db.db_name||db.name||''}</td>
                <td>${db.status||''}</td>
                <td>${db.hostname||''}</td>
                <td>${db.compartment_id||''}</td>
                <td>${db.id||''}</td>
            `;
            tbody.appendChild(row);
        });
        if (!data.length) tbody.innerHTML = '<tr><td colspan="6">No data</td></tr>';
    })
    .catch(() => {
        document.querySelector('#dbTable tbody').innerHTML = '<tr><td colspan="6">Error loading data</td></tr>';
    });
