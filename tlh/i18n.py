"""Every word the page shows, in both languages it speaks.

Vietnamese is the default and the original: this is a tool for one Vietnamese
streamer's VODs, and the person using it reads Vietnamese. English is here so
the page can be shown to someone who does not.

The page keeps its Vietnamese inline in the HTML as well as here, so it reads
correctly before the script runs and even if the script never runs. That is a
duplication on purpose; `check()` guards the failure that actually happens,
which is a key translated in one language and not the other.

Not in here: anything the SERVER writes. Job details, progress lines and API
errors are produced by tlh/web.py and run.py and arrive already worded, so in
English mode those lines stay Vietnamese. Translating them means carrying a
language through the API, which is a bigger change than the page needed.
"""

VI = {
    # ---- chrome
    "head.title": "Cắt VOD stream Heroes 3",
    "tab.fn": "Chức năng",
    "tab.trim": "Hỗ trợ cắt ghép",
    "tab.author": "Tác giả",
    "lang.tip": "Đổi ngôn ngữ giao diện",
    "tip.version": "Xem có gì mới trong bản này",

    # ---- shared buttons and tips
    "btn.open": "Mở",
    "btn.clear": "Dọn",
    "btn.clearAll": "Dọn tất cả",
    "btn.copy": "Copy",
    "tip.openFolder": "Mở thư mục này trong Explorer",
    "tip.clearFolder": "Chuyển mọi file trong thư mục này vào Thùng rác",
    "tip.clearWork": "Chuyển file tạm và cache phân tích vào Thùng rác. "
                     "Video trong input và output không bị xoá",
    "tip.clearAll": "Chuyển input + output + work (kèm cache phân tích) vào "
                    "Thùng rác. Giống lựa chọn 6 của Clear.cmd",
    "tip.openWork": "Mở thư mục work trong Explorer",
    "tip.openInput": "Mở thư mục input trong Explorer",

    # ---- 1. what to do
    "h2.step1": "1 · Chọn việc muốn làm",
    "opt.games.t": "Lược bỏ thời gian chờ turn đối thủ, tách nhiều video cho nhiều đối",
    "opt.games.d": "Mỗi game một video, mỗi cái một timeline riêng, tên "
                   "<code>[ngày] Opponent (game 1).mp4</code>. Tách theo game "
                   "chứ không theo tên đối thủ.",
    "opt.full.t": "Lược bỏ thời gian chờ turn đối thủ, gộp 1 video",
    "opt.full.d": "Một video hoàn chỉnh, kèm 1 file timeline .txt để dán vào "
                  "mô tả YouTube. Đây là cái để đăng.",
    "opt.download.t": "Chỉ tải video về, không cắt",
    "opt.download.d": 'Lưu nguyên bản vào <code class="p-in">input\\</code> rồi '
                      "dừng. Để tải sẵn lúc mạng khoẻ, cắt sau — hoặc để giữ "
                      "lại bản gốc.",
    "dev.summary": "Tuỳ chọn cho lập trình viên",
    "opt.parts.t": "Cắt thành nhiều đoạn rời",
    "opt.parts.d": "Mỗi đoạn giữ lại thành một file riêng, không ghép. Để mở "
                   "từng đoạn xem máy cắt có đúng chỗ không.",
    "opt.segments.t": "Chỉ phân tích, không tạo video",
    "opt.segments.d": "Chỉ ra danh sách khoảng sẽ giữ / sẽ bỏ và danh sách "
                      "chương. Nhanh nhất.",
    "paths.video": "Video ra",
    "paths.parts": "Đoạn rời ra",

    # ---- 2. the source
    "h2.step2": "2 · Chọn nguồn",
    "ph.url": "Dán link YouTube: https://www.youtube.com/watch?v=...",
    "btn.chopen": "Chọn từ kênh…",
    "tip.chopen": "Mở danh sách stream của kênh để lấy link",
    # ---- the channel card, and the picker it opens
    #
    # Everything here except the two counters comes out of the ONE flat
    # listing the picker already fetches. The counters are read off this
    # disk and cost no request at all.
    "chan.live": "ĐANG PHÁT",
    "chan.subs": "Người đăng ký",
    "chan.latest": "Stream mới nhất",
    "chan.aired": "Phát lúc",
    "chan.have": "Đã có trên máy",
    "chan.off": "Không phát",
    "chan.haveSub": "trong {n} stream mới nhất, {c} đã cắt",
    "chan.about": "Giới thiệu kênh",
    "chan.loading": "đang lấy thông tin kênh…",
    "chan.failed": "không lấy được thông tin kênh",
    "btn.refresh": "Làm mới",
    "btn.seeAll": "Xem tất cả stream",
    "tip.refreshChan": "Hỏi lại YouTube về kênh này",
    "tip.chpick": "Đổi giữa kênh chính và kênh dự phòng",
    "ch.head": "Stream của kênh",
    "ch.n10": "10 mới nhất",
    "ch.n20": "20 mới nhất",
    "ch.n100": "100 mới nhất",
    "ch.onlyNew": "chỉ hiện chưa tải",
    "ch.loading": "đang lấy danh sách…",
    "ch.failed": "không lấy được",
    "ch.count": "{n} video",
    "ch.empty": "Kênh này chưa có stream nào.",
    "ch.allDone": "Mọi stream trong danh sách đều đã tải về rồi.",
    "ch.live": "ĐANG PHÁT",
    "ch.notdone": "chưa kết thúc, không tải được",
    "ch.views": "view",
    "ch.aired": "phát",
    "ch.dateFail": "không lấy được",
    "btn.reload": "Tải lại",
    "btn.close": "Đóng",
    "btn.useLink": "Dùng link này",
    "btn.copyLink": "Copy link",
    "btn.date": "Ngày phát",
    "btn.openCut": "Mở file đã cắt",
    "have.cut": "ĐÃ CẮT",
    "have.dl": "ĐÃ TẢI",
    "copy.ok": "Đã copy",
    "copy.fail": "Không copy được",
    "btn.start": "Tải & chạy",
    "btn.startDl": "Tải về",
    "sep.orRun": "hoặc chạy một file đã có trong",
    "empty.reading": "đang đọc…",
    "empty.noInput": "Chưa có video nào ở đây.",
    "btn.run": "Chạy",
    "btn.delete": "Xoá",
    "tip.showFile": "Mở thư mục chứa file này, chọn sẵn nó",
    "tip.deleteFile": "Chuyển vào Thùng rác, có thể phục hồi",
    "tip.noRunInDl": "Đang chọn chế độ chỉ tải về, file này thì đã tải rồi",

    # ---- jobs
    "h2.jobs": "Công việc",
    "empty.jobs": "Chưa có việc nào. Dán link ở trên để bắt đầu.",
    "job.stop": "Dừng",
    "job.remove": "Xoá",
    "job.detail": "Chi tiết",
    "job.copyLog": "Copy log",
    "job.openFolder": "Mở thư mục",
    "tip.copyLog": "Copy toàn bộ log + thông tin việc này vào clipboard",
    "tip.openResult": "Mở thư mục chứa kết quả",
    "kv.mode": "Chế độ",
    "kv.downloaded": "Dung lượng tải",
    "kv.streams": "Luồng",
    "kv.downloader": "Downloader",
    "kv.length": "Thời lượng",
    "kv.segments": "Segment",
    "kv.kept": "giữ",
    "kv.chapters": "Chương",
    "kv.source": "File nguồn",
    "kv.output": "Video ra",
    "kv.downloadedFile": "File đã tải",
    "kv.timeline": "Timeline (.txt)",
    "job.started": "Bắt đầu",
    "job.finished": "xong",
    "job.took": "mất",
    "job.stale": "Không có dữ liệu mới",

    # ---- version tab
    "tab.ver": "Phiên bản",
    "h2.ver": "Phiên bản",
    "ver.current": "hiện tại",
    "ver.3.0.d": "<ul>"
                 "<li>Cắt được video ở mọi độ phân giải 16:9 — 720p, 1080p, "
                 "1440p. Video ra giữ nguyên độ phân giải của bản gốc.</li>"
                 "<li>Tải về ở độ phân giải gốc thay vì ép xuống 1080p.</li>"
                 "<li>Giữ nguyên tốc độ khung hình của bản gốc thay vì ép 60 "
                 "— file nhỏ hơn khoảng 13% và render nhanh hơn, hình y "
                 "hệt.</li>"
                 "<li>Video không phải 16:9 bị từ chối thẳng, kèm lý do.</li>"
                 "<li>Không còn đổ lỗi đỏ ra cửa sổ đen khi trình duyệt ngắt "
                 "kết nối.</li></ul>",
    "ver.2.0.d": "<ul>"
                 "<li>Sửa lỗi cắt ngược: đọc nhầm ghế nên giữ lượt đối thủ và "
                 "cắt lượt Tieulinh.</li>"
                 "<li>Không còn sót mẩu lượt đối thủ ở đầu và cuối mỗi "
                 "lượt.</li>"
                 "<li>Thêm <b>Xoá QR code</b>: dò mã QR một lần rồi phủ logo "
                 "kênh lên cả video.</li>"
                 '<li>Hỗ trợ cắt ghép lấy video từ cả <code class="p-in">'
                 "input\\</code> lẫn "
                 '<code class="p-out">output\\</code>.</li>'
                 "<li>Sửa nút <b>Mở thư mục</b> ở mục Công việc: mở sai chỗ và "
                 "nuốt lỗi im lặng.</li>"
                 "</ul>",
    "ver.1.0.d": "<ul>"
                 "<li>Tự cắt bỏ thời gian chờ lượt đối thủ, ghép lại có fade "
                 "đen.</li>"
                 "<li>Tải VOD từ link YouTube.</li>"
                 "<li>Viết timeline chương theo ngày trong game, dán thẳng vào "
                 "mô tả.</li>"
                 "<li>Tách riêng từng ván thành video rời.</li>"
                 "<li>Trang web theo dõi tiến độ, và tab hỗ trợ cắt thử một "
                 "đoạn.</li>"
                 "</ul>",

    # ---- remove QR tab
    "tab.qr": "Xoá QR code",
    "h2.qr": "Xoá QR code khỏi video",
    "qr.intro": "<ul><li>Chọn video trong "
                '<code class="p-in">input\\</code> hoặc '
                '<code class="p-out">output\\</code>, rồi bấm '
                "<b>Xoá QR</b>.</li>"
                "<li>File mới nằm cùng thư mục với bản gốc, tên thêm "
                "<code>[remove-qr]</code> ở đầu.</li>"
                "<li>Bản gốc không bị đụng vào.</li></ul>",
    "btn.removeQr": "Xoá QR",
    "qr.note": "<ul><li>Mã QR đứng yên suốt cả stream, nên nó chỉ được dò "
               "một lần rồi phủ ảnh lên toàn bộ video.</li>"
               "<li>Việc này encode lại cả file nên lâu ngang một lần cắt — "
               "theo dõi ở tab <b>Chức năng</b>, mục <b>Công việc</b>.</li>"
               "<li>Không dò ra thì vẫn phủ vào đúng góc đó với viền rộng "
               "hơn, và báo rõ trong log.</li></ul>",
    "reveal.failed": "không mở được thư mục",
    "qr.askTitle": "Xoá QR code khỏi video này?",
    "qr.askOut": "File mới:",
    "qr.askNote": "Phải encode lại cả file, lâu ngang một lần cắt. "
                  "Bản gốc không bị sửa.",
    "qr.starting": "đang bắt đầu…",
    "qr.started": "đã bắt đầu, xem tiến độ ở mục Công việc",
    "qr.failed": "không xoá được",

    # ---- trim tab
    "h2.trim": "Cắt một đoạn ra file riêng",
    "trim.intro": "<ul><li>Chọn video trong "
                  '<code class="p-in">input\\</code> hoặc '
                  '<code class="p-out">output\\</code>, tua tới chỗ cần '
                  "rồi bấm <b>Đặt tại đây</b>.</li>"
                  "<li>Đoạn cắt ra nằm cùng thư mục với bản gốc, chạy được "
                  "ngay ở tab <b>Chức năng</b> — để thử thuật toán trên 15 "
                  "phút thay vì 4 tiếng.</li></ul>",
    "trim.sameFolder": "File mới nằm cùng thư mục với bản gốc, "
                       "không sửa gì vào bản gốc.",
    "btn.preview": "Xem",
    "tip.preview": "Nạp video này vào khung xem",
    "lbl.start": "Điểm đầu",
    "lbl.end": "Điểm cuối",
    "btn.setHere": "Đặt tại đây",
    "btn.goto": "Tới",
    "btn.cut": "Cắt đoạn này ra",
    "trim.note": "<ul><li>Copy nguyên luồng, không encode lại: 90 phút xong "
                 "trong vài giây, và hình y hệt bản gốc.</li>"
                 "<li>Đổi lại điểm đầu bám vào keyframe gần nhất phía trước, "
                 "nên đoạn ra có thể dài hơn yêu cầu vài giây — cắt nhỏ để "
                 "chạy thử thì không ảnh hưởng gì.</li></ul>",
    "trim.noVideo": "chưa có video nào trong input hay output",
    "trim.pickFirst": "Chưa có video nào để xem.",
    "trim.noSource": "Chưa chọn video.",
    "trim.badMarks": "Mốc thời gian không hợp lệ.",
    "trim.unreadable": "mốc không đọc được",
    "trim.endAfterStart": "điểm cuối phải sau điểm đầu",
    "trim.long": "dài",
    "trim.cutting": "đang cắt…",
    "trim.cutFailed": "không cắt được",
    "trim.done": "Đã cắt:",
    "trim.realLength": "dài thật",
    "trim.keyframeNote": "(dài hơn yêu cầu do bám keyframe)",
    "trim.cantPlay": "Trình duyệt không phát được file này. mp4 và webm thì "
                     "được; mkv, ts, avi thì thường không, nhưng vẫn cắt được "
                     "nếu tự nhập mốc.",
    "ask.cutTitle": "Cắt đoạn này ra thành file mới?",
    "ask.cutNote": "File mới nằm trong thư mục input, không sửa gì vào bản gốc.",

    # ---- channel picker
    "ch.title": "Stream của kênh",
    "ch.newest": "mới nhất",
    "ch.reload": "Tải lại",
    "ch.close": "Đóng",
    "ch.loading": "đang lấy danh sách…",
    "ch.failed": "không lấy được",
    "ch.videos": "video",
    "ch.empty": "Kênh này chưa có stream nào.",
    "ch.live": "ĐANG PHÁT",
    "ch.liveNoDl": "chưa kết thúc, không tải được",
    "ch.use": "Dùng link này",
    "ch.copy": "Copy link",
    "ch.date": "Ngày phát",
    "ch.aired": "phát",
    "ch.views": "view",
    "copied": "Đã copy",
    "copyFailed": "Không copy được",

    # ---- confirmations and messages
    "ask.deleteFile": "Xoá file này?",
    "ask.recycle": "File sẽ được chuyển vào Thùng rác, có thể phục hồi.",
    "ask.clearFolder": "Dọn sạch thư mục này?",
    "ask.clearNote": "Tất cả sẽ được chuyển vào Thùng rác, có thể phục hồi.",
    "ask.emptyFolder": "Thư mục này đang trống.",
    "ask.stopJob": "Dừng việc này?",
    "ask.removeJob": "Xoá thẻ công việc này?",
    "msg.recycled": "Đã chuyển vào Thùng rác:",
    "msg.deleteFailed": "không xoá được",
    "msg.clearFailed": "không dọn được",
    "msg.cleared": "đã dọn",
    "file": "file",

    # ---- author
    "h2.author": "Tác giả",
    "author.dev": "Dev",
    "author.email": "Email",
    "author.page": "Giới thiệu",
    "tip.copyEmail": "Copy email vào clipboard",

    # ---- foot
    "foot": "<ul><li>Việc chỉ chạy khi cửa sổ đen (server) còn mở — đóng nó "
            "là mọi việc đang chạy bị dừng theo, kể cả ffmpeg.</li>"
            "<li>File tải dở vẫn resume được ở lượt sau.</li>"
            "<li>Trang này không thấy được việc chạy từ Start.cmd.</li></ul>",
}

