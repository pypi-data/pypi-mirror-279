import argparse
import datetime
import os
import pathlib
import re

from PIL import Image
from audio2splitted.audio2splitted import get_split_audio_scheme, make_split_audio
from dotenv import load_dotenv
from pytube.extract import video_id
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from mutagen.mp4 import MP4

from utils4audio.duration import get_duration
from ytb2audio.ytb2audio import download_audio, download_thumbnail
from datetime import timedelta


def get_youtube_move_id(url: str):
    try:
        movie_id = video_id(url)
    except Exception as e:
        return None
    return movie_id


def output_filename_in_telegram(text):
    name = (re.sub(r'[^\w\s\-\_\(\)\[\]]', ' ', text)
            .replace('    ', ' ')
            .replace('   ', ' ')
            .replace('  ', ' ')
            .strip())

    return f'{name}.m4a'


DATA_DIR = 'data'

TIMECODES_THRESHOLD_COUNT = 3
SEND_AUDIO_TIMEOUT = 120
TELEGRAM_CAPTION_TEXT_LONG_MAX = 1024


def clean_timecodes_text(text):
    text = (text
            .replace('---', '')
            .replace('--', '')
            .replace('===', '')
            .replace('==', '')
            .replace(' =', '')
            .replace('___', '')
            .replace('__', '')
            .replace('_ _ _', '')
            .replace('_ _', '')
            .replace(' _', '')
            .replace('\n-', '')
            .replace('\n=', '')
            .replace('\n_', '')
            .replace('\n -', '')
            .replace('\n =', '')
            .replace('\n _', '')
            .strip()
            .lstrip()
            .rstrip()
            )
    return text


def telegram_caption_text_limit(text):
    groups = [0]
    text_tmp = ''
    rows = text.split('\n')
    for idx, row in enumerate(rows):
        total_len = len(text_tmp) + len(row)
        if total_len > TELEGRAM_CAPTION_TEXT_LONG_MAX:
            groups.append(idx)
            text_tmp = ''
        text_tmp += f'{row}\n'

    grps = []
    for border in groups[1:]:
        grps += [border - 1, border]
    grps = [0] + grps + [len(rows) - 1]

    parts = []
    part = []
    for idx in grps:
        part.append(idx)
        if len(part) == 2:
            parts.append(part)
            part = []

    text_parts = []

    for part in parts:
        slice_rows = rows[part[0]:part[1]]
        text_parts.append('\n'.join(slice_rows))

    return text_parts


def get_timecodes_text(description):
    if not description:
        return
    if type(description) is not list:
        return
    if len(description) < 1:
        return ''

    for part in description[0].split('\n\n'):
        matches = re.compile(r'(\d{1,2}:\d{2})').findall(part)
        if len(matches) > TIMECODES_THRESHOLD_COUNT:
            return clean_timecodes_text(part)


def capital2lower_letters_filter(text):
    CAPITAL_LETTERS_PERCENT_THRESHOLD = 0.3
    count_capital = sum(1 for char in text if char.isupper())
    if count_capital / len(text) < CAPITAL_LETTERS_PERCENT_THRESHOLD:
        return text

    text = text.lower()
    text = text[0].upper() + text[1:]
    return text


def image_compress_and_resize(
        path: pathlib.Path,
        output: pathlib.Path = None,
        quality: int = 80,
        thumbnail_size=(960, 960)
):
    image = Image.open(path)
    image.thumbnail(thumbnail_size)
    if not output:
        output = path
    image.save(output, optimize=True, quality=quality)
    return output


async def error_handler(post, text):
    print(text)
    await post.edit_text(text)
    return


AUDIO_SPLIT_THRESHOLD_MINUTES = 15
AUDIO_SPLIT_DELTA_SECONDS = 5


def time_to_seconds(time_str):
    if time_str.count(':') == 1:
        format_str = '%M:%S'
        time_obj = datetime.datetime.strptime(time_str, format_str)
        total_seconds = time_obj.minute * 60 + time_obj.second
    elif time_str.count(':') == 2:
        format_str = '%H:%M:%S'
        time_obj = datetime.datetime.strptime(time_str, format_str)
        total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    else:
        raise ValueError("Time format not recognized")
    return total_seconds


def filter_timestamp_format(time):
    time = str(time)
    if time == '0:00':
        return '0:01'

    if time == '00:00':
        return '0:01'

    if time == '0:00:00':
        return '0:01'

    if time == '00:00:00':
        return '0:01'

    if time.startswith('00:00:0'):
        return time.replace('00:00:0', '0:0')

    if time.startswith('0:00:0'):
        return time.replace('0:00:0', '0:0')

    if time.startswith('00:00:'):
        return time.replace('00:00:', '0:')

    if time.startswith('0:00:'):
        return time.replace('0:00:', '0:')

    time = f'@@{time}##'
    time = time.replace('@@00:00:0', '@@0:0')
    time = time.replace('@@0:0', '@@')
    time = time.replace('@@0:', '@@')

    return time.replace('@@', '').replace('##', '')


def get_timestamps_group(text, scheme):
    timestamps_findall_results = re.findall(r'(\d*:?\d+:\d+)\s+(.+)', text)
    if not timestamps_findall_results:
        return ['' for part in range(len(scheme))]

    timestamps_all = [{'time': time_to_seconds(stamp[0]), 'title': stamp[1]} for stamp in timestamps_findall_results]

    timestamps_group = []
    for idx, part in enumerate(scheme):
        output_rows = []
        for stamp in timestamps_all:
            if stamp.get('time') < part[0] or part[1] < stamp.get('time'):
                continue
            time = filter_timestamp_format(timedelta(seconds=stamp.get('time') - part[0]))
            title = capital2lower_letters_filter(stamp.get('title'))
            output_rows.append(f'{time} - {title}')
        timestamps_group.append('\n'.join(output_rows))

    return timestamps_group


