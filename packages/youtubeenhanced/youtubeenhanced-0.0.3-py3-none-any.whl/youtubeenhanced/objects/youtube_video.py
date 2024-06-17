from ..utils.downloader import download_file
from yt_dlp import YoutubeDL
from os import remove as os_remove
from random import uniform as random_uniform

SUBTITLE_TYPE_JSON3 = 'json3'
SUBTITLE_TYPE_SRV1 = 'srv1'
SUBTITLE_TYPE_SRV2 = 'srv2'
SUBTITLE_TYPE_SRV3 = 'srv3'
SUBTITLE_TYPE_TTML = 'ttml'
SUBTITLE_TYPE_VTT = 'vtt'
VALID_SUBTITLES_TYPES = [SUBTITLE_TYPE_JSON3, SUBTITLE_TYPE_SRV1, SUBTITLE_TYPE_SRV2, SUBTITLE_TYPE_SRV3, SUBTITLE_TYPE_TTML, SUBTITLE_TYPE_VTT]

# TODO: Set all languages
LANGUAGE_ARABIC = 'ar'
LANGUAGE_SPANISH = 'es'
LANGUAGE_CHINESE_TRADITIONAL = 'zh-Hant'
LANGUAGE_ENGLISH = 'en'
LANGUAGE_FRENCH = 'fr'
LANGUAGE_GERMAN = 'de'
LANGUAGE_HINDO = 'hi'
LANGUAGE_JAPANESE = 'ja'
LANGUAGE_KOREAN = 'ko'
LANGUAGE_PORTUGUESE = 'pt'
LANGUAGE_RUSSIAN = 'ru'
LANGUAGE_INDONESIAN = 'in'
LANGUAGE_TURKISH = 'tr'
LANGUAGE_VIETNAMESE = 'vi'
LANGUAGE_DEFAULT = 'default'
VALID_LANGUAGES = [LANGUAGE_ARABIC, LANGUAGE_SPANISH, LANGUAGE_CHINESE_TRADITIONAL, LANGUAGE_ENGLISH, LANGUAGE_FRENCH, LANGUAGE_GERMAN, LANGUAGE_HINDO, LANGUAGE_JAPANESE, LANGUAGE_KOREAN, LANGUAGE_PORTUGUESE, LANGUAGE_RUSSIAN, LANGUAGE_INDONESIAN, LANGUAGE_TURKISH, LANGUAGE_VIETNAMESE, LANGUAGE_DEFAULT]

QUALITY_4K = 2160
QUALITY_2K = 1440
QUALITY_FULL_HD = 1080
QUALITY_HD = 720
QUALITY_STANDARD = 480
QUALITY_LOW = 360
QUALITY_MINIMUM = 240
QUALITY_DEFAULT = 1
VALID_QUALITIES = [QUALITY_4K, QUALITY_2K, QUALITY_FULL_HD, QUALITY_HD, QUALITY_STANDARD, QUALITY_LOW, QUALITY_MINIMUM, QUALITY_DEFAULT]