EN = {
    "head.title": "Cut Heroes 3 stream VODs",
    "tab.fn": "Main",
    "tab.trim": "Trim helper",
    "tab.author": "Author",
    "lang.tip": "Change the interface language",
    "tip.version": "What is new in this build",

    "btn.open": "Open",
    "btn.clear": "Empty",
    "btn.clearAll": "Empty all",
    "btn.copy": "Copy",
    "tip.openFolder": "Open this folder in Explorer",
    "tip.clearFolder": "Send every file in this folder to the Recycle Bin",
    "tip.clearWork": "Send scratch files and the analysis cache to the "
                     "Recycle Bin. Videos in input and output are untouched",
    "tip.clearAll": "Send input + output + work (analysis cache included) to "
                    "the Recycle Bin. Same as choice 6 in Clear.cmd",
    "tip.openWork": "Open the work folder in Explorer",
    "tip.openInput": "Open the input folder in Explorer",

    "h2.step1": "1 · Choose what to do",
    "opt.games.t": "Drop the waiting on the opponent's turn, one video per game",
    "opt.games.d": "One video per game, each with its own timeline, named "
                   "<code>[date] Opponent (game 1).mp4</code>. Split by game, "
                   "not by the opponent's name.",
    "opt.full.t": "Drop the waiting on the opponent's turn, one video in total",
    "opt.full.d": "One finished video, with a timeline .txt to paste into the "
                  "YouTube description. This is the one to upload.",
    "opt.download.t": "Only download the video, cut nothing",
    "opt.download.d": 'Save the original into <code class="p-in">input\\</code> '
                      "and stop. For downloading while the connection is good "
                      "and cutting later — or for keeping the original.",
    "dev.summary": "Developer options",
    "opt.parts.t": "Cut into loose pieces",
    "opt.parts.d": "Every kept stretch as its own file, not joined. For opening "
                   "them one by one to see whether the cuts landed right.",
    "opt.segments.t": "Analyse only, produce no video",
    "opt.segments.d": "Just the list of what would be kept and dropped, and the "
                      "chapter list. The quickest.",
    "paths.video": "Video out",
    "paths.parts": "Loose pieces",

    "h2.step2": "2 · Choose a source",
    "ph.url": "Paste a YouTube link: https://www.youtube.com/watch?v=...",
    "btn.chopen": "From the channel…",
    "tip.chopen": "Open the channel's stream list to take a link from it",
    # ---- the channel card, and the picker it opens
    "chan.live": "LIVE NOW",
    "chan.subs": "Subscribers",
    "chan.latest": "Latest stream",
    "chan.aired": "Aired",
    "chan.have": "On this machine",
    "chan.off": "Not live",
    "chan.haveSub": "of the newest {n}, {c} cut",
    "chan.about": "About the channel",
    "chan.loading": "reading the channel…",
    "chan.failed": "could not read the channel",
    "btn.refresh": "Refresh",
    "btn.seeAll": "All streams",
    "tip.refreshChan": "Ask YouTube about this channel again",
    "tip.chpick": "Switch between the main channel and the backup",
    "ch.head": "Streams from",
    "ch.n10": "newest 10",
    "ch.n20": "newest 20",
    "ch.n100": "newest 100",
    "ch.onlyNew": "only the ones not downloaded",
    "ch.loading": "fetching the list…",
    "ch.failed": "could not fetch it",
    "ch.count": "{n} videos",
    "ch.empty": "This channel has no streams yet.",
    "ch.allDone": "Every stream in this list is already downloaded.",
    "ch.live": "LIVE",
    "ch.notdone": "still running, cannot be downloaded",
    "ch.views": "views",
    "ch.aired": "aired",
    "ch.dateFail": "no date",
    "btn.reload": "Reload",
    "btn.close": "Close",
    "btn.useLink": "Use this link",
    "btn.copyLink": "Copy link",
    "btn.date": "Air date",
    "btn.openCut": "Open the cut",
    "have.cut": "CUT",
    "have.dl": "DOWNLOADED",
    "copy.ok": "Copied",
    "copy.fail": "Could not copy",
    "btn.start": "Download & run",
    "btn.startDl": "Download",
    "sep.orRun": "or run a file already in",
    "empty.reading": "reading…",
    "empty.noInput": "Nothing here yet.",
    "btn.run": "Run",
    "btn.delete": "Delete",
    "tip.showFile": "Open the folder holding this file, with it selected",
    "tip.deleteFile": "Move to the Recycle Bin, recoverable",
    "tip.noRunInDl": "Download-only is selected, and this file is already "
                     "downloaded",

    "h2.jobs": "Jobs",
    "empty.jobs": "Nothing running. Paste a link above to start.",
    "job.stop": "Stop",
    "job.remove": "Remove",
    "job.detail": "Details",
    "job.copyLog": "Copy log",
    "job.openFolder": "Open folder",
    "tip.copyLog": "Copy the whole log and this job's details to the clipboard",
    "tip.openResult": "Open the folder holding the result",
    "kv.mode": "Mode",
    "kv.downloaded": "Downloaded",
    "kv.streams": "Streams",
    "kv.downloader": "Downloader",
    "kv.length": "Length",
    "kv.segments": "Segments",
    "kv.kept": "kept",
    "kv.chapters": "Chapters",
    "kv.source": "Source file",
    "kv.output": "Video out",
    "kv.downloadedFile": "Downloaded file",
    "kv.timeline": "Timeline (.txt)",
    "job.started": "Started",
    "job.finished": "finished",
    "job.took": "took",
    "job.stale": "No new data",

    # ---- version tab
    "tab.ver": "Version",
    "h2.ver": "Version",
    "ver.current": "current",
    "ver.3.0.d": "<ul>"
                 "<li>Cuts any 16:9 source — 720p, 1080p, 1440p. The output "
                 "keeps the source's own resolution.</li>"
                 "<li>Downloads at the source's resolution instead of forcing "
                 "1080p.</li>"
                 "<li>Keeps the source's frame rate instead of forcing 60 — "
                 "about 13% smaller and quicker to render, same picture.</li>"
                 "<li>Anything not 16:9 is refused outright, with the "
                 "reason.</li>"
                 "<li>No more red traceback in the black window when a browser "
                 "hangs up.</li></ul>",
    "ver.2.0.d": "<ul>"
                 "<li>Fixed an inverted cut: the seat was misread, so the "
                 "opponent's turns were kept and Tieulinh's were cut.</li>"
                 "<li>No more slivers of an opponent turn left at either "
                 "end.</li>"
                 "<li>New <b>Remove QR code</b>: the QR is found once and the "
                 "channel logo painted over the whole video.</li>"
                 '<li>The trim helper reads from both <code class="p-in">'
                 "input\\</code> and "
                 '<code class="p-out">output\\</code>.</li>'
                 "<li>Fixed <b>Open folder</b> under Jobs: it opened the wrong "
                 "one and swallowed the error.</li>"
                 "</ul>",
    "ver.1.0.d": "<ul>"
                 "<li>Cuts out the wait on the opponent's turn and joins the "
                 "pieces with a fade to black.</li>"
                 "<li>Downloads a VOD from a YouTube link.</li>"
                 "<li>Writes a chapter timeline by in-game day, ready to paste "
                 "into the description.</li>"
                 "<li>Splits each game out into its own video.</li>"
                 "<li>A local page for progress, and a tab for cutting a short "
                 "test piece.</li>"
                 "</ul>",

    # ---- remove QR tab
    "tab.qr": "Remove QR code",
    "h2.qr": "Remove the QR code from a video",
    "qr.intro": "<ul><li>Pick a video in "
                '<code class="p-in">input\\</code> or '
                '<code class="p-out">output\\</code>, then press '
                "<b>Remove QR</b>.</li>"
                "<li>The new file lands in the same folder as its source, "
                "with <code>[remove-qr]</code> in front of its name.</li>"
                "<li>The original is left alone.</li></ul>",
    "btn.removeQr": "Remove QR",
    "qr.note": "<ul><li>The QR sits in one place for the whole stream, so "
               "it is found once and painted over the whole video.</li>"
               "<li>That re-encodes the file, so it takes about as long as a "
               "cut — watch it under <b>Jobs</b> on the <b>Features</b> "
               "tab.</li>"
               "<li>If it is not found, the usual corner is covered anyway "
               "with a wider margin, and the log says so.</li></ul>",
    "reveal.failed": "could not open that folder",
    "qr.askTitle": "Remove the QR code from this video?",
    "qr.askOut": "New file:",
    "qr.askNote": "This re-encodes the whole file, about as long as a cut. "
                  "The original is left alone.",
    "qr.starting": "starting…",
    "qr.started": "started; watch it under Jobs",
    "qr.failed": "could not remove it",

    "h2.trim": "Cut a range out into its own file",
    "trim.intro": "<ul><li>Pick a video in "
                  '<code class="p-in">input\\</code> or '
                  '<code class="p-out">output\\</code>, seek to the moment '
                  "and press <b>Set here</b>.</li>"
                  "<li>The clip lands in the same folder as its source and "
                  "can be run straight from the <b>Main</b> tab — to try the "
                  "detector on fifteen minutes instead of four hours.</li>"
                  "</ul>",
    "trim.sameFolder": "The new file lands in the same folder as its "
                       "source. The original is left alone.",
    "btn.preview": "Preview",
    "tip.preview": "Load this video into the player",
    "lbl.start": "Start",
    "lbl.end": "End",
    "btn.setHere": "Set here",
    "btn.goto": "Go",
    "btn.cut": "Cut this range out",
    "trim.note": "<ul><li>Copies the streams, no re-encode: ninety minutes "
                 "in a few seconds, and the original pixels.</li>"
                 "<li>In exchange the start lands on the nearest keyframe "
                 "before it, so a clip can run a few seconds longer than "
                 "asked — which for cutting a test piece down does not "
                 "matter.</li></ul>",
    "trim.noVideo": "no video in input or output yet",
    "trim.pickFirst": "There is no video to preview.",
    "trim.noSource": "No video chosen.",
    "trim.badMarks": "Those marks are not valid.",
    "trim.unreadable": "marks unreadable",
    "trim.endAfterStart": "the end must come after the start",
    "trim.long": "length",
    "trim.cutting": "cutting…",
    "trim.cutFailed": "could not cut",
    "trim.done": "Cut:",
    "trim.realLength": "real length",
    "trim.keyframeNote": "(longer than asked, snapped to a keyframe)",
    "trim.cantPlay": "The browser cannot play this file. mp4 and webm it can; "
                     "mkv, ts and avi usually not — but it can still be cut if "
                     "you type the marks in.",
    "ask.cutTitle": "Cut this range out into a new file?",
    "ask.cutNote": "The new file goes into the input folder; the original is "
                   "not touched.",

    "ch.title": "Streams on the channel",
    "ch.newest": "newest",
    "ch.reload": "Reload",
    "ch.close": "Close",
    "ch.loading": "fetching the list…",
    "ch.failed": "could not fetch",
    "ch.videos": "videos",
    "ch.empty": "This channel has no streams yet.",
    "ch.live": "LIVE NOW",
    "ch.liveNoDl": "still live, cannot be downloaded",
    "ch.use": "Use this link",
    "ch.copy": "Copy link",
    "ch.date": "Air date",
    "ch.aired": "aired",
    "ch.views": "views",
    "copied": "Copied",
    "copyFailed": "Could not copy",

    "ask.deleteFile": "Delete this file?",
    "ask.recycle": "It goes to the Recycle Bin and can be restored.",
    "ask.clearFolder": "Empty this folder?",
    "ask.clearNote": "Everything goes to the Recycle Bin and can be restored.",
    "ask.emptyFolder": "This folder is already empty.",
    "ask.stopJob": "Stop this job?",
    "ask.removeJob": "Remove this job card?",
    "msg.recycled": "Moved to the Recycle Bin:",
    "msg.deleteFailed": "could not delete",
    "msg.clearFailed": "could not empty",
    "msg.cleared": "emptied",
    "file": "files",

    "h2.author": "Author",
    "author.dev": "Dev",
    "author.email": "Email",
    "author.page": "About",
    "tip.copyEmail": "Copy the email to the clipboard",

    "foot": "<ul><li>Jobs only run while the black window (the server) is "
            "open — closing it stops everything running, ffmpeg included.</li>"
            "<li>A part-downloaded file still resumes next time.</li>"
            "<li>This page cannot see runs started from Start.cmd.</li></ul>",
}

STRINGS = {"vi": VI, "en": EN}
DEFAULT = "vi"


def check():
    """Both languages carry the same keys, or say which ones they do not.

    The failure this catches is the one that happens: a string added to the
    page in one language and forgotten in the other, which shows up as a blank
    label only when somebody switches.
    """
    missing = {}
    keys = set().union(*(set(d) for d in STRINGS.values()))
    for lang, table in STRINGS.items():
        gap = sorted(keys - set(table))
        if gap:
            missing[lang] = gap
    if missing:
        raise ValueError(f"i18n keys missing: {missing}")
    return len(keys)


check()
