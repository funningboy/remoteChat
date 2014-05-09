(function() {
  var canvas, ctx, onError, onSuccess, update, video, ws, target;

  onError = function(e) {
    return console.log("Rejected", e);
  };

  onSuccess = function(localMediaStream) {
    video.src = webkitURL.createObjectURL(localMediaStream);
    return setInterval(update, 250);
  };

  update = function() {
   ctx.drawImage(video, 0, 0, 320, 240);
   return canvas.toBlob(function(blob) {
      return ws.send(blob);
    }, 'image/jpeg');
  };


  video = document.querySelector('video');

  canvas = document.querySelector('canvas');

  ctx = canvas.getContext('2d');

  ctx.strokeStyle = '#ff0';

  ctx.lineWidth = 2;

  if ("WebSocket" in window) {
    ws = new WebSocket("ws://" + location.host + "/webhandler");
    ws.onopen = function() {
      return console.log("Opened websocket");
    };

    ws.onmessage = function(e) {
      $("#cam").attr('src', 'data:image/jpg;base64,' + e.data);
      //
      //target = document.getElementById('target');
      //url=window.webkitURL.createObjectURL(e.data);
      //target.onload = function() {
      //  window.webkitURL.revokeObjectURL(url);
      //};
      //target.src = url;
    };
  }

  navigator.getMedia = (
      navigator.getUserMedia        ||
      navigator.webkitGetUserMedia  ||
      navigator.mozGetUserMedia     ||
      navigator.msGetUserMedia);

  navigator.getMedia({
    'video': true,
    'audio': false
  }, onSuccess, onError);

}).call(this);