async def processing_ytb2audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        print('🟥No update.message.text. Skip.')
        return

    if not (movie_id := get_youtube_move_id(update.message.text)):
        print('🟥️ Not a Youtube Url. Skip.')
        return

    post_status = await context.bot.send_message(
        chat_id=update.message.from_user.id,
        reply_to_message_id=update.message.id,
        text=f'⌛️ Downloading ... '
    )

    data_dir = pathlib.Path(DATA_DIR)
    data_dir.mkdir(parents=True, exist_ok=True)

    audio = download_audio(movie_id, data_dir)
    audio = pathlib.Path(audio)
    if not audio.exists():
        return await error_handler(post_status, f'🟥 Unexpected error. After Check m4a_file.exists.')

    thumbnail = download_thumbnail(movie_id, data_dir)
    thumbnail = pathlib.Path(thumbnail)
    if not thumbnail.exists():
        return await error_handler(post_status, f'🟥 Unexpected error. After Check thumbnail.exists().')

    thumbnail_compressed = image_compress_and_resize(thumbnail)
    if thumbnail_compressed.exists():
        thumbnail = thumbnail_compressed
    else:
        await error_handler(post_status, f'🟥 Problem with image compression.')

    duration_minutes = 14

    audio_duration = get_duration(audio)
    scheme = get_split_audio_scheme(
        source_audio_length=audio_duration,
        duration_seconds=duration_minutes * 60,
        delta_seconds=AUDIO_SPLIT_DELTA_SECONDS,
        magic_tail=True,
        threshold_seconds=AUDIO_SPLIT_THRESHOLD_MINUTES * 60
    )
    print('📊 scheme: ', scheme)

    audios = make_split_audio(
        audio_path=audio,
        audio_duration=audio_duration,
        output_folder=data_dir,
        scheme=scheme
    )

    await post_status.edit_text('⌛ Uploading to Telegram ... ')

    try:
        audio_mp4obj = MP4(audio)
    except Exception as e:
        await error_handler(post_status, f'🟥 Exception as e: [m4a = MP4(m4a_file.as_posix())]. \n\n{e}')
        audio_mp4obj = {}

    if not audio_mp4obj:
        await error_handler(post_status, '🟥 Unexpected error. [not audio in MP4 metadata].')

    title = str(movie_id)
    if audio_mp4obj.get('\xa9nam'):
        title = audio_mp4obj.get('\xa9nam')[0]

    url_youtube = f'youtu.be/{movie_id}'
    link_html = f'<a href=\"{url_youtube}\">{url_youtube}</a>'

    title = capital2lower_letters_filter(title)
    caption_head = f'{title}\n{link_html}'
    filename_head = output_filename_in_telegram(title)

    timecodes = ['' for part in range(len(scheme))]
    if timecodes_text := get_timecodes_text(audio_mp4obj.get('desc')):
        timecodes = get_timestamps_group(timecodes_text, scheme)

    for idx, audio_part in enumerate(audios, start=1):
        print('💜 Idx: ', idx, 'part: ', audio_part)
        path = audio_part.get('path')

        duration_seconds = audio_part.get('duration')

        filename = filename_head
        caption = f'{caption_head} [{timedelta(seconds=audio_duration)}]'
        if len(audios) != 1:
            filename = f'(p{idx}-of{len(audios)}) {filename_head}'
            caption = f'[Part {idx} of {len(audios)}] {caption_head} [{timedelta(seconds=duration_seconds)}]'

        caption += f'\n\n{timecodes[idx - 1]}'

        with thumbnail.open('rb') as thumbnail_file:
            audio_post = await context.bot.send_audio(
                chat_id=update.message.from_user.id,
                reply_to_message_id=None if idx > 1 else update.message.id,
                audio=path.as_posix(),
                duration=duration_seconds,
                filename=filename,
                thumbnail=thumbnail_file,
                caption=caption,
                parse_mode=ParseMode.HTML,
                pool_timeout=SEND_AUDIO_TIMEOUT,
                write_timeout=SEND_AUDIO_TIMEOUT,
                read_timeout=SEND_AUDIO_TIMEOUT,
                connect_timeout=SEND_AUDIO_TIMEOUT
            )

    await post_status.delete()

    if context.bot_data.get('keepfiles') == 0:
        for file in filter(lambda f: f.name.startswith(movie_id), pathlib.Path(DATA_DIR).iterdir()):
            try:
                file.unlink()
            except Exception as e:
                print(f'🟠 Failed to delete {file}: {e}')

    print(f'💚 Success! [{movie_id}]\n')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Help text',
        parse_mode=ParseMode.HTML
    )


def run_bot(token: str, opt_keepfiles: str):
    print('🚀 Run bot...')

    application = ApplicationBuilder().token(token).build()

    application.bot_data['keepfiles'] = opt_keepfiles

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, processing_ytb2audio))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    parser = argparse.ArgumentParser(description='Bot ytb 2 audio')
    parser.add_argument('--keepfiles', type=int,
                        help='Keep raw files 1=True, 0=False (default)', default=0)

    args = parser.parse_args()

    load_dotenv()
    token = os.environ.get("TG_TOKEN")
    if not token:
        print('⛔️ No telegram bot token. Exit')
        return

    run_bot(token, args.keepfiles)


if __name__ == "__main__":
    main()
