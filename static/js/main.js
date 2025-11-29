let selectedQuality = 'best';
let currentDownloadId = '';

document.querySelectorAll('.quality-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.quality-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedQuality = this.dataset.quality;
    });
});

async function fetchVideoInfo() {
    const url = document.getElementById('videoUrl').value;
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }

    try {
        const response = await fetch('/api/video-info', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url})
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('thumbnail').src = data.info.thumbnail;
            document.getElementById('title').textContent = data.info.title;
            document.getElementById('uploader').textContent = data.info.uploader;
            document.getElementById('duration').textContent = data.info.duration;
            document.getElementById('views').textContent = data.info.view_count.toLocaleString();
            document.getElementById('videoInfo').classList.add('show');
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to fetch video info');
    }
}

async function startDownload() {
    const url = document.getElementById('videoUrl').value;
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }

    currentDownloadId = Date.now().toString();

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                url: url,
                quality: selectedQuality,
                download_id: currentDownloadId
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('progressContainer').classList.add('show');
            checkProgress(currentDownloadId);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to start download');
    }
}

function showError(message) {
    const alert = document.getElementById('errorAlert');
    alert.textContent = message;
    alert.classList.add('show');
}