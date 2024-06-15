import os
import yt_dlp as youtube_dl
import ffmpeg

class GetAudio():
    

    def set_directory_permissions(self, path):
        try:
            # 使用chmod 777命令设置目录权限
            os.chmod(path, 0o777)
            print(f'Successfully set permissions for directory: {path}')
        except Exception as e:
            print(f'Failed to set permissions for directory: {path}')
            print(e)


    def set_available_formats(self, url):
        ydl_opts = {
            'format': 'best',
            'listformats': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            for f in formats:
                print(f)
                format_id = f.get('format_id', 'Unknown ID')
                format_name = f.get('format', 'Unknow name')
                if 'audio' in format_name:
                    self.format_code = format_id
                    self.file_ext = f.get('ext')
                    break
                    print(format_id, format_name)


    def convert_to_mp3(self, input_file, output_file):
        try:
            (
                ffmpeg
                .input(input_file)
                .output(output_file)
                .run()
            )
            print(f'Successfully converted {input_file} to {output_file}')
        except ffmpeg.Error as e:
            print(f'Error occurred: {e.stderr.decode()}')
 

    def download_video(self, url, save_path, format_code, file_ext):
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 设置目录权限
        self.set_directory_permissions(save_path)
    
        # 定义下载选项
        ydl_opts = {
            'format': format_code,  # 下载最高质量的视频
            'outtmpl': os.path.join(save_path, f'test.{file_ext}'),  # 保存文件名为视频标题，指定保存路径
            'noplaylist': True,  # 如果URL是播放列表，只下载第一个视频
            'nocheckcertificate': True, # 忽略ssl
            'continuedl ': True # 断点续传
        }

        # 使用yt_dlp下载视频
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    
if __name__ == '__main__':
    get_audio = GetAudio()
    # 视频URL
    # 哔哩哔哩的视频url
    video_url = ''
    save_path = '/home/drq/python/get_audio'
    # 列出可用格式
    get_audio.set_available_formats(video_url)
    # 下载视频
        
    get_audio.download_video(video_url, save_path, format_code=get_audio.format_code, file_ext=get_audio.file_ext)

    # 转换下载的文件为 MP3
    input_file = os.path.join(save_path, f'test.{get_audio.file_ext}')
    output_file = os.path.join(save_path, 'test.mp3')
    get_audio.convert_to_mp3(input_file, output_file)



