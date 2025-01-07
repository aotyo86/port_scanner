$(document).ready(function() {
    $('#scan-form').submit(function(e) {
        e.preventDefault(); // フォームのデフォルト動作を防止

        const formData = {
            ip: $('#ip').val(),
            start_port: parseInt($('#start_port').val(), 10),
            end_port: parseInt($('#end_port').val(), 10),
        };

        // デバッグ用ログ
        console.log("Form Data:", formData);

        // 値が正しく取得できているか確認
        if (!formData.ip || isNaN(formData.start_port) || isNaN(formData.end_port)) {
            alert('Please provide valid input values.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/scan',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                const tableBody = $('#results-table tbody');
                tableBody.empty(); // 既存の結果をクリア

                response.open_ports.forEach(portInfo => {
                    tableBody.append(`
                        <tr>
                            <td>${portInfo.port}</td>
                            <td style="color: green;">Open</td>
                            <td>${portInfo.service || 'Unknown'}</td>
                        </tr>
                    `);
                });
            },
            error: function(xhr) {
                $('#result').html('Error: ' + (xhr.responseJSON?.error || 'An error occurred'));
            },
        });
    });
});
