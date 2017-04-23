$(document).ready(() => {
    $('#file-selector').change(() => {
        uploadFiles()
    })
    $('#add-song-button').click(() => {
        $('#file-selector').trigger('click')
    })
    refreshSongs()
})

function uploadFiles() {
    var formData = new FormData()
    for(var file of $('#file-selector')[0].files) {
        formData.append(file.name, file)
    }
    $.ajax({
        url: '/upload/',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: refreshSongs
    })
}

function upvote(id) {
    $.ajax({
        url: '/upvote/' + id,
        type: 'POST',
        success: refreshSongs
    })
}

function downvote(id) {
    $.ajax({
        url: '/downvote/' + id,
        type: 'POST',
        success: refreshSongs
    })
}

function refreshSongs() {
    $.ajax({
        url: '/songs/',
        type: 'GET',
        success: (data) => {
            songs = JSON.parse(data)
            for(var song of songs) {
                console.log(song)
            }
        }
    })
}