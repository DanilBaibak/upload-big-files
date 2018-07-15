$(function () {
    var $progress = $('#progress'),
        $fileUpload = $('#fileupload'),
        $finished = $('#finished'),
        $finishedSize = $finished.find('span'),
        $progressSize = $progress.find('span');

    var sendSize = 0,
        maxChunkSize = 10000000, // 10 MB
        oneMb = 1000000;


    $progress.hide()
    $finished.hide()

    $fileUpload.fileupload({
        maxChunkSize: maxChunkSize,
        dataType: 'json',
        maxRetries: 10,
        retryTimeout: 500,
        done: function (e, data) {
            if (data.result.status === 'failed') {
                window.location.href = '/'
            }
            $progress.hide()
            $fileUpload.prop('disabled', false);

            $finishedSize.text(parseFloat(data.total / oneMb).toFixed(2))
            $finished.show()

            sendSize = 0;
        }
    })
    .on('fileuploadstart', function (e) {
        $progressSize.text(sendSize)
        $finished.hide()
        $progress.show()
        $fileUpload.prop('disabled', true);
    })
    .on('fileuploadchunkdone', function (e, data) {
        sendSize += maxChunkSize / oneMb
        $progressSize.text(sendSize)
    })
});