class YoutubeVideo:
    """
    An object that represents a Youtube video with all its data and metadata. It just
    needs the url to load all the information.
    """
    def __init__(self, url):
        self.url = url

        ydl_opts = {
            #'listformats': True,
            'format': 'bestaudio/best',
            #'outtmpl': '%(title)s.%(ext)s', # You can change the PATH as you want
            #'download_archive': 'downloaded.txt',
            'noplaylist': True,   
            'quiet': True,
            'no_warnings': True,
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
            #'progress_hooks': [hook]
        }
        self.youtubedl = YoutubeDL(ydl_opts)

        self.__load_data()

        #self.youtubedl.download([url])
        #print(self.video_formats)
        #print(self.audio_formats)
        #print(self.get_best_quality_audio_format(LANGUAGE_SPANISH))
        #print(self.get_best_quality_video_format())

    def __load_data(self):
        """
        Makes a request and loads the data for the specific Youtube video. This will refresh
        url links expiration time.
        """
        # Urls have expiration token, so I do the 'get_data' here to force, with this method
        # to get the data again if outdated, but using only one 'youtubedl' service loaded
        # on __init__ method.
        self.data = self.youtubedl.extract_info(self.url, download = False)

        self.__get_id()
        self.__get_thumbnail()
        self.__get_duration()
        self.__get_description()
        self.__get_views_count()
        self.__get_likes_count()
        self.__get_comments_count()
        self.__get_heatmap()
        self.__get_key_moment()
        self.__get_attribution()
        self.__get_all_subtitles()
        self.__get_all_automatic_subtitles()
        self.__get_all_formats()

        self.__get_video_formats()
        self.__get_audio_formats()

    def __get_id(self):
        self.id = self.data['id']

    def __get_thumbnail(self):
        self.thumbnail = self.data['thumbnail']

    def __get_duration(self):
        self.duration = self.data['duration']

    def __get_description(self):
        self.description = self.data['description']

    def __get_views_count(self):
        self.views = self.data['view_count']

    def __get_likes_count(self):
        self.likes = self.data.get('like_count')

    def __get_comments_count(self):
        self.comments = self.data['comment_count']

    def __get_heatmap(self):
        self.heatmap = self.data['heatmap']

    def __get_key_moment(self):
        """
        This method gets the key moment from description, that is written in a
        specific way so we can read it to our own benefit. This key moment is
        set manually to let our system know in which video second happens the
        most interesting thing of the video. 
        """
        # Read from self.description
        self.key_moment = 0
        if '@@@@@@@@@@' in self.description:
            try:
                # We wrap the key moment in an specific way
                self.key_moment = float(self.description.split('@@@@@@@@@@')[1].strip().split('=')[1])
            except:
                pass

        return self.key_moment

    def __get_attribution(self):
        """
        This method gets the song attribution from description, that is written in
        a specific way so we can read it. This attribution is to know which songs
        we have used in the video so we can add them in our final video, as the
        attribution, when uploaded.
        """
        self.attribution = ''
        if 'Attribution is just below' in self.description:
            try:
                self.attribution = self.description.split('Attribution is just below')[1]
            except:
                pass

        return self.attribution

    def get_hottest_moments(self, moments_number, ordered_by_time = False):
        """
        Returns the 'moments_number' hottest moments of the video based on the 'heatmap'
        if existing. If it doesn't exist, it just return None as it can not be calculated.

        This method is calculated on-demand to avoid useless calculations if it won't be
        used.

        If 'ordered_by_time' is True, it will return those X moments but ordered from
        begin to end of the video.

        Each element returned has 'start', 'end' and 'score' (but 'score' is only for internal
        use so you can ignore it).

        This moments are not given always by Youtube. When given, they represent the moments
        that people have played the most of the time. Those hot moments are intervals of time.
        That is the graph you can see when mouse hover the Youtube player timeline.
        """
        if not self.heatmap:
            return None
        else:
            hottest_moments = [{
                'start': -1,
                'end': -1,
                'score': -1,   
            }]

            for heatmap_moment in self.heatmap:
                # 'start_time', 'end_time' and 'value' (score)
                for index, hot_moment in enumerate(hottest_moments):
                    if heatmap_moment['value'] > hot_moment['score']:
                        # TODO: What about moments that collide?
                        hottest_moments.insert(index, {
                            'start': heatmap_moment['start_time'],
                            'end': heatmap_moment['end_time'],
                            'score': heatmap_moment['value']
                        })

                         # If we have more moments than the limit, we remove the last (the less viewed)
                        if len(hottest_moments) > moments_number:
                            hottest_moments.pop()
                        break
            
        if ordered_by_time:
            hottest_moments_ordered_by_time = [{
                'start': 99999999999,
                'end': 99999999999,
                'score': -1,  
            }]

            for hot_moment in hottest_moments:
                for index, moment in enumerate(hottest_moments_ordered_by_time):
                    if hot_moment['start'] < moment['start']:
                        hottest_moments_ordered_by_time.insert(index, hot_moment)
                        break

            # We remove the additional moment that we used in the comparison
            if len(hottest_moments_ordered_by_time) > moments_number:
                hottest_moments_ordered_by_time.pop()

            hottest_moments = hottest_moments_ordered_by_time

        return hottest_moments

    def get_scenes(self, scenes_number, scene_duration):
        """
        Returns 'scenes_number' scenes of 'scene_duration' that are from the video. Each
        of those scenes has 'start' and 'end' attributes to be able to subclip the clip.

        Imagine a video of 10 minutes, and we want 5 ('scenes_number') scenes. We will 
        first crop the video in 5 different scenes of 2 minutes each one. Then, we will
        get only 'scene_duration' seconds of each of those scenes.
        """
        scene_fragment_duration = self.duration / scenes_number
        scenes = []
        for i in range(scenes_number):
            # We calculate the center for our scene
            scene_segment_start = (i * scene_fragment_duration) + (scene_duration / 2)
            scene_segment_end = (scene_segment_start + scene_fragment_duration) - (scene_duration / 2)

            # Generate a random between our valid limits for each segment
            start = random_uniform(scene_segment_start, scene_segment_end)
            scenes.append({
                'start': start,
                'end': start + scene_duration
            })

        return scenes
    
    def __get_all_subtitles(self):
        self.subtitles = self.data['subtitles']
    
    def get_subtitles(self, language = LANGUAGE_DEFAULT, format = SUBTITLE_TYPE_JSON3):
        """
        Returns the subtitles url for the provided 'language' and 'format'.

        This method returns None if not found.
        """
        if not language or not format:
            return None
        
        if language not in VALID_LANGUAGES:
            return None

        if self.subtitles:
            if language == LANGUAGE_DEFAULT:
                language = list(self.subtitles.keys())[0]

            if language in self.subtitles:
                for type in self.subtitles[language]:
                    if type['ext'] == format:
                        type['language'] = language
                        return type

        return None
    
    def download_subtitles(self, language = LANGUAGE_DEFAULT, format = SUBTITLE_TYPE_JSON3, output_filename = 'subtitles'):
        subtitles = self.get_subtitles(language, format)

        if not subtitles:
            return None

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + SUBTITLE_TYPE_JSON3
        
        download_file(subtitles['url'], output_filename)
    
    def __get_all_automatic_subtitles(self):
        self.automatic_subtitles = self.data['automatic_captions']

    def get_automatic_subtitles(self, language = LANGUAGE_DEFAULT, format = SUBTITLE_TYPE_JSON3):
        """
        Returns the automatic subtitles for the provided 'language' and 'format'.

        This method returns None if not found.
        """
        if not language or not format:
            return None
        
        if language not in VALID_LANGUAGES:
            return None

        if self.automatic_subtitles:
            if language == LANGUAGE_DEFAULT:
                language = list(self.automatic_subtitles.keys())[0]

            if language in self.automatic_subtitles:
                for type in self.automatic_subtitles[language]:
                    if type['ext'] == format:
                        type['language'] = language
                        return type

        return None
    
    def download_automatic_subtitles(self, language = LANGUAGE_DEFAULT, format = SUBTITLE_TYPE_JSON3, output_filename = 'automatic_subtitles'):
        automatic_subtitles = self.get_automatic_subtitles(language, format)

        if not automatic_subtitles:
            return None

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + SUBTITLE_TYPE_JSON3
        
        download_file(automatic_subtitles['url'], output_filename)
    
    # TODO: Maybe get_spanish_subtitles, get_english_subtitles?

    def __get_all_formats(self):
        self.formats = self.data['formats']
    
    def __get_video_formats(self):
        self.video_formats = {}
        for format in self.formats:
            if format['aspect_ratio'] and 'format_note' in format and format['format_note'] != 'storyboard' and format['format_note'] != 'Premium':
                # We customize the format preserving only interesting fields
                self.video_formats[str(format['height'])] = {
                    'format_id': format['format_id'],
                    'url': format['url'],
                    'quality': format['quality'],
                    'width': format['width'],
                    'height': format['height'],
                    'extension': format['ext'],
                    'video_extension': format['video_ext'], # Yes, redundant
                    'fps': format['fps'],
                    'aspect_ratio': format['aspect_ratio'],
                    'vbr': format['vbr'],
                }

    def get_best_quality_video_format(self):
        """
        Returns the best quality video format.
        """
        if len(self.video_formats.keys()) == 0:
            return None
    
        return self.video_formats[sorted(self.video_formats.keys(), key = float, reverse = True)[0]]
    
    def get_video_format(self, quality: int = QUALITY_DEFAULT):
        """
        Returns the video format of the provided 'quality' that is the height we usually associate
        with the video quality (1080 is for 1080p that is 1920x1080).

        If you provide 1080 as 'quality' parameter you will receive the video format of that 
        height, if existing, or None if not.
        """
        if quality not in VALID_QUALITIES:
            return None

        if not self.video_formats or len(self.video_formats.keys()) == 0:
            return None
        
        if quality == QUALITY_DEFAULT:
            quality = sorted(self.video_formats.keys(), key = float, reverse = True)[0]

        quality = str(quality)
        
        if not quality in self.video_formats:
            return None
        
        return self.video_formats[quality]

    def download(self, quality: int = QUALITY_DEFAULT, output_filename: str = 'video.mp4'):
        """
        Downloads the video in the provided 'quality' quality if existing and stores it
        locally as 'output_filename' with the video format extension, so any extension 
        provided will be ignored.

        This method returns the real output filename that has been downloaded.
        """
        video_format = self.get_video_format(quality)

        if not video_format:
            # TODO: Raise exception
            return None

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + video_format['video_extension']

        try:
            # I remove the file because youtube-dl will detect it as downloaded and pass
            os_remove(output_filename)
        except:
            pass
        
        # I use the youtubedl download method because it is faster than others
        self.youtubedl = YoutubeDL({
            'outtmpl': output_filename,
            'format': video_format['format_id']
        })
        self.youtubedl.download(self.url)

        return output_filename

    def __get_audio_formats(self):
        self.audio_formats = {}
        for format in self.formats:
            if 'width' in format and not format['width'] and 'height' in format and not format['height']:
                # We first check the language
                if not format['language'] in self.audio_formats:
                    self.audio_formats[format['language']] = {}

                # We customize the format preserving only interesting fields
                self.audio_formats[format['language']][str(format['abr'])] = {
                    'format_id': format['format_id'],
                    'url': format['url'],
                    'quality': format['quality'],
                    'language': format['language'], # Yes, redundant
                    'extension': format['ext'],
                    'audio_extension': format['audio_ext'], # Yes, redundant
                    'abr': format['abr'],
                }

    def get_best_quality_audio_format(self, language = LANGUAGE_DEFAULT):
        """
        Returns the highest audio (based on quality) available that is for the provided
        'language' language. If 'language' is None, the first language is provided.
        """
        if language not in VALID_LANGUAGES:
            return None

        # No audios detected
        if len(self.audio_formats.keys()) == 0:
            return None

        if language != LANGUAGE_DEFAULT:
            # Specific audio requested
            if len(self.audio_formats[language].keys()) == 0:
                return None
        
            if not language in self.audio_formats:
                return None
        else:
            # Default audio is just the first one: simple
            language = list(self.audio_formats.keys())[0]
        
        return self.audio_formats[language][sorted(self.audio_formats[language].keys(), key = float, reverse = True)[0]]

    def download_audio(self, language = LANGUAGE_DEFAULT, output_filename = 'audio.mp3'):
        """
        Downloads the best audio available for the provided 'language' and stores it locally
        as 'output_filename' with the audio format extension, so any extension provided will
        be ignored.

        This method returns the real output filename that has been downloaded.
        """
        audio_format = self.get_best_quality_audio_format(language)

        if not audio_format:
            # TODO: Raise exception
            return None

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + audio_format['audio_extension']

        try:
            # I remove the file because youtube-dl will detect it as downloaded and pass
            os_remove(output_filename)
        except:
            pass
        
        # I use the youtubedl download method because it is faster than others
        self.youtubedl = YoutubeDL({
            'outtmpl': output_filename,
            'format': audio_format['format_id']
        })
        self.youtubedl.download(self.url)

        return output_filename

    def download_with_audio(self, quality = QUALITY_FULL_HD, language = LANGUAGE_DEFAULT, output_filename = 'video.mp4'):
        """
        Downloads the video in the provided 'quality' and with the best quality audio found
        for the provided 'language'.
        """
        video = self.get_video_format(quality)
        audio = self.get_best_quality_audio_format(language)

        if not video or not audio:
            # TODO: Raise exception
            return None

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]

        # I will merge them, so I don't need another extension that the merged one
        merged_file_extension = 'mp4'
        output_filename += '.' + merged_file_extension

        try:
            # I remove the file (if existing) because youtube-dl will detect it as
            # previsouly downloaded and will not download it again
            os_remove(output_filename)
        except:
            pass

        # Thank you boss: https://gist.github.com/khalid32/129cdd43d7347601a6515eeb6e1bc2da
        self.youtubedl = YoutubeDL({
            'outtmpl': output_filename,
            'format': video['format_id'] + '+' + audio['format_id'],
            'merge_output_format': merged_file_extension
        })
        self.youtubedl.download(self.url)

        return output_filename
    