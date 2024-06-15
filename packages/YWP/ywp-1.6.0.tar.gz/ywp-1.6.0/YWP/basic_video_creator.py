def basic_video_creator(image_folder="images/", animation_choice="None", frame_rate=25, video_name="output", video_type=".mp4", video_platform="Youtube", image_time=5):
    import os
    from moviepy.editor import ImageClip, concatenate_videoclips
    from moviepy.video.fx import all as vfx

    VIDEO_DURATIONS = {
        'Youtube': 60,
        'Facebook': 20,
        'Instagram': 15,
        'Tiktok': 60
    }

    try:
        files = os.listdir(image_folder)
        image_files = [os.path.join(image_folder, f) for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        image_files.sort()
    except:
        raise ValueError("Not Found Images")

    if video_platform in VIDEO_DURATIONS:
        video_duration = VIDEO_DURATIONS[video_platform]
    else:
        raise ValueError(f"Unsupported video platform: {video_platform}. Choose from Youtube, Facebook, Instagram, or Tiktok.")

    video_clips = []
    for i, image_file in enumerate(image_files):
        clip = ImageClip(image_file).set_duration(image_time)
        video_clips.append(clip)
        
        if i < len(image_files) - 1 and animation_choice:
            next_clip = ImageClip(image_files[i + 1]).set_duration(image_time)
            if animation_choice == 'FadeIn':
                fade_duration = min(1, image_time / 2)
                video_clips.append(next_clip.crossfadein(fade_duration).set_start(clip.end))
            elif animation_choice == 'FadeOut':
                video_clips.append(clip.crossfadeout(1).set_end(clip.end))
            elif animation_choice == 'Rotate':
                rotate_clip = next_clip.rotate(lambda t: 360*t).set_start(clip.end)
                video_clips.append(rotate_clip)
            elif animation_choice == 'FlipHorizontal':
                video_clips.append(next_clip.fx(vfx.mirror_x).set_start(clip.end))
            elif animation_choice == 'FlipVertical':
                video_clips.append(next_clip.fx(vfx.mirror_y).set_start(clip.end))
    
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    output_file = f"{video_name}.{video_type}"
    final_video.write_videofile(output_file, fps=frame_rate)
    return 'done'
