function show_modal_top(clicked_id) {
  var idNum = clicked_id.substring(14);
  var modal = document.getElementById('modal-item-top-' + idNum);
  modal.style.display = "block";
}

function hide_modal_top(clicked_id) {
  var idNum = clicked_id.substring(10);
  var modal = document.getElementById('modal-item-top-' + idNum);
  modal.style.display = "none";
}

function show_modal_search(clicked_id) {
  var idNum = clicked_id.substring(17);
  var modal = document.getElementById('modal-item-search-' + idNum);
  modal.style.display = "block";
}

function hide_modal_search(clicked_id) {
  var idNum = clicked_id.substring(13);
  var modal = document.getElementById('modal-item-search-' + idNum);
  modal.style.display = "none";
}

function show_modal_sub(clicked_id) {
  var idNum = clicked_id.substring(14);
  var modal = document.getElementById('modal-item-sub-' + idNum);
  modal.style.display = "block";
}

function hide_modal_sub(clicked_id) {
  var idNum = clicked_id.substring(10);
  var modal = document.getElementById('modal-item-sub-' + idNum);
  modal.style.display = "none";
}

function show_modal_browse(clicked_id) {
  var idNum = clicked_id.substring(17);
  var modal = document.getElementById('modal-item-browse-' + idNum);
  modal.style.display = "block";
}

function hide_modal_browse(clicked_id) {
  var idNum = clicked_id.substring(13);
  var modal = document.getElementById('modal-item-browse-' + idNum);
  modal.style.display = "none";
}
