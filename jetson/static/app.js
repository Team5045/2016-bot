( function ( io, $ ) {
    var socket = io.connect(undefined, {
        reconnectionDelayMax: 1000
    });

    // VIDEO STREAM
    var streamEl = document.getElementById('stream')
    var canvas = streamEl.getElementsByTagName('canvas')[0];
    canvas.width = CAMERA_WIDTH;
    canvas.height = CAMERA_HEIGHT;
    var stream = {
        startTime: new Date().getTime(),
        frameCt: 0,
        fps: streamEl.getElementsByClassName('fps')[0],
        context: canvas.getContext('2d')
    };

    // ROBOT STATS
    var robotStats = {
        connected_to_jetson: false,
        connected_to_robot: false
    };

    var robotEditables = {
        // 'editable--chooser--autonomous_command/options': ['thing1', 'thing2'],
        // 'editable--chooser--autonomous_command/default': 'thing1',
        // 'editable--chooser--autonomous_command/selected': 'thing2'
    };

    socket.on('close disconnect', function() {
        robotStats.connected_to_jetson = false;
        updateRobotStats();
    });
    socket.on('reconnect', function() {
        socket.emit('request_driver_vision');
        socket.emit('request_network_tables');
    });

    // VIDEO STREAM
    var latestData = null;
    socket.on('driver_vision', function ( data ) {
        // Each time we receive some data, request some more!
        // socket.emit('request_driver_vision');
        latestData = data;
        stream.frameCt++;
    } );
    function updateImage() {
        if (!latestData) {
            return;
        }

        var img = new Image();
        img.src = latestData.raw;

        if (img) {
            stream.context.drawImage(img, 0, 0);
        }
    }
    setInterval(updateImage, 33);

    /// FRAMES PER SECOND
    function updateFps () {
        // Update fps (loop)
        var d = new Date().getTime(),
            currentTime = (d - stream.startTime) / 1000,
            result = Math.floor(stream.frameCt / currentTime);

        if (currentTime > 1) {
            stream.startTime = new Date().getTime();
            stream.frameCt = 0;
        }

        stream.fps.innerText = result;
    }
    setInterval(updateFps, 500);

    // NETWORK TABLES

    socket.on('network_tables_update', function (data) {
        data.connected_to_jetson = true;

        Object.assign(robotStats, _.pickBy(data, function(value, key) {
            return !_.startsWith(key, 'editable--');
        }));

        Object.assign(robotEditables, _.pickBy(data, function(value, key) {
            return _.startsWith(key, 'editable--');
        }));

        updateRobotStats();
        updateRobotEditables();
    });

    function updateRobotStats() {
        var $stats = $('#robotStatsInner');
        Object.keys(robotStats).forEach(function (key) {
            var $existing = $stats.find('#stats_' + key);
            if ($existing.length) {
                $existing.find('span').text(robotStats[key]);
            } else {
                $stats.append(
                    $('<div>', { id: 'stats_' + key })
                    .append($('<b>').text(key))
                    .append(': ')
                    .append($('<span>').text(robotStats[key]))
                );
            }
        });

        if (!robotStats.connected_to_jetson || !robotStats.connected_to_robot) {
            $(document.body).addClass('disconnected');
        } else {
            $(document.body).removeClass('disconnected');
        }
    }

    // stop editables update from propagating while the driver
    // is interacting with the dropdown menu. 
    var isInteractingWithEditable = false;
    $('#robotEditablesInner input, #robotEditablesInner select')
        .on('mousedown focus', function () { isInteractingWithEditable = true; })
        .on('blur', function () { isInteractingWithEditable = false; });

    function updateRobotEditables() {
        var $editables = $('#robotEditablesInner').empty(),
            alreadyHandled = {};

        if (isInteractingWithEditable) {
            setTimeout(updateRobotEditables, 500);
        }

        _.forIn(robotEditables, function (value, key) {
            var keyParams = key.split('--'),
                type = keyParams[1], name = keyParams[2].split('/')[0];

            if (alreadyHandled[name]) {
                return;
            } else {
                alreadyHandled[name] = true;
            }

            if (type === 'chooser') {
                var keyPrefix = keyParams.slice(0, 2).join('--') + '--' + name,
                    options = robotEditables[keyPrefix + '/options'],
                    defaultValue = robotEditables[keyPrefix + '/default'],
                    selectedValue = robotEditables[keyPrefix + '/selected'] || defaultValue;

                var $options = options.map(function (o) {
                    return $('<option>')
                        .prop('selected', o === selectedValue)
                        .text(o)
                        .prop('value', o)
                });

                $('<div>', { id: 'editables_' + name })
                    .append($('<b>').text(name))
                    .append(': ')
                    .append(
                        $('<select>')
                            .append($options)
                            .change(function () {
                                $(this).prop('disabled', true);
                                socket.emit('edit_network_tables', {
                                    key: keyPrefix + '/selected',
                                    value: $(this).val(),
                                    type: 'string'
                                });
                            })
                    )
                    .appendTo($editables);
            }
        });
    }

    // Request initial updates
    socket.emit('request_driver_vision');
    socket.emit('request_network_tables');

    // LOL
    $('#yeeButton').click(function () {
        var yee = $('#yee').fadeIn().get(0);
        yee.currentTime = 0;
        yee.play();

        setTimeout(function () {
            $('#yee').fadeOut();
            $(document).off('keydown click', prematureyeeEndYee);
        }, 7500);

        function prematureyeeEndYee () {
            $('#yee').hide();
            yee.pause();
        }
        $(document).one('keydown click', prematureyeeEndYee)

        return false;
    });

}( io, jQuery ) );
