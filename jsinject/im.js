const ATT_COUNT = 200;
const MEDIA_TYPES = "photo";
const SIZE_TYPES = ["w", "z", "y", "x", "m", "s"];

function make_code(peer_id, from_id) {
    return `
        var Ret = {
            count: 0,
            next_from: null,
            attachments: []
        };
        
        var request = {
            peer_id: ${peer_id},
            start_from: "${from_id}",
            count: ${ATT_COUNT},
            media_type: "${MEDIA_TYPES}"
        };
        var att_returned = API.messages.getHistoryAttachments(request);
            
        var photos = att_returned.items@.attachment@.photo;
        var i = 0;
        while (i < photos.length) {
            Ret.attachments.push({
                "id": photos[i].id,
                "date": photos[i].date,
                "urls": photos[i].sizes
            });
            i = i + 1;
        }
    
        Ret.count = Ret.attachments.length;
        Ret.next_from = att_returned.next_from;
        
        return Ret;
    `;
}

new QWebChannel(qt.webChannelTransport, function(channel) {
    const on_next_series = function() {
        const args = JSON.parse(arguments[0]);
        if (args.debug) {
            channel.objects.app_receiver.log("Arguments object", arguments[0]);
        }

        var textarea_code = document.getElementById("dev_const_code");
        textarea_code.value = make_code(args.peer_id, args.from_id);

        var run_button = document.getElementById("dev_req_run_btn");
        try {
            run_button.click();
        }
        catch (e) {}

        setTimeout(function() {
            var dev_result = document.getElementById("dev_result");
            channel.objects.app_receiver.on_dev_result(dev_result.innerHTML);
        }, 1000);
    };
    const on_finish = function() {
        channel.objects.app_receiver.get_next_series.disconnect(on_next_series);
        channel.objects.app_receiver.on_finish.disconnect(on_finish);
    };
    channel.objects.app_receiver.get_next_series.connect(on_next_series);
    channel.objects.app_receiver.on_finish.connect(on_finish);
    const textarea_code = document.getElementById("dev_const_code");
    if (textarea_code)
        channel.objects.app_receiver.init("Injection ready: `im`");
});
