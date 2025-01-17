import cv2
import os
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def create_caption_file(youtube_captions_file_name, captions_file_name, video_file_name, image_frame_directory):
    f = open(youtube_captions_file_name)
    lines = f.readlines()
    line_number = 1

    caption_file = open(captions_file_name, "a")

    while line_number < len(lines) - 1:
        from_time = lines[line_number][0:8]
        to_time = lines[line_number][18:25]

        from_time_in_milliseconds = sum(x * int(t) for x, t in zip([3600, 60, 1], from_time.split(":"))) * 1000 + \
                                    int(lines[line_number][9:12])

        to_time_in_milliseconds = sum(x * int(t) for x, t in zip([3600, 60, 1], to_time.split(":"))) * 1000 + \
                                  int(lines[line_number][9:12])

        vidcap = cv2.VideoCapture(video_file_name)

        for time_in_milliseconds in range(from_time_in_milliseconds, to_time_in_milliseconds, 5000):
            print(str(time_in_milliseconds) + '.jpg' + '\t' + cleanhtml(lines[line_number + 1]))
            caption_file.write(str(time_in_milliseconds) + '.jpg' + '\t' + cleanhtml(lines[line_number + 1]))

            vidcap.set(cv2.CAP_PROP_POS_MSEC, int(time_in_milliseconds))
            success, image = vidcap.read()
            if success:
                if not os.path.exists(image_frame_directory):
                    os.makedirs(image_frame_directory)
                cv2.imwrite(image_frame_directory + str(time_in_milliseconds) + '.jpg', image)

        line_number = line_number + 4


dataset_number = '1'
video_file_name = 'C:/Users/Sireesha Keesara/PycharmProjects/lab4/data/video/' + dataset_number + '.mp4'
youtube_captions_file_name = 'C:/Users/Sireesha Keesara/PycharmProjects/lab4/data/youtube_captions/' + dataset_number + '.txt'
captions_file_name = 'C:/Users/Sireesha Keesara/PycharmProjects/lab4/data/captions/' + dataset_number + '.txt'
image_frame_directory = 'data/image_frames/' + dataset_number + '/'
create_caption_file(youtube_captions_file_name, captions_file_name, video_file_name, image_frame_directory)