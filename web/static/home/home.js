/* home.js
Simple Home Automation Server
jQuery Mobile Frontend

Thomas Koch, 2014-2020
*/


function toggleAlarm(flag) {
    // call http request to toggle alarm
    $.ajax({
           type: "POST",
           url: "/alarm/"+encodeURIComponent(flag),
           data: {},
           dataType: "json",
           success: function(data) {
              $("#statusupdate").html("<span class='updateMessage'>" + data.time +"</span>");
           }
       });
};


function toggleSwitch(swt, turn) {
    // call http request to toggle switch
    $.ajax({
           type: "POST",
           url: "/turn/"+encodeURIComponent(swt),
           data: {'cmd': encodeURIComponent(turn)
           },
           dataType: "json",
           success: function(data) {
              $("#switchupdate").html("<span class='updateMessage'>" + data.time +"</span>");
           }
       });
};

function updateStatus() {
    //  simple http request to fetch status data
    $.getJSON("/status", function(data , textStatus) {
              if (data.motion) {
                $("#lastmotion").html(data.motion);
              }
              if (data.temperature) {
                  $("#temperature").html(data.temperature);
              }
              if (data.webcam) {
                  $("#webcam").prop('src', data.webcam);
              }
              if (data.time) {
                  $("#statusupdate").html("<span class='updateMessage'>" + data.time +"</span>");
              }
    });
};

function initAlarmSwitch() {
    //  connect flip button handler
    $('select#switchAlarm').change(function() {
        var val = $('select#switchAlarm').val();
        toggleAlarm(val);
    });
};

function initSwitches() {
    //  connect flip button handler
    $('select#switchA').change(function() {
        var val = $('select#switchA').val();
        toggleSwitch('A', val);
    });
    $('select#switchB').change(function() {
        var val = $('select#switchB').val();
        toggleSwitch('B', val);
    });
    $('select#switchC').change(function() {
        var val = $('select#switchC').val();
        toggleSwitch('C', val);
    });
};

$(document).on('pageinit', '#switches', function() {
    // alert('Pageinit: Switch');
    initSwitches();
});

$(document).on('pageinit', '#motion', function(){
    // alert('Pageinit: Motion');
    initAlarmSwitch();
    $("#refresh").click(function(e){
        e.preventDefault();
        updateStatus();
    });
});

$(document).on('pagebeforeshow', '#motion', function(){
    // alert('pagebeforeshow: Kontrolle');
    updateStatus() ;
});
