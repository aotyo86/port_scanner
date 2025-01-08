$(document).ready(function() {
    // ページロード時に過去にスキャンしたIPアドレスを取得
    $.get('/scan_history', function(data) {
        console.log("Rceived data from /scan_history:",data);

        const ipHistory = $('#ip-history');
        ipHistory.empty(); // 以前の候補を削除

        if (data.history && Array.isArray(data.history)) {
            data.history.forEach(ip => {
                ipHistory.append(`<option value="${ip}">`);
            });
        } else {
            console.error("Invalid or missing history data:", data);
        }
    });

    $('#scan-form').submit(function (e) {
        e.preventDefault();

        const formData = {
            ip: $('#ip').val(),
            start_port: parseInt($('#start_port').val(), 10),
            end_port: parseInt($('#end_port').val(), 10),
        };

        $.ajax({
            type: 'POST',
            url: '/scan',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (response) {
                console.log("Received response from /scan:",response)
                
                const historyContainer = $('#history');
                historyContainer.empty();
                
                if (response.history && Array.isArray(response.history)) {
                    response.history.forEach(ip => {
                        historyContainer.append(`<li>${ip}</li>`);
                    });
                } else {
                    console.error("Invalid or missing history data:", response.history);
                }

                const tableBody = $('#results-table tbody');
                tableBody.empty(); // Clear previous results

                if (response.open_ports && Array.isArray(response.open_ports)) {
                    response.open_ports.forEach(portInfo => {
                        tableBody.append(`
                            <tr>
                                <td>${portInfo.port}</td>
                                <td style="color: green;">Open</td>
                                <td>${portInfo.service || 'Unknown'}</td>
                            </tr>
                        `);
                    });
                } else {
                    console.error("Invalid or missing open_ports data:", response.open_ports);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error occurred:", error);
                console.error("Response text:", xhr.responseText);
                alert('An error occurred while scanning ports.');
            },
        });
    });
});
