fetch('/api/db-systems')
    .then(r => r.json())
    .then(data => {
        const tbody = document.querySelector('#dbTable tbody');
        tbody.innerHTML = '';
        (Array.isArray(data) ? data : []).forEach((db, i) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i+1}</td>
                <td>${db.db_name||''}</td>
                <td>${db.status||''}</td>
                <td>${db.crash_recovery||''}</td>
                <td>${db.delete_protected||''}</td>
                <td>${db.heatwave_cluster||''}</td>
                <td>${db.created||''}</td>
                <td>${db.compartment_id||''}</td>
                <td>${db.id||''}</td>
            `;
            tbody.appendChild(row);
        });
        if (!data.length) tbody.innerHTML = '<tr><td colspan="9">No data</td></tr>';
    })
    .catch(() => {
        document.querySelector('#dbTable tbody').innerHTML = '<tr><td colspan="9">Error loading data</td></tr>';
    }); 