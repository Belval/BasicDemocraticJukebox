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
        url: '/upvote/' + id + '/',
        type: 'POST',
        success: refreshSongs
    })
}

function downvote(id) {
    $.ajax({
        url: '/downvote/' + id + '/',
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
            $("#song-table-list").html('')
            for(var song of songs) {
                addSongElement(song)
            }
        }
    })
}

function addSongElement(song) {
    const id = song.id
    const upvote = song.upvote
    const downvote = song.downvote
    const title = song.title
    const SongItem = (song) => `
        <tr id="song-display-element">
            <td class="col-xs-4">
                <div class="btn btn-success" onclick="upvote(${id})"><span class="glyphicon glyphicon-arrow-up"></span><span class="badge song-upvote">${upvote}</span></div>
                <div class="btn btn-danger" onclick="downvote(${id})"><span class="glyphicon glyphicon-arrow-down"></span><span class="badge song-downvote">${downvote}</span></div>
            </td>
            <td class="col-xs-8 song-title">${title}</td>
        </tr>
    `
    $('#song-table-list').append(SongItem)
}