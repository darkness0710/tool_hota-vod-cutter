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
    "tab.set": "Cài đặt",
    "lang.tip": "Đổi ngôn ngữ giao diện",

    # ---- settings tab
    "h2.set": "Cài đặt",
    "set.minGame.t": "Bỏ qua ván ngắn hơn",
    "set.minGame.d": "Đo trên <b>độ dài ván trong video gốc</b>, không phải độ "
                     "dài video xuất ra — một ván dài bao nhiêu là chuyện của "
                     "ván đấu, còn cắt được bao nhiêu là chuyện của bộ dò. Chỉ "
                     "áp dụng cho chế độ <b>tách theo game</b>. Đặt <b>0</b> "
                     "để xuất mọi ván.<br>Ván bị bỏ qua vẫn <b>giữ nguyên số "
                     "thứ tự</b> — bỏ ván 3 thì ván sau vẫn tên là ván 4 — và "
                     "được ghi rõ trong log để biết mà hạ ngưỡng xuống nếu lỡ "
                     "mất ván hay.",
    "set.stall.t": "Tự chạy lại khi tiến trình im quá",
    "set.stall.d": "Đếm từ lần cuối tiến trình <b>in ra bất cứ thứ gì</b>, "
                   "không phải từ lần cuối tốc độ thay đổi — một lần tải "
                   "chậm vẫn in mỗi giây một dòng nên không bao giờ bị động tới. "
                   "Đặt <b>0</b> để tắt.<br>Chỉ áp dụng cho <b>khâu tải</b>: "
                   "tải lại thì tiếp tục từ file <code>.part</code> nên gần như "
                   "không mất gì, còn chạy lại khâu phân tích hay render thì có "
                   "thể mất cả tiếng đồng hồ — hai khâu đó vẫn phải bấm tay. "
                   "Khâu <b>ghép video + audio</b> vốn không in gì nên được "
                   "gấp 3 lần thời gian này.<br>Tự chạy lại tối đa <b>3 lần</b> "
                   "liên tiếp rồi dừng, để không quay vòng vô tận với một link hỏng.",
    "set.minutes": "phút",
    "set.save": "Lưu",
    "set.saved": "đã lưu",
    "set.clamped": "ngoài khoảng cho phép, đã đặt thành {n}",
    "set.failed": "không lưu được",
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
    # Three ways a job can go quiet. They look identical on screen unless the
    # page says which one it is, and they want opposite reactions from the
    # reader: wait, wait, or act.
    "job.merging": "Đang ghép video + audio — khâu này không báo tiến độ, "
                   "video càng lớn càng lâu",
    "job.aliveUnread": "Vẫn đang chạy, nhưng trang chưa đọc được tiến độ",
    "job.heardAgo": "nhận tín hiệu {t} trước",
    "job.silent": "Không nhận được gì từ tiến trình trong {t}",
    "job.asOf": "số liệu ở trên là lúc {t}, không còn mới",
    "job.restart": "Chạy lại",
    "job.restarted": "Đã chạy lại",
    "job.restartFail": "không chạy lại được",
    # A fourth kind of quiet, and the only one that ends by itself: fetch.py
    # waits 30 seconds between attempts, which is longer than the floor the
    # page calls a stall, so without a line of its own every retry showed a
    # red warning for a run that was about to carry on.
    "job.retrying": "Lần tải vừa rồi hỏng, đang chờ thử lại — phần đã tải giữ nguyên",
    "job.autoRestart": "trang tự chạy lại lần {n} vì tiến trình cũ im",
    "job.giveup": "Đã tự chạy lại {n} lần mà vẫn im. Trang không tự chạy lại nữa — xem log rồi bấm Chạy lại nếu muốn thử tiếp.",
    "ask.restart.t": "Chạy lại việc này?",
    "ask.restart.keep": "Phần đã tải được giữ nguyên, tải tiếp từ đó.",
    "ask.restart.stop": "Tiến trình hiện tại sẽ bị dừng.",

    # ---- version tab
    "tab.ver": "Phiên bản",
    "h2.ver": "Phiên bản",
    "ver.current": "hiện tại",
    "ver.4.2.d": "<ul>"
                 "<li>Sửa lỗi <b>video tách theo game bị cắt giữa trận combat cuối</b>. Trong combat, ô ngày ở góc dưới bị làm mờ và số <b>4, 5, 7</b> đọc không ra, nên tool tưởng ván đã hết ở lần cuối đọc được đủ ngày — có video dừng ở round 2, mất nửa phút cuối trận và cả bảng “YOU WIN”.</li>"
                 "<li>Giờ nếu tháng và tuần vẫn đọc được và khớp với ngay trước đó, tool coi như vẫn là ngày đó, nên ván kéo tới hết trận. Chạy thử lại trên nguyên stream 5 tiếng 26 phút: ván bị lỗi giờ kết thúc sau “YOU WIN”, 9 ván còn lại không đổi.</li>"
                 "</ul>",
    "ver.4.1.d": "<ul>"
                 "<li>Trang <b>tự chạy lại một lần tải bị treo</b>. Trước đây "
                 "một lần tải chết lúc 2 giờ sáng thì sáng ra vẫn nằm nguyên ở "
                 "chỗ đó — có lần đứng im 2 tiếng 7 phút. Giờ nếu tiến trình "
                 "không in ra gì suốt 30 phút, trang tự dừng và tải tiếp từ chỗ "
                 "đang dở. Đổi số phút hoặc tắt hẳn ở tab <b>Cài đặt</b>.</li>"
                 "<li>Chỉ áp dụng cho <b>khâu tải</b>, vì tải lại thì tiếp tục từ "
                 "file dở nên gần như không mất gì. Khâu phân tích và render vẫn "
                 "phải bấm tay.</li>"
                 "<li>Đếm theo <b>“tiến trình có in ra gì không”</b>, không phải "
                 "theo tốc độ — một lần tải chậm vẫn in mỗi giây một dòng nên "
                 "không bao giờ bị động tới. Tối đa <b>3 lần</b> liên tiếp rồi "
                 "dừng hẳn.</li>"
                 "<li>Thẻ việc <b>đọc được lúc đang thử lại</b>, thay vì 30 "
                 "giây trắng trơn kèm một cảnh báo treo giả.</li>"
                 "<li>Dòng lỗi đỏ <b>không còn dính lại</b> sau khi lần thử sau "
                 "chạy được.</li>"
                 "<li>Thông báo <b>tải hỏng hẳn</b> giờ hiện ra được.</li>"
                 "<li>Sửa dấu <code>]</code> thừa ở cuối dòng tốc độ tải.</li>"
                 "</ul>",
    "ver.4.0.d": "<ul>"
                 "<li>Thêm tab <b>Cài đặt</b>, và ô <b>bỏ qua ván ngắn hơn N "
                 "phút</b> (mặc định 30) cho chế độ tách theo game — ván chết "
                 "biome hoặc đối thủ GG sớm không còn tốn công render. Ván bị "
                 "bỏ vẫn giữ nguyên số thứ tự và được ghi rõ trong log.</li>"
                 "<li>Trang phân biệt được <b>ba kiểu “đứng im”</b> thay vì gộp "
                 "làm một: đang chạy bình thường, đang ghép video (khâu này vốn "
                 "không báo tiến độ), và im thật.</li>"
                 "<li>Số liệu cũ bị <b>làm mờ và gạch ngang</b> khi tiến trình "
                 "im, thay vì hiện y như số đang chạy.</li>"
                 "<li>Thêm nút <b>Chạy lại</b> khi một việc im thật — phần đã "
                 "tải được giữ nguyên và tải tiếp.</li>"
                 "<li>Hết báo động giả ở khâu <b>ghép video + audio</b>.</li>"
                 "<li>Thêm nút <b>Dọn</b> cho <code>work\\</code> và "
                 "<b>Dọn tất cả</b>, kèm dung lượng sẽ xoá.</li>"
                 "<li>Render lỗi giờ <b>tự dọn file tạm</b> thay vì bỏ lại "
                 "hàng GiB không ai dùng tới.</li>"
                 "<li>Sửa lỗi cắt ngược khi Tieulinh <b>đổi ghế giữa các "
                 "ván</b>.</li>"
                 "<li>Không còn sót <b>mẩu lượt đối thủ</b> 5–11 giây xen giữa "
                 "các đoạn.</li></ul>",
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
    "tab.set": "Settings",
    "lang.tip": "Change the interface language",

    "h2.set": "Settings",
    "set.minGame.t": "Skip games shorter than",
    "set.minGame.d": "Measured on the <b>length of the game in the source</b>, "
                     "not the length of the video produced — how long a game "
                     "ran is a fact about the game, how much survives is a "
                     "fact about the detector. Applies only to <b>one video "
                     "per game</b>. Set <b>0</b> to render every game.<br>"
                     "A skipped game <b>keeps its number</b> — drop game 3 and "
                     "the next one is still game 4 — and is named in the log, "
                     "so a good game lost to the threshold can be found and "
                     "the number lowered.",
    "set.stall.t": "Restart automatically after silence of",
    "set.stall.d": "Counted from the last time the process printed "
                   "<b>anything at all</b>, not from the last change in speed "
                   "— a slow download still prints a line a second and is "
                   "never touched. Set <b>0</b> to switch it off.<br>"
                   "Applies to the <b>download</b> step only: a restart there "
                   "resumes from the <code>.part</code> file and costs almost "
                   "nothing, while restarting analysis or rendering can throw "
                   "away an hour — those two stay on the manual button. The "
                   "<b>video + audio mux</b> prints nothing by design and is "
                   "given three times this long.<br>At most <b>3</b> automatic "
                   "restarts in a row, so a broken link cannot loop for ever.",
    "set.minutes": "minutes",
    "set.save": "Save",
    "set.saved": "saved",
    "set.clamped": "outside the allowed range, set to {n}",
    "set.failed": "could not save",
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
    "job.merging": "Muxing video + audio — this step reports no progress, and "
                   "takes longer the larger the video is",
    "job.aliveUnread": "Still running, but the page cannot read its progress",
    "job.heardAgo": "heard from {t} ago",
    "job.silent": "Nothing heard from the process for {t}",
    "job.asOf": "the figures above are from {t} and are no longer current",
    "job.restart": "Run again",
    "job.restarted": "Started again",
    "job.restartFail": "could not start it again",
    "job.retrying": "That attempt failed; waiting to try again — what has "
                    "downloaded is kept",
    "job.autoRestart": "started again automatically, attempt {n}, after the "
                       "last process went silent",
    "job.giveup": "Restarted automatically {n} times and still silent. No "
                  "further automatic restarts — read the log, then press "
                  "Run again to keep trying.",
    "ask.restart.t": "Run this job again?",
    "ask.restart.keep": "What has already downloaded is kept and resumed.",
    "ask.restart.stop": "The current process will be stopped.",

    # ---- version tab
    "tab.ver": "Version",
    "h2.ver": "Version",
    "ver.current": "current",
    "ver.4.2.d": "<ul>"
                 "<li>Fixed <b>per-game videos cut off in the middle of the last fight</b>. Combat dims the day counter at the bottom right, and the digits <b>4, 5 and 7</b> could not be read there, so a game was taken to end at its last full reading — one video stopped in round 2, losing the last half minute of the fight and the “YOU WIN” screen.</li>"
                 "<li>A reading whose month and week still agree with the one just before it now counts as the same day, so the game runs to the end of the fight. Re-run over the whole 5h26 stream: the broken game now ends after “YOU WIN”, and the other nine are unchanged.</li></ul>",
    "ver.4.1.d": "<ul>"
                 "<li>The page now <b>restarts a stalled download by "
                 "itself</b>. A download that died at 2am used to still be "
                 "sitting there in the morning — one sat silent for 2 hours "
                 "and 7 minutes. Now, if the process prints nothing for 30 "
                 "minutes, the page stops it and resumes from what is on "
                 "disk. Change the number or switch it off on the "
                 "<b>Settings</b> tab.</li>"
                 "<li>Downloads only, because a restart there resumes from "
                 "the part file and costs almost nothing. Analysis and "
                 "rendering still need the button.</li>"
                 "<li>Measured on <b>whether the process printed anything</b>, "
                 "not on speed — a slow download still prints a line a second "
                 "and is never touched. At most <b>3</b> automatic restarts in "
                 "a row.</li>"
                 "<li>The card can now <b>read a retry while it happens</b>, "
                 "instead of 30 blank seconds under a false stall "
                 "warning.</li>"
                 "<li>The red error line <b>no longer sticks</b> once a later "
                 "attempt succeeds.</li>"
                 "<li>The <b>download gave up for good</b> message is readable "
                 "at last.</li>"
                 "<li>Fixed the stray <code>]</code> at the end of the "
                 "download speed line.</li></ul>",
    "ver.4.0.d": "<ul>"
                 "<li>New <b>Settings</b> tab, with <b>skip games shorter than "
                 "N minutes</b> (default 30) for the per-game mode — a biome "
                 "death or an early concede no longer costs a render. Skipped "
                 "games keep their number and are named in the log.</li>"
                 "<li>The page tells <b>three kinds of “stuck”</b> apart "
                 "instead of merging them: running normally, muxing the video "
                 "(a step that reports nothing), and genuinely silent.</li>"
                 "<li>Stale figures are <b>dimmed and struck through</b> when "
                 "a job goes silent, rather than shown as if current.</li>"
                 "<li>New <b>Run again</b> button for a silent job — what has "
                 "downloaded is kept and resumed.</li>"
                 "<li>No more false alarm during <b>video + audio "
                 "muxing</b>.</li>"
                 "<li>New <b>Empty</b> button for <code>work\\</code> and an "
                 "<b>Empty all</b>, both showing what they would free.</li>"
                 "<li>A failed render now <b>discards its own scratch</b> "
                 "instead of stranding gigabytes.</li>"
                 "<li>Fixed the inverted cut when Tieulinh <b>changes seat "
                 "between games</b>.</li>"
                 "<li>No more 5–11 second <b>slivers of the opponent's "
                 "turn</b> left between segments.</li></ul>",
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
