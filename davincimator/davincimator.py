import os
import glob
import cv2
import DaVinciResolveScript as dvr


class Davincimator:
    def __init__(self):
        resolve = dvr.scriptapp('Resolve')
        self.project_manager = resolve.GetProjectManager()

    def get_project_by_name(self, name: str):
        project = self.project_manager.CreateProject(name)

        if project:
            return project
        else:
            return self.project_manager.LoadProject(name)

    def create_copy_to_dir(self, path: str) -> bool:
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path)
            return True

    def find_files_source_dir(self, path: str, media_extensions):
        files = []
        for extension in media_extensions:
            files.extend(glob.glob(os.path.join(path, extension)))

        return files

    def add_files_to_timeline(self, project, timeline_name, files):
        media_pool = project.GetMediaPool()
        imported_media = media_pool.ImportMedia(files)

        timeline_count = project.GetTimelineCount()
        if timeline_count == 0:
            media_pool.CreateTimelineFromClips(timeline_name, imported_media)
        else:
            # search in the existing timelines
            found_timeline = None
            for i in range(1, timeline_count + 1):
                timeline = project.GetTimelineByIndex(i)

                if timeline_name == timeline.GetName():
                    found_timeline = timeline
                    break

            if found_timeline:
                project.SetCurrentTimeline(found_timeline)

                # for some reason AppendToTimeline(imported_media) does not work
                for a_media in imported_media:
                    media_pool.AppendToTimeline(a_media)
            else:
                # could not find the timeline in the existing ones, create a new one
                media_pool.CreateTimelineFromClips(timeline_name, imported_media)

    def setFPSforProjectTimline(self, project, files):
        highest_fps = 0
        for file in files:
            video = cv2.VideoCapture(file)
            temp_fps = video.get(cv2.CAP_PROP_FPS)

            if temp_fps > highest_fps:
                highest_fps = temp_fps

        project.SetSetting('timelineFrameRate', highest_fps)
